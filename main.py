import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import sys
import subprocess
import shutil
import threading
import psutil
import time
from pathlib import Path

class HTMLToEXEConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("HTML转EXE/Python工具")
        self.root.geometry("750x750")
        self.root.resizable(True, True)
        self.root.minsize(650, 600)
        
        # 存储配置信息
        self.input_dir = tk.StringVar()
        self.output_dir = tk.StringVar()
        self.window_title = tk.StringVar(value="My Application")
        self.icon_path = tk.StringVar()
        self.html_file = tk.StringVar(value="index.html")
        self.convert_type = tk.StringVar(value="exe")  # exe 或 py
        
        # API设置相关变量
        self.enable_api = tk.BooleanVar(value=False)
        self.api_executables = []  # 存储选择的可执行文件路径
        self.running_processes = []  # 存储运行的进程
        self.monitoring_thread = None
        self.monitoring_active = False
        
        self.setup_ui()
        
    def setup_ui(self):
        # 设置样式
        style = ttk.Style()
        try:
            style.theme_use("clam")  # 尝试使用更现代的主题
        except tk.TclError:
            pass  # 如果不支持则使用默认

        # 自定义样式
        style.configure("Title.TLabel", font=("微软雅黑", 16, "bold"))
        style.configure("TLabelframe.Label", font=("微软雅黑", 10, "bold"))
        style.configure("Accent.TButton", font=("微软雅黑", 10, "bold"))
        style.configure("TButton", padding=6)
        style.configure("Status.TLabel", relief="sunken", anchor="center", padding=5)

        # 主框架
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

        # 标题
        title_label = ttk.Label(main_frame, text="HTML 转 EXE / Python 工具", style="Title.TLabel")
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))

        # === 转换类型选择 ===
        type_frame = ttk.LabelFrame(main_frame, text="转换设置", padding=(15, 10))
        type_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        type_frame.columnconfigure(1, weight=1)

        ttk.Label(type_frame, text="转换类型:").grid(row=0, column=0, sticky=tk.W, padx=(0, 15))
        ttk.Radiobutton(type_frame, text="EXE 可执行文件", variable=self.convert_type, value="exe").grid(row=0, column=1, sticky=tk.W)
        ttk.Radiobutton(type_frame, text="Python 脚本", variable=self.convert_type, value="py").grid(row=0, column=2, sticky=tk.W, padx=(25, 0))

        # === 输入输出配置 ===
        io_frame = ttk.LabelFrame(main_frame, text="目录配置", padding=(15, 10))
        io_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        io_frame.columnconfigure(1, weight=1)

        # 输入目录
        ttk.Label(io_frame, text="HTML 项目目录:").grid(row=0, column=0, sticky=tk.W, pady=8)
        input_frame = ttk.Frame(io_frame)
        input_frame.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5)
        input_frame.columnconfigure(0, weight=1)
        ttk.Entry(input_frame, textvariable=self.input_dir, font=("微软雅黑", 9)).grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        ttk.Button(input_frame, text="浏览", command=self.browse_input_dir, width=8).grid(row=0, column=1)

        # 输出目录
        ttk.Label(io_frame, text="输出目录:").grid(row=1, column=0, sticky=tk.W, pady=8)
        output_frame = ttk.Frame(io_frame)
        output_frame.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5)
        output_frame.columnconfigure(0, weight=1)
        ttk.Entry(output_frame, textvariable=self.output_dir, font=("微软雅黑", 9)).grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        ttk.Button(output_frame, text="浏览", command=self.browse_output_dir, width=8).grid(row=0, column=1)

        # === 应用配置 ===
        config_frame = ttk.LabelFrame(main_frame, text="应用配置", padding=(15, 10))
        config_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        config_frame.columnconfigure(1, weight=1)

        # 窗口标题
        ttk.Label(config_frame, text="窗口标题:").grid(row=0, column=0, sticky=tk.W, pady=8)
        ttk.Entry(config_frame, textvariable=self.window_title, font=("微软雅黑", 9)).grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5)

        # 图标文件
        ttk.Label(config_frame, text="图标文件 (.ico):").grid(row=1, column=0, sticky=tk.W, pady=8)
        icon_frame = ttk.Frame(config_frame)
        icon_frame.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5)
        icon_frame.columnconfigure(0, weight=1)
        ttk.Entry(icon_frame, textvariable=self.icon_path, font=("微软雅黑", 9)).grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        ttk.Button(icon_frame, text="浏览", command=self.browse_icon, width=8).grid(row=0, column=1)

        # 主HTML文件
        ttk.Label(config_frame, text="主HTML文件名:").grid(row=2, column=0, sticky=tk.W, pady=8)
        ttk.Entry(config_frame, textvariable=self.html_file, font=("微软雅黑", 9)).grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5)

        # === API设置 ===
        api_frame = ttk.LabelFrame(main_frame, text="API服务设置（可选）", padding=(15, 10))
        api_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        api_frame.columnconfigure(1, weight=1)

        # 启用API复选框
        ttk.Checkbutton(api_frame, text="启用API服务", variable=self.enable_api, command=self.toggle_api_settings).grid(row=0, column=0, sticky=tk.W, pady=5)

        # API可执行文件列表
        self.api_listbox = tk.Listbox(api_frame, height=4, font=("微软雅黑", 9))
        self.api_listbox.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        self.api_listbox.columnconfigure(0, weight=1)

        # API操作按钮
        api_button_frame = ttk.Frame(api_frame)
        api_button_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Button(api_button_frame, text="添加可执行文件", command=self.add_api_executable).grid(row=0, column=0, padx=(0, 10))
        ttk.Button(api_button_frame, text="移除选中", command=self.remove_api_executable).grid(row=0, column=1, padx=(0, 10))
        ttk.Button(api_button_frame, text="清空列表", command=self.clear_api_executables).grid(row=0, column=2)

        # === 提示信息 ===
        info_label = ttk.Label(main_frame, text="说明：确保HTML项目完整，图标为.ico格式（仅EXE可用）", foreground="gray")
        info_label.grid(row=5, column=0, columnspan=3, pady=15, sticky=(tk.W, tk.E))

        # === 转换按钮 ===
        convert_btn = ttk.Button(main_frame, text="开始转换", command=self.convert_to_exe, style="Accent.TButton")
        convert_btn.grid(row=6, column=0, columnspan=3, pady=25)

        # === 状态栏 ===
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=7, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)

        self.status_label = ttk.Label(main_frame, text="就绪", style="Status.TLabel")
        self.status_label.grid(row=8, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        # 绑定窗口关闭事件
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def toggle_api_settings(self):
        """切换API设置状态"""
        pass  # 可以在这里添加启用/禁用逻辑
        
    def add_api_executable(self):
        """添加API可执行文件"""
        file_path = filedialog.askopenfilename(
            title="选择API可执行文件",
            filetypes=[("可执行文件", "*.exe"), ("所有文件", "*.*")]
        )
        if file_path:
            if file_path not in self.api_executables:
                self.api_executables.append(file_path)
                self.update_api_listbox()
                self.update_status(f"已添加API可执行文件: {os.path.basename(file_path)}")
            else:
                messagebox.showwarning("警告", "该文件已存在列表中")
                
    def remove_api_executable(self):
        """移除选中的API可执行文件"""
        selection = self.api_listbox.curselection()
        if selection:
            index = selection[0]
            removed_file = os.path.basename(self.api_executables[index])
            del self.api_executables[index]
            self.update_api_listbox()
            self.update_status(f"已移除: {removed_file}")
        else:
            messagebox.showwarning("警告", "请先选择要移除的文件")
            
    def clear_api_executables(self):
        """清空API可执行文件列表"""
        if self.api_executables:
            count = len(self.api_executables)
            self.api_executables.clear()
            self.update_api_listbox()
            self.update_status(f"已清空 {count} 个API可执行文件")
            
    def update_api_listbox(self):
        """更新API列表框显示"""
        self.api_listbox.delete(0, tk.END)
        for exe_path in self.api_executables:
            self.api_listbox.insert(tk.END, os.path.basename(exe_path))
            
    def start_api_services(self):
        """启动API服务"""
        if not self.enable_api.get() or not self.api_executables:
            return
            
        self.update_status("正在启动API服务...")
        
        # 停止之前可能运行的服务
        self.stop_api_services()
        
        # 启动新的服务
        for exe_path in self.api_executables:
            try:
                if os.path.exists(exe_path):
                    # 启动进程，隐藏窗口
                    startupinfo = subprocess.STARTUPINFO()
                    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                    startupinfo.wShowWindow = subprocess.SW_HIDE
                    
                    process = subprocess.Popen(
                        [exe_path],
                        startupinfo=startupinfo,
                        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
                    )
                    self.running_processes.append(process)
                    self.update_status(f"已启动API服务: {os.path.basename(exe_path)}")
                else:
                    self.update_status(f"API文件不存在: {exe_path}")
            except Exception as e:
                self.update_status(f"启动API服务失败 {os.path.basename(exe_path)}: {str(e)}")
                
        # 启动监控线程
        if self.running_processes and not self.monitoring_active:
            self.monitoring_active = True
            self.monitoring_thread = threading.Thread(target=self.monitor_processes, daemon=True)
            self.monitoring_thread.start()
            
    def stop_api_services(self):
        """停止API服务"""
        self.monitoring_active = False
        
        # 终止所有运行的进程
        for process in self.running_processes:
            try:
                # 先尝试优雅关闭
                process.terminate()
                try:
                    process.wait(timeout=3)
                except subprocess.TimeoutExpired:
                    # 如果优雅关闭失败，强制终止
                    process.kill()
                    process.wait()
            except Exception as e:
                print(f"终止进程失败: {e}")
                
        self.running_processes.clear()
        self.update_status("API服务已停止")
        
    def monitor_processes(self):
        """监控进程状态"""
        while self.monitoring_active:
            # 检查进程是否还在运行
            for process in self.running_processes[:]:  # 使用副本避免修改列表时出错
                try:
                    if process.poll() is not None:  # 进程已结束
                        self.running_processes.remove(process)
                        self.update_status("检测到API服务已停止")
                except Exception:
                    if process in self.running_processes:
                        self.running_processes.remove(process)
                        
            time.sleep(1)  # 每秒检查一次
            
    def browse_input_dir(self):
        directory = filedialog.askdirectory(title="选择HTML项目目录")
        if directory:
            self.input_dir.set(directory)
            
    def browse_output_dir(self):
        directory = filedialog.askdirectory(title="选择输出目录")
        if directory:
            self.output_dir.set(directory)
            
    def browse_icon(self):
        file_path = filedialog.askopenfilename(
            title="选择图标文件",
            filetypes=[("图标文件", "*.ico"), ("所有文件", "*.*")]
        )
        if file_path:
            self.icon_path.set(file_path)
            
    def update_status(self, message):
        self.status_label.config(text=message)
        self.root.update_idletasks()
        
    def validate_inputs(self):
        """验证输入"""
        if not self.input_dir.get():
            messagebox.showerror("错误", "请选择HTML项目目录")
            return False
            
        if not os.path.exists(self.input_dir.get()):
            messagebox.showerror("错误", "HTML项目目录不存在")
            return False
            
        if not self.output_dir.get():
            messagebox.showerror("错误", "请选择输出目录")
            return False
            
        # 检查主HTML文件是否存在
        html_path = os.path.join(self.input_dir.get(), self.html_file.get())
        if not os.path.exists(html_path):
            messagebox.showerror("错误", f"主HTML文件不存在: {html_path}")
            return False
            
        return True
            
    def convert_to_exe(self):
        # 验证输入
        if not self.validate_inputs():
            return
            
        # 开始转换
        self.progress.start()
        self.update_status("正在准备转换...")
        
        try:
            # 启动API服务（如果启用）
            self.start_api_services()
            
            if self.convert_type.get() == "exe":
                self.create_exe()
                self.update_status("EXE转换完成!")
                messagebox.showinfo("成功", f"EXE文件已生成到: {self.output_dir.get()}")
            else:
                self.create_python_script()
                self.update_status("Python脚本生成完成!")
                messagebox.showinfo("成功", f"Python脚本已生成到: {self.output_dir.get()}")
        except Exception as e:
            self.update_status(f"转换失败: {str(e)}")
            messagebox.showerror("错误", f"转换失败: {str(e)}")
        finally:
            self.progress.stop()
            
    def create_python_script(self):
        """创建可运行的Python脚本"""
        self.update_status("正在生成Python脚本...")
        
        # 创建输出目录
        output_dir = self.output_dir.get()
        os.makedirs(output_dir, exist_ok=True)
        
        # 复制HTML文件到输出目录
        html_output_dir = os.path.join(output_dir, "html")
        if os.path.exists(html_output_dir):
            shutil.rmtree(html_output_dir)
        shutil.copytree(self.input_dir.get(), html_output_dir)
        
        # 创建主Python脚本
        self.create_standalone_python_script(output_dir)
        
    def create_standalone_python_script(self, output_dir):
        """创建独立的Python脚本"""
        # 转义字符串中的特殊字符
        window_title_escaped = self.window_title.get().replace('"', '\\"').replace('\\', '\\\\')
        html_file_escaped = self.html_file.get().replace('"', '\\"').replace('\\', '\\\\')
        script_name = f"{self.window_title.get().replace(' ', '_')}.py"
        
        script_content = f'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HTML应用程序 - {window_title_escaped}
自动生成的Python脚本
"""

import os
import sys
import webview

def get_html_path():
    """获取HTML文件路径"""
    # 如果是打包后的exe
    if getattr(sys, 'frozen', False):
        # 运行在打包环境中
        base_path = sys._MEIPASS
        html_path = os.path.join(base_path, 'html', '{html_file_escaped}')
    else:
        # 运行在开发环境中
        script_dir = os.path.dirname(os.path.abspath(__file__))
        html_path = os.path.join(script_dir, 'html', '{html_file_escaped}')
    
    return f"file:///" + html_path.replace("\\\\", "/")

def main():
    """主函数"""
    # 创建WebView窗口
    window = webview.create_window(
        "{window_title_escaped}",
        get_html_path(),
        width=1200,
        height=800,
        resizable=True,
        fullscreen=False
    )
    
    # 启动应用
    webview.start()

if __name__ == "__main__":
    main()
'''
        
        script_name = f"{self.window_title.get().replace(' ', '_')}.py"
        script_path = os.path.join(output_dir, script_name)
        
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(script_content)
            
        # 创建requirements.txt
        requirements_content = '''pywebview>=3.0
'''
        requirements_path = os.path.join(output_dir, "requirements.txt")
        with open(requirements_path, 'w', encoding='utf-8') as f:
            f.write(requirements_content)
            
        # 创建README文件 - 修复转义问题
        window_title_readme = self.window_title.get().replace('"', '\\"').replace('\\', '\\\\')
        script_name_readme = script_name.replace('"', '\\"').replace('\\', '\\\\')
        
        readme_content = f'''# {window_title_readme}

这是一个自动生成的HTML应用程序。

## 使用方法

1. 安装依赖：
   ```
   pip install -r requirements.txt
   ```

2. 运行程序：
   ```
   python {script_name_readme}
   ```

## 文件说明

- `{script_name_readme}`: 主程序文件
- `html/`: HTML项目文件夹
- `requirements.txt`: 依赖包列表

## 系统要求

- Python 3.6+
- Windows/Linux/macOS
'''
        readme_path = os.path.join(output_dir, "README.md")
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
            
    def create_exe(self):
        """创建EXE文件"""
        # 创建临时工作目录
        work_dir = os.path.join(self.output_dir.get(), "temp_webview_build")
        if os.path.exists(work_dir):
            shutil.rmtree(work_dir)
        os.makedirs(work_dir)
        
        self.update_status("正在复制文件...")
        
        # 复制HTML项目文件
        self.copy_project_files(work_dir)
        
        # 创建主Python脚本
        self.create_main_script(work_dir)
        
        # 使用PyInstaller打包
        self.build_with_pyinstaller(work_dir)
        
        # 清理临时文件
        # shutil.rmtree(work_dir)
        
    def copy_project_files(self, work_dir):
        """复制HTML项目文件到工作目录"""
        project_dir = self.input_dir.get()
        html_dir = os.path.join(work_dir, "html")
        os.makedirs(html_dir, exist_ok=True)
        
        # 复制所有文件
        for item in os.listdir(project_dir):
            src_path = os.path.join(project_dir, item)
            dst_path = os.path.join(html_dir, item)
            if os.path.isdir(src_path):
                shutil.copytree(src_path, dst_path)
            else:
                shutil.copy2(src_path, dst_path)
                
    def create_main_script(self, work_dir):
        """创建主Python脚本"""
        # 转义字符串中的特殊字符
        window_title_escaped = self.window_title.get().replace('\\', '\\\\').replace('"', '\\"')
        html_file_escaped = self.html_file.get().replace('\\', '\\\\').replace('"', '\\"')
        
        script_content = f'''import webview
import os
import sys

def resource_path(relative_path):
    """获取资源文件路径"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def main():
    # 创建WebView窗口
    html_file = resource_path("html/{html_file_escaped}")
    window = webview.create_window(
        "{window_title_escaped}",
        f"file:///" + html_file.replace("\\\\", "/"),
        width=1200,
        height=800,
        resizable=True,
        fullscreen=False
    )
    
    # 启动应用
    webview.start()

if __name__ == "__main__":
    main()
'''
        
        script_path = os.path.join(work_dir, "main.py")
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(script_content)
            
    def build_with_pyinstaller(self, work_dir):
        """使用PyInstaller构建exe"""
        self.update_status("正在安装必要依赖...")
        
        # 切换到工作目录
        original_cwd = os.getcwd()
        os.chdir(work_dir)
        
        try:
            # 安装必要的包
            try:
                import webview
            except ImportError:
                subprocess.check_call([sys.executable, "-m", "pip", "install", "pywebview"])
                
            try:
                import PyInstaller
            except ImportError:
                subprocess.check_call([sys.executable, "-m", "pip", "install", "PyInstaller"])
                
            self.update_status("正在构建EXE文件...")
            
            # 构建命令
            cmd = [
                sys.executable, "-m", "PyInstaller",
                "--onefile",
                "--windowed",
                "--add-data", f"html{os.pathsep}html",
                "--name", self.window_title.get().replace(" ", "_")
            ]
            
            # 添加图标
            if self.icon_path.get() and os.path.exists(self.icon_path.get()):
                cmd.extend(["--icon", self.icon_path.get()])
                
            cmd.append("main.py")
            
            # 执行构建
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                raise Exception(f"PyInstaller构建失败: {result.stderr}")
                
            # 复制生成的exe到输出目录
            dist_dir = os.path.join(work_dir, "dist")
            if os.path.exists(dist_dir):
                exe_files = [f for f in os.listdir(dist_dir) if f.endswith('.exe')]
                if exe_files:
                    src_exe = os.path.join(dist_dir, exe_files[0])
                    dst_exe = os.path.join(self.output_dir.get(), exe_files[0])
                    shutil.copy2(src_exe, dst_exe)
                    
        finally:
            os.chdir(original_cwd)
            
    def on_closing(self):
        """窗口关闭事件处理"""
        # 停止API服务
        self.stop_api_services()
        
        # 关闭窗口
        self.root.destroy()

def main():
    root = tk.Tk()
    
    # 设置窗口样式
    try:
        # 尝试设置一些现代样式
        style = ttk.Style()
        if 'win' in sys.platform:
            style.theme_use('vista')
    except:
        pass
        
    app = HTMLToEXEConverter(root)
    root.mainloop()

if __name__ == "__main__":
    main()