import tkinter as tk
from tkinter import ttk
import json
from tkinter import messagebox
from datetime import datetime, timedelta
from gui.CenterWindow import center_window as cw

class AdvancedSettings:
    def __init__(self, master):
        self.master = master
        master.title("课表生成高级设置 v2.0")
        master.geometry("400x300")

        # 创建主容器
        self.main_frame = ttk.Frame(master)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 添加 Notebook 控件
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # 基本设置区域
        self.create_basic_settings()

        # 时间规则区域
        self.create_time_rules()

        # 高级规则区域
        self.create_advanced_rules()

        # 操作按钮区域
        self.create_action_buttons()

    def create_basic_settings(self):
        # 创建基本设置的标签页
        basic_frame = ttk.Frame(self.notebook)
        self.notebook.add(basic_frame, text="基本设置")

        # 课程天数设置
        ttk.Label(basic_frame, text="课程天数:").grid(row=0, column=0, sticky=tk.W)
        self.days_spin = ttk.Spinbox(basic_frame, from_=1, to=7, width=5)
        self.days_spin.set(5)
        self.days_spin.grid(row=0, column=1, sticky=tk.W, padx=5)

        # 每周循环周期
        ttk.Label(basic_frame, text="循环周期:").grid(row=0, column=2, sticky=tk.W, padx=10)
        self.cycle_combo = ttk.Combobox(basic_frame, values=["单周", "双周", "每周"], width=6)
        self.cycle_combo.set("每周")
        self.cycle_combo.grid(row=0, column=3, sticky=tk.W)

        # 课程最大时长
        ttk.Label(basic_frame, text="最大课时长(分钟):").grid(row=1, column=0, sticky=tk.W)
        self.max_duration = ttk.Entry(basic_frame, width=8)
        self.max_duration.insert(0, "45")
        self.max_duration.grid(row=1, column=1, sticky=tk.W, padx=5)

        # 休息间隔
        ttk.Label(basic_frame, text="最小休息间隔:").grid(row=1, column=2, sticky=tk.W, padx=10)
        self.break_interval = ttk.Entry(basic_frame, width=8)
        self.break_interval.insert(0, "10")
        self.break_interval.grid(row=1, column=3, sticky=tk.W)

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

    def create_advanced_rules(self):
        # 创建高级规则的标签页
        advanced_frame = ttk.Frame(self.notebook)
        self.notebook.add(advanced_frame, text="高级约束规则")

        # 规则类型选择
        ttk.Label(advanced_frame, text="添加新规则:").grid(row=0, column=0, sticky=tk.W)
        self.rule_type = ttk.Combobox(advanced_frame, values=[
            "禁止时间安排",
            "教师时间冲突避免",
            "教室分配限制"
        ], width=20)
        self.rule_type.grid(row=0, column=1, padx=5)

        # 添加规则按钮
        ttk.Button(advanced_frame, text="+ 添加", command=self.add_rule).grid(row=0, column=2)

        # 规则列表
        self.rules_list = tk.Listbox(advanced_frame, width=40, height=8)
        self.rules_list.grid(row=1, column=0, columnspan=3, pady=5, sticky="ew")

        # 规则操作按钮
        btn_frame = ttk.Frame(advanced_frame)
        btn_frame.grid(row=2, column=0, columnspan=3)
        ttk.Button(btn_frame, text="删除选中", command=self.delete_rule).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="清除所有", command=self.clear_rules).pack(side=tk.LEFT, padx=2)

    def create_action_buttons(self):
        # 操作按钮框架
        frame = ttk.Frame(self.main_frame)
        frame.pack()

        ttk.Button(frame, text="确定", command=self.export_settings).pack(side=tk.RIGHT, padx=5)
        ttk.Button(frame, text="取消", command=self.master.destroy).pack(side=tk.RIGHT, padx=5)
        ttk.Button(frame, text="恢复默认", command=self.reset_defaults).pack(side=tk.RIGHT, padx=5)

    def edit_time_rule(self):
        # 编辑时间规则对话框
        selected = self.time_tree.selection()
        if not selected:
            return

        item = self.time_tree.item(selected[0])
        values = item["values"]

        edit_win = tk.Toplevel(self.master)
        edit_win.title("编辑")
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
        start_entry = ttk.Entry(edit_win)
        start_entry.insert(0, values[2])
        start_entry.grid(row=2, column=1)
        
        # 结束时间
        ttk.Label(edit_win, text="结束时间:").grid(row=3, column=0)
        end_entry = ttk.Entry(edit_win)
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

    def add_time_ban_rule(self):
        win = tk.Toplevel(self.master)
        win.title("添加禁止时间规则")
        cw(win, 430, 105)

        # 课程选择
        ttk.Label(win, text="课程名称:").grid(row=0, column=0)
        course_entry = ttk.Entry(win)
        course_entry.grid(row=0, column=1)

        # 禁止时间
        ttk.Label(win, text="禁止时间段:").grid(row=1, column=0)
        start_combo = ttk.Combobox(win, values=self.generate_time_options())
        start_combo.grid(row=1, column=1)
        ttk.Label(win, text="至").grid(row=1, column=2)
        end_combo = ttk.Combobox(win, values=self.generate_time_options())
        end_combo.grid(row=1, column=3)

        # 适用日期
        ttk.Label(win, text="适用日期:").grid(row=2, column=0)
        days_frame = ttk.Frame(win)
        days_frame.grid(row=2, column=1, columnspan=3)
        days_vars = []
        for i, day in enumerate(["周一", "周二", "周三", "周四", "周五", "周六", "周日"]):
            var = tk.IntVar()
            cb = ttk.Checkbutton(days_frame, text=day, variable=var)
            cb.grid(row=0, column=i, padx=2)
            days_vars.append(var)

        def save_rule():
            # 收集数据并添加到规则列表
            course = course_entry.get()
            time_range = f"{start_combo.get()}-{end_combo.get()}"
            selected_days = [day for day, var in zip(["周一", "周二", "周三", "周四", "周五", "周六", "周日"], days_vars) if var.get()]

            if course and time_range and selected_days:
                rule_text = f"[禁止] {course} 在 {','.join(selected_days)} 的 {time_range}"
                self.rules_list.insert(tk.END, rule_text)
                win.destroy()

        ttk.Button(win, text="添加", command=save_rule).grid(row=3, columnspan=4, pady=5)

    def add_interval_rule(self):
        win = tk.Toplevel(self.master)
        win.title("添加课程间隔规则")
        cw(win, 218, 122)

        # 间隔时间输入
        ttk.Label(win, text="最小间隔时间(分钟):").grid(row=0, column=0)
        interval_entry = ttk.Entry(win)
        interval_entry.grid(row=0, column=1)

        def save_rule():
            interval = interval_entry.get()
            if interval.isdigit() and int(interval) > 0:
                rule_text = f"[间隔] 最小间隔时间为 {interval} 分钟"
                self.rules_list.insert(tk.END, rule_text)
                win.destroy()
            else:
                messagebox.showwarning("输入错误", "请输入有效的正整数作为间隔时间")

        ttk.Button(win, text="添加", command=save_rule).grid(row=1, columnspan=2, pady=5)

    def add_teacher_conflict_rule(self):
        win = tk.Toplevel(self.master)
        win.title("添加教师时间冲突规则")
        cw(win, 430, 90)

        # 教师选择
        ttk.Label(win, text="教师名称:").grid(row=0, column=0)
        teacher_entry = ttk.Entry(win)
        teacher_entry.grid(row=0, column=1)

        # 不可用时间段
        ttk.Label(win, text="不可用时间段:").grid(row=1, column=0)
        start_combo = ttk.Combobox(win, values=self.generate_time_options())
        start_combo.grid(row=1, column=1)
        ttk.Label(win, text="至").grid(row=1, column=2)
        end_combo = ttk.Combobox(win, values=self.generate_time_options())
        end_combo.grid(row=1, column=3)

        def save_rule():
            teacher = teacher_entry.get()
            time_range = f"{start_combo.get()}-{end_combo.get()}"
            if teacher and time_range:
                rule_text = f"[教师冲突] {teacher} 在 {time_range} 不可用"
                self.rules_list.insert(tk.END, rule_text)
                win.destroy()
            else:
                messagebox.showwarning("输入错误", "请填写教师名称和时间段")

        ttk.Button(win, text="添加", command=save_rule).grid(row=2, columnspan=4, pady=5)

    def add_classroom_limit_rule(self):
        win = tk.Toplevel(self.master)
        win.title("添加教室分配限制规则")
        cw(win, 430, 90)

        # 教室选择
        ttk.Label(win, text="教室名称:").grid(row=0, column=0)
        classroom_entry = ttk.Entry(win)
        classroom_entry.grid(row=0, column=1)

        # 不可用时间段
        ttk.Label(win, text="不可用时间段:").grid(row=1, column=0)
        start_combo = ttk.Combobox(win, values=self.generate_time_options())
        start_combo.grid(row=1, column=1)
        ttk.Label(win, text="至").grid(row=1, column=2)
        end_combo = ttk.Combobox(win, values=self.generate_time_options())
        end_combo.grid(row=1, column=3)

        def save_rule():
            classroom = classroom_entry.get()
            time_range = f"{start_combo.get()}-{end_combo.get()}"
            if classroom and time_range:
                rule_text = f"[教室限制] {classroom} 在 {time_range} 不可用"
                self.rules_list.insert(tk.END, rule_text)
                win.destroy()
            else:
                messagebox.showwarning("输入错误", "请填写教室名称和时间段")

        ttk.Button(win, text="添加", command=save_rule).grid(row=2, columnspan=4, pady=5)

    def generate_time_options(self):
        times = []
        current = datetime.strptime("08:00", "%H:%M")
        for _ in range(24 * 4):  # 15分钟间隔
            times.append(current.strftime("%H:%M"))
            current += timedelta(minutes=15)
        return times

    def delete_rule(self):
        selected = self.rules_list.curselection()
        if selected:
            self.rules_list.delete(selected[0])

    def clear_rules(self):
        self.rules_list.delete(0, tk.END)

    def export_settings(self):
        data = {
            "basic": {
                "days": self.days_spin.get(),
                "cycle": self.cycle_combo.get(),
                "max_duration": self.max_duration.get(),
                "break_interval": self.break_interval.get()
            },
            "time_rules": [self.time_tree.item(item, 'values') for item in self.time_tree.get_children()],
            "advanced_rules": list(self.rules_list.get(0, tk.END))
        }
        
        file_path = "settings.json"
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
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
        # 清空规则列表
        self.rules_list.delete(0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = AdvancedSettings(root)
    root.mainloop()