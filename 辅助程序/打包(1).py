import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, font, simpledialog, ttk
import subprocess
import os
import sys
import pkg_resources
import threading
import shutil
import ctypes
import difflib
import webbrowser
import psutil
import datetime
import time

# 优化DPI感知
if sys.platform == "win32":
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)  # 使应用程序具有系统DPI感知
    except Exception:
        pass

class PyPacker:
    def __init__(self, root, file_to_pack=None):
        self.root = root
        self.root.title("Silent Packager ➵ 无言打包")
        self.root.geometry("800x600")
        self.root.configure(bg="#282c34")

        # 创建菜单栏
        menubar = tk.Menu(root, bg="#282c34", fg="white")
        root.config(menu=menubar)
        file_menu = tk.Menu(menubar, tearoff=0, bg="#282c34", fg="white")
        menubar.add_cascade(label="文件", menu=file_menu)
        file_menu.add_command(label="退出", command=root.quit)
        setting_menu = tk.Menu(menubar, tearoff=0, bg="#282c34", fg="white")
        menubar.add_cascade(label="设置", menu=setting_menu)
        setting_menu.add_command(label="修改字体", command=self.change_font)

        # 创建顶部标签
        self.top_label = tk.Label(root, text="➵PyPacker➵", font=("Arial", 24, "bold"), bg="#282c34", fg="white")
        self.top_label.pack(pady=20, fill=tk.X)

        # 创建选择框和按钮
        self.frame = tk.Frame(root, bg="#282c34")
        self.frame.pack(pady=20, fill=tk.X)

        self.pack_type_label = tk.Label(self.frame, text="选择打包类型:", font=("Arial", 12), bg="#282c34", fg="white")
        self.pack_type_label.grid(row=0, column=0, padx=10, sticky="w")

        self.pack_type_var = tk.StringVar(value="single")
        self.pack_type_single = tk.Radiobutton(self.frame, text="单个打包", variable=self.pack_type_var, value="single", font=("Arial", 12), bg="#282c34", fg="white", selectcolor="#282c34")
        self.pack_type_single.grid(row=0, column=1)
        self.pack_type_single.select()  # 默认选择单个打包
        self.pack_type_batch = tk.Radiobutton(self.frame, text="批量打包", variable=self.pack_type_var, value="batch", font=("Arial", 12), bg="#282c34", fg="white", selectcolor="#282c34")
        self.pack_type_batch.grid(row=0, column=2)

        self.output_type_label = tk.Label(self.frame, text="选择输出格式:", font=("Arial", 12), bg="#282c34", fg="white")
        self.output_type_label.grid(row=1, column=0, padx=10, sticky="w")

        self.output_type_var = tk.StringVar(value="onefile")
        self.output_type_onefile = tk.Radiobutton(self.frame, text="单文件", variable=self.output_type_var, value="onefile", font=("Arial", 12), bg="#282c34", fg="white", selectcolor="#282c34")
        self.output_type_onefile.grid(row=1, column=1)
        self.output_type_onefile.select()  # 默认选择单文件
        self.output_type_folder = tk.Radiobutton(self.frame, text="文件夹", variable=self.output_type_var, value="folder", font=("Arial", 12), bg="#282c34", fg="white", selectcolor="#282c34")
        self.output_type_folder.grid(row=1, column=2)

        self.select_button = tk.Button(root, text="选择文件", command=self.select_files, font=("Arial", 12), bg="#61dafb", fg="black")
        self.select_button.pack(pady=10, fill=tk.X)

        self.output_dir_button = tk.Button(root, text="选择输出目录", command=self.select_output_dir, font=("Arial", 12), bg="#61dafb", fg="black")
        self.output_dir_button.pack(pady=10, fill=tk.X)

        # 创建进程显示区域
        self.process_label = tk.Label(root, text="↶程序终端↷", font=("Arial", 12), bg="#282c34", fg="white")
        self.process_label.pack(fill=tk.X)
        self.process_text = scrolledtext.ScrolledText(root, width=80, height=10, font=("Arial", 12), bg="#333333", fg="#005d77")
        self.process_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.process_text.bind("<Control-MouseWheel>", self.zoom_text)
        self.process_text.bind("<Return>", self.handle_input)
        self.process_text.bind("<Motion>", self.handle_mouse_motion)
        self.process_text.bind("<Control-Button-1>", self.open_output_dir)
        self.process_text.bind("<Button-3>", self.copy_selected_text)
        self.process_text.bind("<Up>", self.recall_last_command)
        self.process_text.config(state=tk.DISABLED)

        # 配置文本标签样式
        self.process_text.tag_configure("italic", font=("Arial", 12, "italic"), foreground="#005d77")
        self.process_text.tag_configure("normal", font=("Arial", 12), foreground="#005d77")
        self.process_text.tag_configure("warning", font=("Arial", 12), foreground="#ffcc00")
        self.process_text.tag_configure("error", font=("Arial", 12), foreground="#ff0000")
        self.process_text.tag_configure("cursor", background="white", foreground="black")

        # 初始化终端输出
        self.print_to_terminal("   Silent Shell", "normal")
        self.print_to_terminal("版权所有  Silent Studio™。保留所有权利。", "normal")

        # 创建开始打包按钮
        self.start_button = tk.Button(root, text="开始打包", command=self.start_packing, font=("Arial", 12), bg="#61dafb", fg="black")
        self.start_button.pack(pady=20, fill=tk.X)

        # 创建清空缓存按钮
        self.clear_cache_button = tk.Button(root, text="清空缓存", command=self.clear_cache, font=("Arial", 12), bg="#61dafb", fg="black")
        self.clear_cache_button.pack(pady=10, fill=tk.X)

        # 创建颜色说明区域
        self.color_label = tk.Label(root, text="颜色说明:", font=("Arial", 12), bg="#282c34", fg="white")
        self.color_label.pack(fill=tk.X)
        self.color_frame = tk.Frame(root, bg="#282c34")
        self.color_frame.pack(fill=tk.X)
        self.info_label = tk.Label(self.color_frame, text="信息", font=("Arial", 12), bg="#005d77", fg="white", width=10)
        self.info_label.grid(row=0, column=0, padx=10, pady=5)
        self.warning_label = tk.Label(self.color_frame, text="警告", font=("Arial", 12), bg="#ffcc00", fg="black", width=10)
        self.warning_label.grid(row=0, column=1, padx=10, pady=5)
        self.error_label = tk.Label(self.color_frame, text="错误", font=("Arial", 12), bg="#ff0000", fg="black", width=10)
        self.error_label.grid(row=0, column=2, padx=10, pady=5)

        # 启动实时更新标题栏
        self.update_title_bar()

        # 如果有文件被拖动到程序上，自动打包该文件
        if file_to_pack:
            self.pack_type_var.set("single")
            self.output_type_var.set("onefile")
            self.files = file_to_pack
            self.print_to_terminal(f"已选择文件：{self.files}", "info")
            self.select_output_dir()
            self.start_packing()

    def print_to_terminal(self, message, tag="normal"):
        self.process_text.config(state=tk.NORMAL)
        self.process_text.insert(tk.END, f"₪{message}\n", tag)
        self.process_text.config(state=tk.DISABLED)
        self.process_text.see(tk.END)

    def select_files(self):
        pack_type = self.pack_type_var.get()
        if pack_type == "single":
            self.files = filedialog.askopenfilename(filetypes=[("Python files", "*.py")])
            if self.files:
                self.print_to_terminal(f"已选择文件：{self.files}", "info")
        elif pack_type == "batch":
            self.files = filedialog.askopenfilenames(filetypes=[("Python files", "*.py")])
            if self.files:
                self.print_to_terminal(f"已选择{len(self.files)}个文件进行批量打包", "info")

    def select_output_dir(self):
        self.output_dir = filedialog.askdirectory()
        if self.output_dir:
            self.print_to_terminal(f"已选择输出目录：{self.output_dir}", "info")

    def start_packing(self):
        if not hasattr(self, 'files') or not self.files:
            self.print_to_terminal("请先选择需要打包的文件", "warning")
            return
        if not hasattr(self, 'output_dir') or not self.output_dir:
            self.print_to_terminal("请先选择输出目录", "warning")
            return

        # 检查PyInstaller是否安装
        if not self.check_pyinstaller_installed():
            self.install_pyinstaller()

        # 在新线程中执行打包操作，防止界面卡顿
        packing_thread = threading.Thread(target=self.pack_files)
        packing_thread.start()

    def check_pyinstaller_installed(self):
        try:
            pkg_resources.get_distribution('PyInstaller')
            return True
        except pkg_resources.DistributionNotFound:
            return False

    def install_pyinstaller(self):
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "PyInstaller"])
            self.print_to_terminal("PyInstaller已成功安装", "info")
        except subprocess.CalledProcessError as e:
            self.print_to_terminal(f"安装PyInstaller失败：{e}", "error")

    def pack_files(self):
        pack_type = self.pack_type_var.get()
        output_type = self.output_type_var.get()
        if pack_type == "single":
            self.pack_single_file(output_type)
        elif pack_type == "batch":
            self.pack_batch_files(output_type)

    def pack_single_file(self, output_type):
        try:
            self.print_to_terminal("开始单个文件打包...", "info")
            if output_type == "onefile":
                command = ['pyinstaller', '--onefile', '--distpath', self.output_dir, self.files]
            else:
                command = ['pyinstaller', '--distpath', self.output_dir, self.files]
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    self.print_to_terminal(output.strip(), "info")
            self.print_to_terminal("单个文件打包完成", "info")
            self.print_to_terminal(f"输出路径：{self.output_dir}", "info")
        except subprocess.CalledProcessError as e:
            self.print_to_terminal(f"单个文件打包失败：{e}", "error")

    def pack_batch_files(self, output_type):
        try:
            self.print_to_terminal("开始批量文件打包...", "info")
            for file in self.files:
                if output_type == "onefile":
                    command = ['pyinstaller', '--onefile', '--distpath', self.output_dir, file]
                else:
                    command = ['pyinstaller', '--distpath', self.output_dir, file]
                process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
                while True:
                    output = process.stdout.readline()
                    if output == '' and process.poll() is not None:
                        break
                    if output:
                        self.print_to_terminal(output.strip(), "info")
                self.print_to_terminal(f"{file} 打包完成", "info")
            self.print_to_terminal("批量文件打包完成", "info")
            self.print_to_terminal(f"输出路径：{self.output_dir}", "info")
        except subprocess.CalledProcessError as e:
            self.print_to_terminal(f"批量文件打包失败：{e}", "error")

    def clear_cache(self):
        try:
            if not hasattr(self, 'files') or not self.files:
                self.print_to_terminal("您还没有打包任何文件", "warning")
                return

            if os.path.exists('build'):
                shutil.rmtree('build')
            if os.path.exists('dist'):
                shutil.rmtree('dist')
            if os.path.exists(f'{os.path.splitext(os.path.basename(self.files))[0]}.spec'):
                os.remove(f'{os.path.splitext(os.path.basename(self.files))[0]}.spec')
            self.print_to_terminal("缓存已清空", "info")
        except Exception as e:
            if "'PyPacker' object has no attribute 'files'" in str(e):
                self.print_to_terminal("您还没有打包任何文件", "warning")
            else:
                self.print_to_terminal("出错啦!!!反馈请联系：Silent_xiaomiao@outlook.com", "error")
                self.print_to_terminal(f"【错误信息】\n{e}", "error")

    def zoom_text(self, event):
        if event.state == 4:  # 检测Ctrl键是否被按下
            current_font = self.process_text.cget("font")
            current_size = int(current_font.split()[1])
            if event.delta > 0:  # 向上滚动，放大
                new_size = current_size + 2
            else:  # 向下滚动，缩小
                new_size = current_size - 2
            self.process_text.config(font=(current_font.split()[0], new_size))

    def change_font(self):
        self.font_window = tk.Toplevel(self.root)
        self.font_window.title("选择字体")
        self.font_window.geometry("400x300")

        self.font_listbox = tk.Listbox(self.font_window)
        self.font_listbox.pack(fill=tk.BOTH, expand=True)
        self.search_entry = tk.Entry(self.font_window)
        self.search_entry.pack(fill=tk.X)
        self.search_entry.bind("<KeyRelease>", self.search_fonts)
        self.load_fonts()

        apply_button = tk.Button(self.font_window, text="应用", command=self.apply_font)
        apply_button.pack(pady=10)

    def load_fonts(self):
        self.all_fonts = font.families()
        for f in self.all_fonts:
            self.font_listbox.insert(tk.END, f)

    def search_fonts(self, event):
        search_text = self.search_entry.get().lower()
        self.font_listbox.delete(0, tk.END)
        if search_text:
            # 使用 difflib 进行模糊匹配
            matches = difflib.get_close_matches(search_text, self.all_fonts, n=10, cutoff=0.1)
            for match in matches:
                self.font_listbox.insert(tk.END, match)
        else:
            for f in self.all_fonts:
                self.font_listbox.insert(tk.END, f)

    def apply_font(self):
        selected_font = self.font_listbox.get(tk.ACTIVE)
        current_font = self.process_text.cget("font")
        font_parts = current_font.split()

        # 检查 font_parts 是否包含足够的元素
        if len(font_parts) < 2:
            # 如果解析失败，提供一个默认字体大小
            default_size = 12
            new_font = (selected_font, default_size)
            messagebox.showwarning("警告", f"无法解析当前字体大小，已使用默认字体大小 {default_size}")
        else:
            current_size = int(font_parts[1])
            new_font = (selected_font, current_size)

        # 应用新字体到所有相关组件
        self.process_text.config(font=new_font)
        self.pack_type_label.config(font=new_font)
        self.pack_type_single.config(font=new_font)
        self.pack_type_batch.config(font=new_font)
        self.output_type_label.config(font=new_font)
        self.output_type_onefile.config(font=new_font)
        self.output_type_folder.config(font=new_font)
        self.select_button.config(font=new_font)
        self.output_dir_button.config(font=new_font)
        self.start_button.config(font=new_font)
        self.clear_cache_button.config(font=new_font)

        # 关闭字体选择窗口
        self.font_window.destroy()

    def handle_input(self, event):
        content = self.process_text.get("insert linestart", "insert lineend").strip().lower()
        if content in ["/", "/help", "/h"]:
            self.print_help()
        elif content == "/v":
            self.developer_mode = True
            self.print_to_terminal("您正在使用开发者模式", "info")
            # 模拟申请管理员权限
            self.print_to_terminal("已申请管理员权限", "info")
        elif content in ["/windows powershell", "powershell"]:
            self.start_powershell()
        elif content == "/cmd":
            self.start_cmd()
        elif content == "/clear":
            self.process_text.config(state=tk.NORMAL)
            self.process_text.delete(1.0, tk.END)
            self.process_text.config(state=tk.DISABLED)
        elif content == "/date":
            self.print_to_terminal(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "normal")
        elif content.startswith("/打包"):
            self.custom_pack(content)
        else:
            self.print_help()

    def print_help(self):
        help_message = (
            "帮助页面\n"
            "/v: 进入开发者模式\n"
            "/windows powershell: 接入Windows PowerShell\n"
            "/cmd: 接入cmd\n"
            "/打包 [文件路径] 输出 [输出路径]: 自定义打包命令\n"
            "/clear: 清空终端内容\n"
            "/date: 显示当前日期和时间\n"
        )
        self.print_to_terminal(help_message, "info")

    def start_powershell(self):
        self.print_to_terminal("接入Windows PowerShell", "info")
        process = subprocess.Popen(["powershell.exe"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        threading.Thread(target=self.read_process_output, args=(process,)).start()

    def start_cmd(self):
        self.print_to_terminal("接入cmd", "info")
        process = subprocess.Popen(["cmd.exe"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        threading.Thread(target=self.read_process_output, args=(process,)).start()

    def read_process_output(self, process):
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                self.print_to_terminal(output.strip(), "normal")
        self.print_to_terminal("命令执行完成", "normal")

    def custom_pack(self, command):
        parts = command.split()
        if len(parts) < 3:
            self.print_to_terminal("命令格式错误，正确格式：/打包 [文件路径] 输出 [输出路径]", "warning")
            return

        file_path = parts[1]
        output_dir = parts[3] if len(parts) >= 4 else os.getcwd()

        if not os.path.exists(file_path):
            self.print_to_terminal(f"文件不存在：{file_path}", "error")
            return

        if not os.path.exists(output_dir):
            self.print_to_terminal(f"输出目录不存在：{output_dir}", "error")
            return

        try:
            self.print_to_terminal(f"开始打包文件：{file_path}", "info")
            command = ['pyinstaller', '--onefile', '--distpath', output_dir, file_path]
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    self.print_to_terminal(output.strip(), "info")
            self.print_to_terminal(f"打包完成，输出路径：{output_dir}", "info")
        except Exception as e:
            self.print_to_terminal(f"打包失败：{e}", "error")

    def handle_mouse_motion(self, event):
        # 检测鼠标是否悬停在输出路径上
        pass

    def open_output_dir(self, event):
        # 检测是否按下Ctrl并点击输出路径
        pass

    def copy_selected_text(self, event):
        try:
            selected_text = self.process_text.get(tk.SEL_FIRST, tk.SEL_LAST)
            self.process_text.clipboard_clear()
            self.process_text.clipboard_append(selected_text)
            self.process_text.tag_remove(tk.SEL, "1.0", tk.END)
        except tk.TclError:
            pass

    def recall_last_command(self, event):
        # 暂时未实现
        pass

    def update_title_bar(self):
        cpu_usage = psutil.cpu_percent(interval=1)
        net_io = psutil.net_io_counters()
        upload_speed = net_io.bytes_sent / 1024 / 1024  # 转换为MB
        download_speed = net_io.bytes_recv / 1024 / 1024  # 转换为MB
        self.root.title(f"Silent Packager ➵ 无言打包              -CPU占用: {cpu_usage}%               -WIFI: {upload_speed:.2f}MB/s ↾    {download_speed:.2f}MB/s ⇂")
        self.root.after(1000, self.update_title_bar)

def main():
    root = tk.Tk()
    file_to_pack = None
    if len(sys.argv) > 1:
        file_to_pack = sys.argv[1]
    app = PyPacker(root, file_to_pack)
    root.mainloop()

if __name__ == "__main__":
    main()