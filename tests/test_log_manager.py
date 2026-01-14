# tests/test_log_manager.py
import pytest
import tempfile
import os
import json
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

    # 添加超过限制的日志 - 使用有效的百分比范围
    for i in range(110):
        # Cycle through valid percentage values (0-100)
        before_pct = (i % 101)
        after_pct = ((i - 5) % 101)
        manager.add_clean_log(before_pct, after_pct, 1.0)

    logs = manager.get_recent_logs(limit=200)
    assert len(logs) == 100  # 应该只保留100条

def test_input_validation_percent_range(tmp_path):
    """测试百分比范围验证"""
    log_file = os.path.join(tmp_path, "test_clean.log")
    manager = LogManager(log_file)

    # Test before_percent out of range
    with pytest.raises(ValueError, match="before_percent must be between 0 and 100"):
        manager.add_clean_log(before_percent=150, after_percent=50, freed_gb=1.0)

    with pytest.raises(ValueError, match="before_percent must be between 0 and 100"):
        manager.add_clean_log(before_percent=-10, after_percent=50, freed_gb=1.0)

    # Test after_percent out of range
    with pytest.raises(ValueError, match="after_percent must be between 0 and 100"):
        manager.add_clean_log(before_percent=50, after_percent=150, freed_gb=1.0)

    with pytest.raises(ValueError, match="after_percent must be between 0 and 100"):
        manager.add_clean_log(before_percent=50, after_percent=-10, freed_gb=1.0)

def test_input_validation_freed_gb_non_negative(tmp_path):
    """测试freed_gb非负验证"""
    log_file = os.path.join(tmp_path, "test_clean.log")
    manager = LogManager(log_file)

    with pytest.raises(ValueError, match="freed_gb must be non-negative"):
        manager.add_clean_log(before_percent=50, after_percent=40, freed_gb=-1.0)

def test_input_validation_type_checking(tmp_path):
    """测试类型验证"""
    log_file = os.path.join(tmp_path, "test_clean.log")
    manager = LogManager(log_file)

    # Test before_percent type
    with pytest.raises(TypeError, match="before_percent must be a number"):
        manager.add_clean_log(before_percent="50", after_percent=40, freed_gb=1.0)

    with pytest.raises(TypeError, match="before_percent must be a number"):
        manager.add_clean_log(before_percent=None, after_percent=40, freed_gb=1.0)

    # Test after_percent type
    with pytest.raises(TypeError, match="after_percent must be a number"):
        manager.add_clean_log(before_percent=50, after_percent=[40], freed_gb=1.0)

    # Test freed_gb type
    with pytest.raises(TypeError, match="freed_gb must be a number"):
        manager.add_clean_log(before_percent=50, after_percent=40, freed_gb="1.0")

def test_valid_boundary_values(tmp_path):
    """测试有效边界值"""
    log_file = os.path.join(tmp_path, "test_clean.log")
    manager = LogManager(log_file)

    # Test boundary values that should work
    manager.add_clean_log(before_percent=0, after_percent=0, freed_gb=0)
    manager.add_clean_log(before_percent=100, after_percent=100, freed_gb=0)

    logs = manager.get_recent_logs(limit=10)
    assert len(logs) == 2
    assert logs[0]["before_percent"] == 0
    assert logs[1]["before_percent"] == 100

def test_load_logs_with_corrupt_json(tmp_path, caplog):
    """测试加载损坏的JSON文件"""
    log_file = os.path.join(tmp_path, "test_clean.log")
    manager = LogManager(log_file)

    # Create a corrupt JSON file
    with open(log_file, 'w', encoding='utf-8') as f:
        f.write("{invalid json content")

    # Should return empty list and log warning
    logs = manager.get_recent_logs()
    assert logs == []

    # Check that a warning was logged
    assert any("Failed to decode JSON" in record.message for record in caplog.records)

def test_save_logs_with_io_error(tmp_path, monkeypatch, caplog):
    """测试保存日志时的IO错误处理"""
    log_file = os.path.join(tmp_path, "test_clean.log")
    manager = LogManager(log_file)

    # Mock open to raise IOError
    def mock_open(*args, **kwargs):
        raise IOError("Simulated IO error")

    monkeypatch.setattr("builtins.open", mock_open)

    # Should raise IOError and log error
    with pytest.raises(IOError, match="Simulated IO error"):
        manager.add_clean_log(before_percent=50, after_percent=40, freed_gb=1.0)

    # Check that an error was logged
    assert any("Failed to write log file" in record.message for record in caplog.records)
