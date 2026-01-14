# src/status_window.py
import tkinter as tk
from tkinter import ttk, scrolledtext
from src.memory_monitor import MemoryMonitor
from src.memory_cleaner import MemoryCleaner
from src.log_manager import LogManager

class StatusWindow:
    def __init__(self, on_clean_callback):
        self.on_clean_callback = on_clean_callback
        self.monitor = MemoryMonitor()
        self.logger = LogManager()
        self.window = None
        self.updating = False

    def show(self):
        """显示状态窗口"""
        if self.window and self.window.winfo_exists():
            self.window.lift()
            return

        self.window = tk.Tk()
        self.window.title("内存清理工具")
        self.window.geometry("400x350")
        self.window.resizable(False, False)

        self._create_widgets()
        self._update_display()

        # 关闭窗口时隐藏而非退出
        self.window.protocol("WM_DELETE_WINDOW", self.hide)

        # 启动自动刷新
        self._start_update_timer()

    def hide(self):
        """隐藏窗口"""
        if self.window:
            self.window.withdraw()

    def _create_widgets(self):
        """创建界面组件"""
        # 标题
        title_label = tk.Label(
            self.window,
            text="内存使用状态",
            font=("Microsoft YaHei", 14, "bold")
        )
        title_label.pack(pady=10)

        # 内存信息框架
        info_frame = ttk.LabelFrame(self.window, text="当前状态", padding=10)
        info_frame.pack(fill="x", padx=15, pady=5)

        # 内存使用率进度条
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            info_frame,
            variable=self.progress_var,
            maximum=100,
            length=350,
            mode='determinate'
        )
        self.progress_bar.pack(pady=5)

        # 详细信息标签
        self.info_label = tk.Label(
            info_frame,
            text="加载中...",
            font=("Microsoft YaHei", 10)
        )
        self.info_label.pack(pady=5)

        # 清理按钮
        clean_btn = ttk.Button(
            self.window,
            text="立即清理内存",
            command=self._on_clean
        )
        clean_btn.pack(pady=10)

        # 最近记录框架
        log_frame = ttk.LabelFrame(self.window, text="最近清理记录", padding=10)
        log_frame.pack(fill="both", expand=True, padx=15, pady=5)

        # 日志文本框
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            height=8,
            font=("Consolas", 9),
            state='disabled'
        )
        self.log_text.pack(fill="both", expand=True)

    def _update_display(self):
        """更新显示内容"""
        # 获取内存信息
        mem_info = self.monitor.get_memory_info()

        # 更新进度条
        self.progress_var.set(mem_info["percent"])

        # 更新信息标签
        self.info_label.config(
            text=f"已用: {mem_info['used']} GB / {mem_info['total']} GB ({mem_info['percent']}%)"
        )

        # 更新日志
        self._update_logs()

    def _update_logs(self):
        """更新日志显示"""
        self.log_text.config(state='normal')
        self.log_text.delete(1.0, tk.END)

        logs = self.logger.get_recent_logs(limit=10)
        if not logs:
            self.log_text.insert(tk.END, "暂无清理记录")
        else:
            for log in reversed(logs):
                timestamp = log['timestamp'][:19]  # 去掉毫秒
                line = f"[{timestamp}] {log['before_percent']}% -> {log['after_percent']}%, 释放 {log['freed']}GB\n"
                self.log_text.insert(tk.END, line)

        self.log_text.config(state='disabled')

    def _on_clean(self):
        """清理按钮回调"""
        result = self.on_clean_callback()
        self._update_display()

    def _start_update_timer(self):
        """启动定时更新"""
        if self.window and self.window.winfo_exists():
            self._update_display()
            self.window.after(3000, self._start_update_timer)  # 每3秒更新
