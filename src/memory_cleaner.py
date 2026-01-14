# src/memory_cleaner.py
import ctypes
from src.memory_monitor import MemoryMonitor

class MemoryCleaner:
    def __init__(self):
        self.monitor = MemoryMonitor()
        self._kernel32 = ctypes.windll.kernel32

    def clean(self):
        """
        执行系统内存清理

        Returns:
            dict: 清理结果 {before, after, freed, success}
        """
        # 获取清理前的内存状态
        before = self.monitor.get_memory_info()

        try:
            # 调用 Windows API 清理系统缓存
            # SetProcessWorkingSetSize(-1, -1, -1) 会触发系统整理所有进程的工作集
            self._kernel32.SetProcessWorkingSetSize(-1, -1, -1)

            # 获取清理后的内存状态
            after = self.monitor.get_memory_info()

            # 计算释放的内存
            freed = round(before["used"] - after["used"], 2)

            return {
                "before": before,
                "after": after,
                "freed": max(0, freed),  # 确保不为负数
                "success": True
            }

        except Exception as e:
            return {
                "before": before,
                "after": before,
                "freed": 0,
                "success": False,
                "error": str(e)
            }
