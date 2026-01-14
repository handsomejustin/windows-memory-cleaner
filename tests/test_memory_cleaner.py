# tests/test_memory_cleaner.py
import pytest
from unittest.mock import patch, MagicMock
from src.memory_cleaner import MemoryCleaner

def test_clean_system_cache():
    """测试系统缓存清理"""
    cleaner = MemoryCleaner()

    # 模拟 Windows API 调用成功
    # Patch the actual location where it's used in the code
    with patch('src.memory_cleaner.ctypes.windll.kernel32.SetProcessWorkingSetSize') as mock_api:
        mock_api.return_value = 1  # 返回成功

        result = cleaner.clean()

        # 验证返回结构
        assert "before" in result
        assert "after" in result
        assert "freed" in result
        assert "success" in result
        assert result["success"] == True

def test_clean_with_api_error():
    """测试 API 调用失败的情况"""
    cleaner = MemoryCleaner()

    # 模拟 API 抛出异常
    # Patch the actual location where it's used in the code
    with patch('src.memory_cleaner.ctypes.windll.kernel32.SetProcessWorkingSetSize') as mock_api:
        mock_api.side_effect = Exception("API Error")

        result = cleaner.clean()

        assert result["success"] == False
        assert "error" in result
        assert result["freed"] == 0
