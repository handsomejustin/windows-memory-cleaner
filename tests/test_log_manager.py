# tests/test_log_manager.py
import pytest
import tempfile
import os
from src.log_manager import LogManager

def test_add_and_get_logs(tmp_path):
    """测试添加和获取日志"""
    log_file = os.path.join(tmp_path, "test_clean.log")
    manager = LogManager(log_file)

    # 添加一条日志
    manager.add_clean_log(
        before_percent=85.5,
        after_percent=72.3,
        freed_gb=2.1
    )

    # 获取日志
    logs = manager.get_recent_logs(limit=10)

    assert len(logs) == 1
    assert logs[0]["before_percent"] == 85.5
    assert logs[0]["after_percent"] == 72.3
    assert logs[0]["freed_gb"] == 2.1
    assert "timestamp" in logs[0]

def test_log_limit(tmp_path):
    """测试日志数量限制"""
    log_file = os.path.join(tmp_path, "test_clean.log")
    manager = LogManager(log_file)

    # 添加超过限制的日志
    for i in range(110):
        manager.add_clean_log(80 + i, 70 + i, 1.0)

    logs = manager.get_recent_logs(limit=200)
    assert len(logs) == 100  # 应该只保留100条
