import tkinter as tk
from tkinter import ttk
import json
from tkinter import messagebox
from datetime import datetime, timedelta
from gui.CenterWindow import center_window as cw
from tkinter import colorchooser

class AdvancedSettings:
    def __init__(self, master):
        self.top = tk.Toplevel(master)
        self.top.transient(master)
        self.top.grab_set()
        self.master = self.top
        self.top.title("课表生成高级设置 v3.0")
        cw(self.top, 400, 340)
        self.top.resizable(False, False)

        self.main_frame = ttk.Frame(self.top)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.create_basic_settings()
        self.create_time_rules()  # 删除这一行
        self.create_action_buttons()
        self.create_subject_management()
        self.load_settings()

    def load_settings(self):
        """加载保存的设置"""
        try:
            with open("settings.json", 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # 加载基本设置
            basic = data.get('basic', {})
            self.days_spin.set(basic.get('days', 5))
            self.cycle_combo.set(basic.get('cycle', '每周'))
            self.max_duration.delete(0, tk.END)
            self.max_duration.insert(0, basic.get('max_duration', '45'))
            self.break_interval.delete(0, tk.END)
            self.break_interval.insert(0, basic.get('break_interval', '10'))
            self.periods_spin.set(basic.get('daily_periods', 8))  # 新增的每天课节数
            self.class_count.set(basic.get('class_count', 6))
            self.grade_entry.delete(0, tk.END)
            self.grade_entry.insert(0, basic.get('grade', '三'))

            # 加载时间规则
            for item in self.time_tree.get_children():
                self.time_tree.delete(item)
            for rule in data.get('time_rules', []):
                self.time_tree.insert("", tk.END, values=rule)

            # 加载科目数据
            for item in self.subject_tree.get_children():
                self.subject_tree.delete(item)
            for subject in data.get('subjects', []):
                if isinstance(subject, dict):
                    self.subject_tree.insert("", tk.END, values=(subject['name'], subject['teachers']))
                else:
                    self.subject_tree.insert("", tk.END, values=(subject, 0))

        except FileNotFoundError:
            pass  # 首次运行时没有设置文件是正常的
        except Exception as e:
            messagebox.showerror("加载错误", f"无法加载设置:\n{str(e)}")

    def create_basic_settings(self):
        basic_frame = ttk.Frame(self.notebook)
        self.notebook.add(basic_frame, text="基本设置")

        # 每天课节数（添加校验）
        ttk.Label(basic_frame, text="每天课节数:").grid(row=0, column=0, pady=5)
        self.periods_spin = ttk.Spinbox(basic_frame, from_=4, to=12, width=5, validate="focusout", 
        validatecommand=(basic_frame.register(self.validate_periods), '%P'))  # 输入验证
        self.periods_spin.set(8)  # 设置默认值
        #self.periods_spin.grid(row=0, column=1)
        self.periods_spin.grid(row=0, column=1, padx=5, sticky=tk.W)

        # 课程天数（添加校验）
        ttk.Label(basic_frame, text="课程天数:").grid(row=0, column=2, pady=5)
        self.days_spin = ttk.Spinbox(basic_frame,from_=1,to=7,width=5,validate="focusout",
            validatecommand=(basic_frame.register(self.validate_days), '%P'))
        self.days_spin.grid(row=0, column=3, padx=5, sticky=tk.W)

        # 最大课时长（添加校验）
        ttk.Label(basic_frame, text="最大课时长:").grid(row=1, column=0, pady=5)
        self.max_duration = ttk.Entry(basic_frame, width=8,validate="focusout",
            validatecommand=(basic_frame.register(self.validate_duration), '%P'))
        self.max_duration.insert(0, "45")
        self.max_duration.grid(row=1, column=1, padx=5, sticky=tk.W)
        
        # 休息间隔（添加校验）
        ttk.Label(basic_frame, text="休息间隔:").grid(row=1, column=2, pady=5)
        self.break_interval = ttk.Entry(
            basic_frame, 
            width=8,
            validate="focusout",
            validatecommand=(basic_frame.register(self.validate_break), '%P')
        )
        self.break_interval.insert(0, "10")
        self.break_interval.grid(row=1, column=3, padx=5, sticky=tk.W)
        
        # 年级输入（添加校验）
        ttk.Label(basic_frame, text="年级:").grid(row=2, column=0, pady=5)
        self.grade_entry = ttk.Entry(
            basic_frame, 
            width=5,
            validate="focusout",
            validatecommand=(basic_frame.register(self.validate_grade), '%P')
        )
        self.grade_entry.insert(0, "三")
        self.grade_entry.grid(row=2, column=1, padx=5, sticky=tk.W)
        
        # 班级数量（添加校验）
        ttk.Label(basic_frame, text="班级数量:").grid(row=2, column=2, pady=5)
        self.class_count = ttk.Spinbox(
            basic_frame, 
            from_=1, 
            to=20, 
            width=5,
            validate="focusout",
            validatecommand=(basic_frame.register(self.validate_class_count), '%P')
        )
        self.class_count.grid(row=2, column=3, padx=5, sticky=tk.W)
        # 新增每天课节数设置 ▲

        # 循环周期（添加缺失的控件定义）
        ttk.Label(basic_frame, text="循环周期:").grid(row=3, column=0, padx=10)
        self.cycle_combo = ttk.Combobox(basic_frame, values=["单周", "双周", "每周"], width=6, validate="focusout", validatecommand=(basic_frame.register(self.validate_cycle), '%P'))
        self.cycle_combo.set("每周")
        self.cycle_combo.grid(row=3, column=1)

    def validate_days(self, value):
        try:
            num = int(value)
            if 1 <= num <= 7:
                return True
            messagebox.showerror("输入错误", "课程天数范围1-7")
            self.days_spin.set(5)
            return False
        except ValueError:
            messagebox.showerror("输入错误", "请输入有效数字")
            self.days_spin.set(5)
            return False

    def validate_duration(self, value):
        try:
            num = int(value)
            if 20 <= num <= 120:
                return True
            messagebox.showerror("输入错误", "课时长范围20-120分钟")
            self.max_duration.delete(0, tk.END)
            self.max_duration.insert(0, "45")
            return False
        except ValueError:
            messagebox.showerror("输入错误", "请输入有效数字")
            self.max_duration.delete(0, tk.END)
            self.max_duration.insert(0, "45")
            return False

    def validate_break(self, value):
        try:
            num = int(value)
            if 5 <= num <= 60:
                return True
            messagebox.showerror("输入错误", "休息间隔范围5-60分钟")
            self.break_interval.delete(0, tk.END)
            self.break_interval.insert(0, "10")
            return False
        except ValueError:
            messagebox.showerror("输入错误", "请输入有效数字")
            self.break_interval.delete(0, tk.END)
            self.break_interval.insert(0, "10")
            return False

    def validate_grade(self, value):
        valid_grades = ['一', '二', '三', '四', '五', '六', '七', '八', '九']
        if value in valid_grades:
            return True
        messagebox.showerror("输入错误", "请输入有效年级（一至九年级）")
        self.grade_entry.delete(0, tk.END)
        self.grade_entry.insert(0, "三")
        return False

    def validate_cycle(self, value):
        valid_cycles = ["单周", "双周", "每周"]
        if value in valid_cycles:
            return True
        messagebox.showerror("输入错误", "请选择有效的循环周期（单周/双周/每周）")
        self.cycle_combo.set("每周")
        return False

    def validate_class_count(self, value):
        try:
            num = int(value)
            if 1 <= num <= 20:
                return True
            messagebox.showerror("输入错误", "班级数量范围1-20")
            self.class_count.set(6)  # 强制重置为默认值
            return False
        except ValueError:
            messagebox.showerror("输入错误", "请输入有效数字")
            self.class_count.set(6)  # 强制重置为默认值
            return False

    def validate_periods(self, value):
        try:
            num = int(value)
            if 4 <= num <= 12:
                return True
            messagebox.showerror("输入错误", "课节数范围必须在4-12之间")
            self.periods_spin.set(8)
            return False
        except ValueError:
            messagebox.showerror("输入错误", "请输入有效的数字")
            self.periods_spin.set(8)
            return False

    def create_subject_management(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="科目管理")

        # Treeview配置
        columns = ("subject", "teachers")
        self.subject_tree = ttk.Treeview(
            frame,
            columns=columns,
            show="headings",
            height=10,
            selectmode="browse"  # 新增选择模式限制
        )
        # 配置列时添加不可拉伸设置
        self.subject_tree.column("subject", width=273, stretch=False)
        self.subject_tree.column("teachers", width=100, stretch=False)

        self.subject_tree.heading("subject", text="科目名称")
        self.subject_tree.heading("teachers", text="教师人数")
        self.subject_tree.column("subject", width=273)
        self.subject_tree.column("teachers", width=100)

        # 示例数据
        sample_data = [
            ("语文", 3),
            ("数学", 2),
            ("英语", 2),
            ("体育", 0)
        ]
        for item in sample_data:
            self.subject_tree.insert("", tk.END, values=item)

        # 滚动条
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.subject_tree.yview)
        self.subject_tree.configure(yscrollcommand=scrollbar.set)

        # 布局
        self.subject_tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        # 操作按钮
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=1, column=0, pady=5)
        ttk.Button(btn_frame, text="添加", command=self.add_subject).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="删除", command=self.del_subject).pack(side=tk.LEFT, padx=5)

    def create_time_rules(self):
        # 创建时间规则的标签页
        time_frame = ttk.Frame(self.notebook)
        self.notebook.add(time_frame, text="时间规则")

        # 时间规则表格
        columns = ("day", "have", "start", "end", "max_classes")
        self.time_tree = ttk.Treeview(time_frame, columns=columns, show="headings", height=7)

        # 设置列
        self.time_tree.heading("day", text="星期")
        self.time_tree.heading("have", text="课程")
        self.time_tree.heading("start", text="开始时间")
        self.time_tree.heading("end", text="结束时间")
        self.time_tree.heading("max_classes", text="最大课时")

        # 设置列宽
        self.time_tree.column("day", width=40)
        self.time_tree.column("have", width=40)
        self.time_tree.column("start", width=100)
        self.time_tree.column("end", width=100)
        self.time_tree.column("max_classes", width=80)

        self.time_tree.grid(row=0, column=0, sticky="ew")

        # 添加示例数据
        days = ["周一", "周二", "周三", "周四", "周五"]
        self.time_tree.insert("", tk.END, values=("周一", "有","08:00", "17:00", 6))
        self.time_tree.insert("", tk.END, values=("周二", "有","08:00", "17:00", 6))
        self.time_tree.insert("", tk.END, values=("周三", "有","08:00", "17:00", 6))
        self.time_tree.insert("", tk.END, values=("周四", "有","08:00", "17:00", 6))
        self.time_tree.insert("", tk.END, values=("周五", "有","08:00", "17:00", 6))
        self.time_tree.insert("", tk.END, values=("周六", "无","", "", None))
        self.time_tree.insert("", tk.END, values=("周日", "按需","", "", None))

        # 编辑按钮
        btn_frame = ttk.Frame(time_frame)
        btn_frame.grid(row=1, column=0, pady=5)
        ttk.Button(btn_frame, text="编辑选中规则", command=self.edit_time_rule).pack(side=tk.LEFT, padx=2)

    def create_action_buttons(self):
        # 操作按钮框架
        frame = ttk.Frame(self.main_frame)
        frame.pack()

        ttk.Button(frame, text="确定", command=self.export_settings).pack(side=tk.RIGHT, padx=5)
        ttk.Button(frame, text="取消", command=self.master.destroy).pack(side=tk.RIGHT, padx=5)
        ttk.Button(frame, text="恢复默认", command=self.reset_defaults).pack(side=tk.RIGHT, padx=5)

    def create_custom_rules(self):
        # 创建新标签页
        custom_frame = ttk.Frame(self.notebook)
        self.notebook.add(custom_frame, text="课程列表")
        
        # 创建带滚动条的列表框
        list_frame = ttk.Frame(custom_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.subject_var = tk.StringVar()
        self.custom_list = ttk.Listbox(list_frame, width=49, height=10, listvariable=self.subject_var)
        
        # 初始化预设科目
        for subject in ["道德与法治","语文","数学",'英语','日语','俄语','历史','地理','科学','物理','化学','生物学','信息科技','体育与健康','艺术','劳动','综合实践活动']:
            self.custom_list.insert(tk.END, subject)
        self.subject_var.set(' '.join(self.custom_list.get(0, tk.END)))
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.custom_list.yview)
        self.custom_list.configure(yscrollcommand=scrollbar.set)
        
        self.custom_list.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        # 按钮区域
        btn_frame = ttk.Frame(custom_frame)
        btn_frame.pack(pady=5)
        
        ttk.Button(btn_frame, text="添加课程", command=self.add_subject).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="删除课程", command=self.del_subject).pack(side=tk.LEFT, padx=5)

    def validate_teacher_count(self, value):
        try:
            num = int(value)
            if 0 <= num <= 20:
                return True
            messagebox.showerror("输入错误", "教师人数范围0-20")
            return False
        except ValueError:
            messagebox.showerror("输入错误", "请输入有效数字")
            return False

    def add_subject(self):
        win = tk.Toplevel(self.master)
        win.title("添加科目")
        win.grab_set()
        cw(win, 300, 150)

        ttk.Label(win, text="科目名称:").grid(row=0, column=0, padx=5, pady=5)
        subject_entry = ttk.Entry(win)
        subject_entry.grid(row=0, column=1)

        ttk.Label(win, text="教师人数:").grid(row=1, column=0)
        teacher_spin = ttk.Spinbox(
            win, 
            from_=0, 
            to=20, 
            width=5,
            validate="focusout",
            validatecommand=(win.register(self.validate_teacher_count), '%P')
        )
        teacher_spin.set(0)
        teacher_spin.grid(row=1, column=1)
        
        def save_subject():
            subject = subject_entry.get().strip()
            teachers = teacher_spin.get()

            if not subject:
                messagebox.showerror("错误", "科目名称不能为空")
                return

            existing = [self.subject_tree.item(item)['values'][0] 
                      for item in self.subject_tree.get_children()]
            if subject in existing:
                messagebox.showerror("错误", "科目已存在")
                return

            try:
                int(teachers)
            except ValueError:
                messagebox.showerror("错误", "教师人数必须为数字")
                return

            self.subject_tree.insert("", tk.END, values=(subject, teachers))
            win.destroy()

        ttk.Button(win, text="保存", command=save_subject).grid(row=2, columnspan=2, pady=10)

    def del_subject(self):
        selected = self.subject_tree.selection()
        if selected:
            self.subject_tree.delete(selected)

    def edit_time_rule(self):
        # 编辑时间规则对话框
        selected = self.time_tree.selection()
        if not selected:
            return

        item = self.time_tree.item(selected[0])
        values = item["values"]

        edit_win = tk.Toplevel(self.master)
        edit_win.title("编辑")
        edit_win.grab_set()  # 新增：锁定主窗口
        edit_win.transient(self.master)  # 新增：设为子窗口
        cw(edit_win, 218, 147)
        edit_win.resizable(False, False)

        # 星期选择
        ttk.Label(edit_win, text="星期:").grid(row=0, column=0)
        day_combo = ttk.Combobox(edit_win, values=["周一", "周二", "周三", "周四", "周五", "周六", "周日"])
        day_combo.set(values[0])
        day_combo.grid(row=0, column=1)

        # 有无课程
        ttk.Label(edit_win, text="有无:").grid(row=1, column=0)
        have_class = ttk.Combobox(edit_win, values=["有", "无", "按需"])
        have_class.set(values[1])
        have_class.grid(row=1, column=1)
        
        # 开始时间（先创建控件）
        ttk.Label(edit_win, text="开始时间:").grid(row=2, column=0)
        start_entry = ttk.Entry(
            edit_win, 
            validate="focusout",
            validatecommand=(edit_win.register(self.validate_time_format), '%P'))
        start_entry.insert(0, values[2])
        start_entry.grid(row=2, column=1)
        
        # 结束时间
        ttk.Label(edit_win, text="结束时间:").grid(row=3, column=0)
        end_entry = ttk.Entry(
            edit_win, 
            validate="focusout",
            validatecommand=(edit_win.register(self.validate_time_format), '%P')
        )
        end_entry.insert(0, values[3])
        end_entry.grid(row=3, column=1)
        
        # 最大课时
        ttk.Label(edit_win, text="最大课时:").grid(row=4, column=0)
        max_classes = ttk.Spinbox(edit_win, from_=1, to=12, width=5)
        max_classes.set(values[4] if values[4] else "")
        max_classes.grid(row=4, column=1)
        
        # 新增状态更新函数（移动到控件创建之后）
        def update_fields_state(event=None):
            state = "normal" if have_class.get() == "有" else "disabled"
            start_entry.configure(state=state)
            end_entry.configure(state=state)
            max_classes.configure(state=state)
            
            if state == "disabled":
                start_entry.delete(0, tk.END)
                end_entry.delete(0, tk.END)
                max_classes.set("")
        
        # 绑定组合框选择事件
        have_class.bind("<<ComboboxSelected>>", update_fields_state)
        
        # 初始化状态
        update_fields_state()
        
        # 保存按钮
        def save_changes():
            new_values = (
                day_combo.get(),
                have_class.get(),  # 保留原数据字段
                start_entry.get(),
                end_entry.get(),
                max_classes.get()
            )
            self.time_tree.item(selected[0], values=new_values)
            edit_win.destroy()

        ttk.Button(edit_win, text="保存", command=save_changes).grid(row=5, columnspan=2, pady=5)

    def validate_time_format(self, value):
        if not value:
            return True
        try:
            datetime.strptime(value, "%H:%M")
            return True
        except ValueError:
            messagebox.showerror("格式错误", "请输入正确时间格式（HH:MM）")
            return False

    def add_rule(self):
        rule_type = self.rule_type.get()
        if not rule_type:
            return

        # 根据规则类型显示详细设置对话框
        if rule_type == "禁止时间安排":
            self.add_time_ban_rule()
        elif rule_type == "课程间隔要求":
            self.add_interval_rule()
        elif rule_type == "教师时间冲突避免":
            self.add_teacher_conflict_rule()
        elif rule_type == "教室分配限制":
            self.add_classroom_limit_rule()

    def generate_time_options(self):
        times = []
        current = datetime.strptime("08:00", "%H:%M")
        for _ in range(24 * 4):  # 15分钟间隔
            times.append(current.strftime("%H:%M"))
            current += timedelta(minutes=15)
        return times

    def export_settings(self):
        try:
            subjects = []
            for item in self.subject_tree.get_children():
                values = self.subject_tree.item(item)['values']
                if int(values[1]) > 0:
                    subjects.append({"name": values[0], "teachers": int(values[1])})
                else:
                    subjects.append(values[0])

            data = {
                "basic": {
                    "days": self.days_spin.get(),
                    "cycle": self.cycle_combo.get(),
                    "max_duration": self.max_duration.get(),
                    "break_interval": self.break_interval.get(),
                    "daily_periods": self.periods_spin.get(),  # 新增
                    "class_count": self.class_count.get(),
                    "grade": self.grade_entry.get()
                },
                "time_rules": [self.time_tree.item(item, 'values') 
                              for item in self.time_tree.get_children()],
                "subjects": subjects
            }

            with open("settings.json", 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

        except Exception as e:
            messagebox.showerror("导出错误", f"错误信息:\n{str(e)}")
        finally:
            self.master.destroy()

    def generate_timetable(self):
        # 生成课表逻辑
        self.master.destroy()

    def reset_defaults(self):
        # 重置默认设置
        self.days_spin.set(5)
        self.cycle_combo.set("每周")
        self.max_duration.delete(0, tk.END)
        self.max_duration.insert(0, "45")
        self.break_interval.delete(0, tk.END)
        self.break_interval.insert(0, "10")

        self.grade_entry.delete(0, tk.END)
        self.grade_entry.insert(0, "三")
        self.class_count.set(6)

        # 清空时间规则表格
        for item in self.time_tree.get_children():
            self.time_tree.delete(item)
        days = ["周一", "周二", "周三", "周四", "周五"]
        self.time_tree.insert("", tk.END, values=("周一", "有","08:00", "17:00", 6))
        self.time_tree.insert("", tk.END, values=("周二", "有","08:00", "17:00", 6))
        self.time_tree.insert("", tk.END, values=("周三", "有","08:00", "17:00", 6))
        self.time_tree.insert("", tk.END, values=("周四", "有","08:00", "17:00", 6))
        self.time_tree.insert("", tk.END, values=("周五", "有","08:00", "17:00", 6))
        self.time_tree.insert("", tk.END, values=("周六", "无","", "", None))
        self.time_tree.insert("", tk.END, values=("周日", "按需","", "", None))


if __name__ == "__main__":
    root = tk.Tk()
    app = AdvancedSettings(root)
    root.mainloop()
