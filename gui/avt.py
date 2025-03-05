import tkinter as tk
from tkinter import ttk

class AdvancedSettingsDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("高级课表设置")
        self.geometry("360x220")
        
        # 创建配置笔记本（多标签页）
        notebook = ttk.Notebook(self)
        
        # 时间设置标签页
        time_frame = ttk.Frame(notebook)
        self._create_time_settings(time_frame)
        
        # 课程规则标签页
        rule_frame = ttk.Frame(notebook)
        self._create_rule_settings(rule_frame)
        
        # 冲突处理标签页
        conflict_frame = ttk.Frame(notebook)
        self._create_conflict_settings(conflict_frame)
        
        # 在原有notebook中添加新的标签页
        course_frame = ttk.Frame(notebook)
        self._create_course_management(course_frame)
        
        notebook.add(time_frame, text="时间设置")
        notebook.add(rule_frame, text="排课规则")
        notebook.add(course_frame, text="课程管理")  # 新增标签页
        notebook.add(conflict_frame, text="冲突处理")
        notebook.pack(expand=True, fill=tk.BOTH)
        
        # 底部按钮
        btn_frame = ttk.Frame(self)
        ttk.Button(btn_frame, text="保存", command=self._save_settings).pack(side=tk.RIGHT, padx=5)
        ttk.Button(btn_frame, text="取消", command=self.destroy).pack(side=tk.RIGHT)
        btn_frame.pack(pady=10)

    def _create_time_settings(self, frame):
        # 时间段配置
        ttk.Label(frame, text="每日时间段设置").grid(row=0, column=0, sticky=tk.W)
        
        # 时间范围设置
        time_grid = ttk.Frame(frame)
        ttk.Label(time_grid, text="最早开始时间:").grid(row=0, column=0)
        self.start_time = ttk.Entry(time_grid)
        self.start_time.insert(0, "08:00")
        self.start_time.grid(row=0, column=1)
        
        ttk.Label(time_grid, text="最晚结束时间:").grid(row=1, column=0)
        self.end_time = ttk.Entry(time_grid)
        self.end_time.insert(0, "18:00")
        self.end_time.grid(row=1, column=1)
        
        ttk.Label(time_grid, text="课程间隔时间（分钟）:").grid(row=2, column=0)
        self.interval = ttk.Spinbox(time_grid, from_=5, to=60, increment=5)
        self.interval.set(10)
        self.interval.grid(row=2, column=1)
        
        time_grid.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)

    def _create_rule_settings(self, frame):
        # 排课规则设置
        rules = [
            ("必修课优先安排", "priority_required", tk.BooleanVar(value=True)),
            ("同科目间隔天数", "interval_days", tk.IntVar(value=2)),
            ("每日最大课时数", "max_daily", tk.IntVar(value=6)),
            ("允许连堂最大数", "max_consecutive", tk.IntVar(value=2))
        ]
        
        for i, (label, name, var) in enumerate(rules):
            ttk.Checkbutton(frame, text=label, variable=var).grid(row=i, column=0, sticky=tk.W)
            if "interval_days" in name or "max" in name:
                ttk.Spinbox(frame, from_=1, to=7, textvariable=var, width=5).grid(row=i, column=1, sticky=tk.W)

    def _create_conflict_settings(self, frame):
        # 冲突解决策略
        ttk.Label(frame, text="时间冲突处理策略:").grid(row=0, column=0, sticky='w')
        self.conflict_strategy = ttk.Combobox(frame, 
            values=["自动调整时间", "跳过并提示", "强制覆盖"])
        self.conflict_strategy.current(0)
        self.conflict_strategy.grid(row=0, column=1)
        
        # 优先级设置
        ttk.Label(frame, text="课程优先级顺序:").grid(row=1, column=0, sticky='w')
        self.priority_order = tk.Listbox(frame, height=4)
        for item in ["必修课程", "实验课程", "选修课程", "社团活动"]:
            self.priority_order.insert(tk.END, item)
        self.priority_order.grid(row=1, column=1)

    def _save_settings(self):
        # 这里添加保存配置的逻辑
        print("保存配置...")
        self.destroy()

    def _create_course_management(self, frame):
        """课程管理模块"""
        # 课程列表
        ttk.Label(frame, text="当前课程列表").pack(anchor=tk.W)
        self.course_list = tk.Listbox(frame, height=12, selectmode=tk.SINGLE)
        self.course_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # 操作按钮
        btn_frame = ttk.Frame(frame)
        ttk.Button(btn_frame, text="添加课程", command=self._add_course_dialog).pack(pady=5)
        ttk.Button(btn_frame, text="删除选中", command=self._remove_course).pack(pady=5)
        btn_frame.pack(side=tk.RIGHT, padx=5)

    def _add_course_dialog(self):
        """添加课程对话框"""
        dialog = tk.Toplevel(self)
        dialog.title("课程详情")
        
        # 表单字段
        fields = [
            ("课程名称", "name", tk.Entry()),
            ("课程类型", "type", ttk.Combobox(values=["必修", "选修", "实验", "社团"])),
            ("周课时数", "hours", ttk.Spinbox(from_=1, to=20, increment=1)),
            ("单次时长", "duration", ttk.Spinbox(from_=30, to=180, increment=10, format="%d分钟")),
            ("优先级", "priority", ttk.Spinbox(from_=1, to=5, increment=1))
        ]
        
        for i, (label, _, widget) in enumerate(fields):
            ttk.Label(dialog, text=label+":").grid(row=i, column=0, sticky=tk.E)
            widget.grid(row=i, column=1, pady=2)
            if label == "课程类型":
                widget.current(0)
        
        # 确认按钮
        ttk.Button(dialog, text="确认", 
            command=lambda: self._save_course(dialog, [w.get() for w in widgets])).grid(row=5, columnspan=2)
        
        widgets = [widget for _, _, widget in fields]

    def _save_course(self, dialog, data):
        """保存课程到列表"""
        if not data[0]:  # 验证课程名称
            tk.messagebox.showerror("错误", "课程名称不能为空")
            return
        self.course_list.insert(tk.END, f"{data[0]} ({data[1]}) - {data[3]} / 周{data[2]}节")
        dialog.destroy()

    def _remove_course(self):
        """删除选中课程"""
        selection = self.course_list.curselection()
        if selection:
            self.course_list.delete(selection[0])

# 使用示例
if __name__ == "__main__":
    root = tk.Tk()
    AdvancedSettingsDialog(root)
    root.mainloop()
