# tests/test_config.py
import pytest
import os
import json
import tempfile
from src.config import ConfigManager

def test_load_default_config(tmp_path):
    """测试加载默认配置"""
    # Use a temporary path to avoid polluting the default config file
    temp_config = os.path.join(tmp_path, "test_config.json")
    manager = ConfigManager(temp_config)
    assert manager.warning_threshold == 85
    assert manager.auto_clean == False
    assert manager.auto_clean_threshold == 80
    assert manager.refresh_interval == 5

def test_save_config(tmp_path):
    """测试保存配置"""
    # 使用临时文件
    temp_config = os.path.join(tmp_path, "test_config.json")
    manager = ConfigManager(temp_config)

    # 修改配置
    manager.warning_threshold = 90
    manager.save()

    # 重新加载验证
    manager2 = ConfigManager(temp_config)
    assert manager2.warning_threshold == 90

def test_warning_threshold_validation(tmp_path):
    """测试warning_threshold验证"""
    temp_config = os.path.join(tmp_path, "test_config.json")
    manager = ConfigManager(temp_config)

    # Valid values
    manager.warning_threshold = 0
    assert manager.warning_threshold == 0

    manager.warning_threshold = 100
    assert manager.warning_threshold == 100

    manager.warning_threshold = 50.5
    assert manager.warning_threshold == 50.5

    # Invalid values
    with pytest.raises(ValueError, match="must be between 0 and 100"):
        manager.warning_threshold = -1

    with pytest.raises(ValueError, match="must be between 0 and 100"):
        manager.warning_threshold = 101

    with pytest.raises(TypeError, match="must be a number"):
        manager.warning_threshold = "invalid"

def test_auto_clean_threshold_validation(tmp_path):
    """测试auto_clean_threshold验证"""
    temp_config = os.path.join(tmp_path, "test_config.json")
    manager = ConfigManager(temp_config)

    # Valid values
    manager.auto_clean_threshold = 0
    assert manager.auto_clean_threshold == 0

    manager.auto_clean_threshold = 100
    assert manager.auto_clean_threshold == 100

    # Invalid values
    with pytest.raises(ValueError, match="must be between 0 and 100"):
        manager.auto_clean_threshold = -1

    with pytest.raises(ValueError, match="must be between 0 and 100"):
        manager.auto_clean_threshold = 101

    with pytest.raises(TypeError, match="must be a number"):
        manager.auto_clean_threshold = "invalid"

def test_refresh_interval_validation(tmp_path):
    """测试refresh_interval验证"""
    temp_config = os.path.join(tmp_path, "test_config.json")
    manager = ConfigManager(temp_config)

    # Valid values
    manager.refresh_interval = 1
    assert manager.refresh_interval == 1

    manager.refresh_interval = 100
    assert manager.refresh_interval == 100

    # Invalid values
    with pytest.raises(ValueError, match="must be a positive integer"):
        manager.refresh_interval = 0

    with pytest.raises(ValueError, match="must be a positive integer"):
        manager.refresh_interval = -5

    with pytest.raises(TypeError, match="must be a number"):
        manager.refresh_interval = "invalid"

def test_auto_clean_validation(tmp_path):
    """测试auto_clean验证"""
    temp_config = os.path.join(tmp_path, "test_config.json")
    manager = ConfigManager(temp_config)

    # Valid values
    manager.auto_clean = True
    assert manager.auto_clean == True

    manager.auto_clean = False
    assert manager.auto_clean == False

    # Invalid values
    with pytest.raises(TypeError, match="must be a boolean"):
        manager.auto_clean = "true"

    with pytest.raises(TypeError, match="must be a boolean"):
        manager.auto_clean = 1

def test_corrupt_config_handling(tmp_path, caplog):
    """测试损坏配置文件的处理"""
    import logging
    temp_config = os.path.join(tmp_path, "test_config.json")

    # Write invalid JSON
    with open(temp_config, 'w') as f:
        f.write("{ invalid json }")

    # Should load defaults and log a warning
    with caplog.at_level(logging.WARNING):
        manager = ConfigManager(temp_config)
        assert manager.warning_threshold == 85
        assert "corrupt" in caplog.text.lower() or "invalid json" in caplog.text.lower()

def test_save_error_handling(tmp_path):
    """测试保存错误处理"""
    temp_config = os.path.join(tmp_path, "test_config.json")
    manager = ConfigManager(temp_config)

    # Try to save to a path that will fail (e.g., read-only filesystem simulation)
    # We can simulate this by using an invalid path
    original_path = manager.config_path
    manager.config_path = "/nonexistent/path/config.json"

    with pytest.raises(IOError):
        manager.save()

    # Restore original path
    manager.config_path = original_path
