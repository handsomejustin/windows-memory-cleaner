# tests/test_memory_monitor.py
import pytest
from src.memory_monitor import MemoryMonitor

def test_get_memory_info():
    """测试获取系统内存信息"""
    monitor = MemoryMonitor()
    info = monitor.get_memory_info()

    # 验证返回结构
    assert "total" in info
    assert "used" in info
    assert "percent" in info
    assert "available" in info

    # 验证数据类型和范围
    assert isinstance(info["total"], float)
    assert isinstance(info["used"], float)
    assert isinstance(info["percent"], float)
    assert isinstance(info["available"], float)
    assert 0 < info["total"] <= 128  # 假设最大128GB
    assert 0 <= info["percent"] <= 100

def test_check_threshold():
    """测试阈值检测"""
    monitor = MemoryMonitor()

    # 设置低阈值，应该不触发警告
    monitor.set_threshold(99)
    assert monitor.is_over_threshold() == False

    # 设置极低阈值，应该触发警告
    monitor.set_threshold(0)
    assert monitor.is_over_threshold() == True
