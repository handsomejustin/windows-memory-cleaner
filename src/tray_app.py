# src/tray_app.py
import sys
import pystray
from PIL import Image, ImageDraw
from src.memory_monitor import MemoryMonitor
from src.memory_cleaner import MemoryCleaner
from src.config import ConfigManager
from src.log_manager import LogManager
from src.status_window import StatusWindow


class MemoryTrayApp:
    def __init__(self):
        # Platform guard - only Windows is supported
        if sys.platform != 'win32':
            raise RuntimeError("MemoryTrayApp only supports Windows platform")

        self.config = ConfigManager()
        self.monitor = MemoryMonitor()
        self.cleaner = MemoryCleaner()
        self.logger = LogManager()
        self.running = False
        self.icon = None
        self.status_window = None

    def create_icon(self, color="green", mem_info=None):
        """创建托盘图标

        Args:
            color: Icon color (green/yellow/red)
            mem_info: Pre-fetched memory info dict to avoid redundant calls.
                     If None, will fetch from monitor.
        """
        try:
            # 创建一个简单的内存条图标
            width, height = 64, 64
            image = Image.new('RGB', (width, height), color='white')
            draw = ImageDraw.Draw(image)

            # 绘制内存条
            colors = {
                "green": (0, 200, 0),
                "yellow": (255, 200, 0),
                "red": (255, 0, 0)
            }
            fill_color = colors.get(color, (0, 200, 0))

            # 绘制外框
            draw.rectangle([8, 16, 56, 48], outline=(100, 100, 100), width=2)

            # 绘制内存填充
            if mem_info is None:
                mem_info = self.monitor.get_memory_info()
            fill_height = int(28 * mem_info["percent"] / 100)
            if fill_height > 0:
                draw.rectangle([10, 47 - fill_height, 54, 46], fill=fill_color)

            return image
        except Exception as e:
            # Return a basic icon on error
            width, height = 64, 64
            image = Image.new('RGB', (width, height), color='white')
            draw = ImageDraw.Draw(image)
            draw.rectangle([8, 16, 56, 48], outline=(100, 100, 100), width=2)
            return image

    def get_icon_color(self, percent):
        """根据内存使用率返回图标颜色"""
        if percent < 70:
            return "green"
        elif percent < 85:
            return "yellow"
        else:
            return "red"

    def update_tooltip(self):
        """更新托盘图标的悬浮提示"""
        mem_info = self.monitor.get_memory_info()
        return f"内存: {mem_info['used']}/{mem_info['total']}GB ({mem_info['percent']}%)"

    def on_clean(self, icon=None, item=None):
        """清理内存回调"""
        result = self.cleaner.clean()
        if result["success"]:
            self.logger.add_clean_log(
                before_percent=result["before"]["percent"],
                after_percent=result["after"]["percent"],
                freed_gb=result["freed"]
            )
            print(f"清理成功: 释放 {result['freed']}GB")
        else:
            print(f"清理失败: {result.get('error', '未知错误')}")
        self.update_icon_state()

    def on_quit(self, icon=None, item=None):
        """退出回调"""
        self.running = False
        icon.stop()

    def update_icon_state(self):
        """更新图标状态（颜色和提示）"""
        try:
            mem_info = self.monitor.get_memory_info()
            color = self.get_icon_color(mem_info["percent"])
            # Ensure icon exists before updating
            if self.icon is not None:
                self.icon.icon = self.create_icon(color, mem_info=mem_info)
                self.icon.title = self.update_tooltip()
        except Exception as e:
            # Silently handle update errors to avoid disrupting the tray app
            pass

    def run(self):
        """启动托盘应用"""
        self.running = True
        self.status_window = StatusWindow(self.on_clean_with_update)

        # 创建菜单
        menu = pystray.Menu(
            pystray.MenuItem("显示内存状态", self.on_show_status),
            pystray.MenuItem("立即清理内存", self.on_clean),
            pystray.MenuItem("退出", self.on_quit)
        )

        # 创建图标
        mem_info = self.monitor.get_memory_info()
        initial_color = self.get_icon_color(mem_info["percent"])
        self.icon = pystray.Icon(
            "memory_cleaner",
            self.create_icon(initial_color, mem_info=mem_info),
            menu=menu,
            title=self.update_tooltip()
        )

        # 启动图标
        self.icon.run()

    def on_show_status(self, icon=None, item=None):
        """显示状态窗口"""
        if self.status_window:
            self.status_window.show()

    def on_clean_with_update(self):
        """清理并返回结果（供状态窗口调用）"""
        result = self.cleaner.clean()
        if result["success"]:
            self.logger.add_clean_log(
                before_percent=result["before"]["percent"],
                after_percent=result["after"]["percent"],
                freed_gb=result["freed"]
            )
            self.update_icon_state()
        return result

if __name__ == "__main__":
    app = MemoryTrayApp()
    app.run()
