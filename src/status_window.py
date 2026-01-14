# src/status_window.py
import sys
import os

# Add parent directory to path for imports to work when run directly
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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
        self.timer_id = None  # Track timer for cancellation

    def show(self):
        """显示状态窗口"""
        if self.window and self.window.winfo_exists():
            try:
                self.window.deiconify()
                self.window.lift()
            except Exception:
                # Window might be destroyed, recreate it
                self.window = None
                return self._create_new_window()
            return

        # Destroy existing window if it exists but doesn't have valid window info
        if self.window is not None:
            try:
                self.window.destroy()
            except Exception:
                pass
            self.window = None

        return self._create_new_window()

    def _create_new_window(self):
        """创建新窗口"""
        self.window = tk.Tk()
        self.window.title("内存清理工具")
        self.window.geometry("400x350")
        self.window.resizable(False, False)

        self._create_widgets()
        self._update_display()

        # 关闭窗口时隐藏而非退出
        self.window.protocol("WM_DELETE_WINDOW", self.hide)

        # 注意：不启动自动更新定时器，避免与 pystray 事件循环冲突
        # 用户可以点击"刷新"按钮或重新打开窗口来更新显示

    def hide(self):
        """隐藏窗口"""
        # Cancel timer to prevent memory leak
        self._cancel_timer()

        if self.window:
            try:
                self.window.withdraw()
            except Exception:
                # Window may already be destroyed
                pass
            # 重新创建窗口实例，避免线程问题
            self.window = None

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

        # 按钮框架
        btn_frame = tk.Frame(self.window)
        btn_frame.pack(pady=10)

        # 清理按钮
        clean_btn = ttk.Button(
            btn_frame,
            text="立即清理内存",
            command=self._on_clean
        )
        clean_btn.pack(side="left", padx=5)

        # 刷新按钮
        refresh_btn = ttk.Button(
            btn_frame,
            text="刷新",
            command=self._update_display
        )
        refresh_btn.pack(side="left", padx=5)

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
        try:
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
        except Exception as e:
            # Log error but don't crash the GUI
            print(f"Error updating display: {e}")
            pass

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
        try:
            result = self.on_clean_callback()
            self._update_display()
        except Exception as e:
            # Log error but don't crash the GUI
            print(f"Error during clean operation: {e}")
            # Still update display even if clean failed
            try:
                self._update_display()
            except Exception:
                pass

    def _start_update_timer(self):
        """启动定时更新"""
        # Cancel any existing timer first
        self._cancel_timer()

        if self.window and self.window.winfo_exists():
            self._update_display()
            # Store timer ID for later cancellation
            self.timer_id = self.window.after(3000, self._start_update_timer)  # 每3秒更新

    def _cancel_timer(self):
        """取消定时器"""
        if self.timer_id is not None and self.window is not None:
            try:
                self.window.after_cancel(self.timer_id)
            except Exception:
                pass
            finally:
                self.timer_id = None
