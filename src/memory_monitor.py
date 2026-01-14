# src/memory_monitor.py
import psutil

class MemoryMonitor:
    def __init__(self):
        self._threshold = 85

    def set_threshold(self, percent):
        """设置警告阈值"""
        if not 0 <= percent <= 100:
            raise ValueError("阈值必须在 0-100 之间")
        self._threshold = percent

    def is_over_threshold(self):
        """检查当前内存是否超过阈值"""
        info = self.get_memory_info()
        return info["percent"] >= self._threshold

    def get_memory_info(self):
        """
        获取系统内存信息

        Returns:
            dict: 包含 total(GB), used(GB), percent(%), available(GB)
        """
        mem = psutil.virtual_memory()

        return {
            "total": round(mem.total / (1024**3), 2),  # 转换为GB
            "used": round(mem.used / (1024**3), 2),
            "percent": round(mem.percent, 1),
            "available": round(mem.available / (1024**3), 2)
        }
