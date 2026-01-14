# tests/test_config.py
import pytest
import os
import json
import tempfile
from src.config import ConfigManager

def test_load_default_config():
    """测试加载默认配置"""
    manager = ConfigManager()
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
