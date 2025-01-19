import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, font, simpledialog
import subprocess
import os
import sys
import pkg_resources
import threading
import shutil
import ctypes
import difflib

# 以编程方式设置 DPI 感知
try:
    ctypes.windll.user32.SetProcessDpiAwarenessContext(-4)  # PerMonitorV2
except AttributeError:
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(2)  # PerMonitor
    except AttributeError:
        pass

class PyPacker:
    def __init__(self, root):
        self.root = root
        self.root.title("PyPackager - 打包器")
        self.root.geometry("800x600")  # 设置窗口大小

        # 创建菜单栏
        menubar = tk.Menu(root)
        root.config(menu=menubar)
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="文件", menu=file_menu)
        file_menu.add_command(label="退出", command=root.quit)
        setting_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="设置", menu=setting_menu)
        setting_menu.add_command(label="修改字体", command=self.change_font)

        # 创建顶部标签
        self.top_label = tk.Label(root, text="PyPackager", font=("Arial", 24, "bold"))
        self.top_label.pack(pady=20)

        # 创建选择框和按钮
        self.frame = tk.Frame(root)
        self.frame.pack(pady=20)

        self.pack_type_label = tk.Label(self.frame, text="选择打包类型:")
        self.pack_type_label.grid(row=0, column=0, padx=10)

        self.pack_type_var = tk.StringVar()
        self.pack_type_single = tk.Radiobutton(self.frame, text="单个打包", variable=self.pack_type_var, value="single")
        self.pack_type_single.grid(row=0, column=1)
        self.pack_type_single.select()  # 默认选择单个打包
        self.pack_type_batch = tk.Radiobutton(self.frame, text="批量打包", variable=self.pack_type_var, value="batch")
        self.pack_type_batch.grid(row=0, column=2)

        self.output_type_label = tk.Label(self.frame, text="选择输出格式:")
        self.output_type_label.grid(row=1, column=0, padx=10)

        self.output_type_var = tk.StringVar()
        self.output_type_onefile = tk.Radiobutton(self.frame, text="单文件", variable=self.output_type_var, value="onefile")
        self.output_type_onefile.grid(row=1, column=1)
        self.output_type_onefile.select()  # 默认选择单文件
        self.output_type_folder = tk.Radiobutton(self.frame, text="文件夹", variable=self.output_type_var, value="folder")
        self.output_type_folder.grid(row=1, column=2)

        self.select_button = tk.Button(root, text="选择文件", command=self.select_files)
        self.select_button.pack(pady=10)

        self.output_dir_button = tk.Button(root, text="选择输出目录", command=self.select_output_dir)
        self.output_dir_button.pack(pady=10)

        # 创建进程显示区域
        self.process_label = tk.Label(root, text="打包进程:")
        
        self.process_label.pack()
        self.process_label.config(state='disabled')
        self.process_text = scrolledtext.ScrolledText(root, width=80, height=10)
        self.process_text.pack(padx=10, pady=10)
        self.process_text.bind("<Control-MouseWheel>", self.zoom_text)
        self.process_text.bind("<Return>", self.handle_input)
        self.developer_mode = False

        # 创建开始打包按钮
        self.start_button = tk.Button(root, text="开始打包", command=self.start_packing)
        self.start_button.pack(pady=20)

        # 创建清空缓存按钮
        self.clear_cache_button = tk.Button(root, text="清空缓存", command=self.clear_cache)
        self.clear_cache_button.pack(pady=10)

    def select_files(self):
        pack_type = self.pack_type_var.get()
        if pack_type == "single":
            self.files = filedialog.askopenfilename(filetypes=[("Python files", "*.py")])
            if self.files:
                self.process_text.insert(tk.END, f"已选择文件：{self.files}\n")
        elif pack_type == "batch":
            self.files = filedialog.askopenfilenames(filetypes=[("Python files", "*.py")])
            if self.files:
                self.process_text.insert(tk.END, f"已选择{len(self.files)}个文件进行批量打包\n")

    def select_output_dir(self):
        self.output_dir = filedialog.askdirectory()
        if self.output_dir:
            self.process_text.insert(tk.END, f"已选择输出目录：{self.output_dir}\n")

    def start_packing(self):
        if not self.files:
            messagebox.showwarning("警告", "请先选择需要打包的文件")
            return
        if not hasattr(self, 'output_dir') or not self.output_dir:
            messagebox.showwarning("警告", "请先选择输出目录")
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
            self.process_text.insert(tk.END, "PyInstaller已成功安装\n")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("错误", f"安装PyInstaller失败：{e}")
            self.process_text.insert(tk.END, f"安装PyInstaller失败：{e}\n")

    def pack_files(self):
        pack_type = self.pack_type_var.get()
        output_type = self.output_type_var.get()
        if pack_type == "single":
            self.pack_single_file(output_type)
        elif pack_type == "batch":
            self.pack_batch_files(output_type)

    def pack_single_file(self, output_type):
        try:
            self.process_text.insert(tk.END, "开始单个文件打包...\n")
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
                    self.process_text.insert(tk.END, output)
                    self.process_text.see(tk.END)
            self.process_text.insert(tk.END, "单个文件打包完成\n")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("错误", f"单个文件打包失败：{e}")
            self.process_text.insert(tk.END, f"单个文件打包失败：{e}\n")

    def pack_batch_files(self, output_type):
        try:
            self.process_text.insert(tk.END, "开始批量文件打包...\n")
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
                        self.process_text.insert(tk.END, output)
                        self.process_text.see(tk.END)
                self.process_text.insert(tk.END, f"{file} 打包完成\n")
            self.process_text.insert(tk.END, "批量文件打包完成\n")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("错误", f"批量文件打包失败：{e}")
            self.process_text.insert(tk.END, f"批量文件打包失败：{e}\n")

    def clear_cache(self):
        try:
            if os.path.exists('build'):
                shutil.rmtree('build')
            if os.path.exists('dist'):
                shutil.rmtree('dist')
            if os.path.exists(f'{os.path.splitext(os.path.basename(self.files))[0]}.spec'):
                os.remove(f'{os.path.splitext(os.path.basename(self.files))[0]}.spec')
            self.process_text.insert(tk.END, "缓存已清空\n")
        except Exception as e:
            messagebox.showerror("错误", f"清空缓存失败：{e}")
            self.process_text.insert(tk.END, f"清空缓存失败：{e}\n")

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
        content = self.process_text.get("insert linestart", "insert lineend")
        if content.startswith("/"):
            if content == "/v":
                self.developer_mode = True
                self.process_text.insert(tk.END, "\n您正在使用开发者模式\n")
            elif content == "/Silent" and self.developer_mode:
                self.developer_mode = False
                self.process_text.insert(tk.END, "\n已退出开发者模式并保持静默\n")
        self.process_text.insert(tk.END, "\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = PyPacker(root)
    root.mainloop()