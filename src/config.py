# src/config.py
import json
import os

class ConfigManager:
    DEFAULT_CONFIG = {
        "warning_threshold": 85,
        "auto_clean": False,
        "auto_clean_threshold": 80,
        "refresh_interval": 5
    }

    def __init__(self, config_path="config.json"):
        self.config_path = config_path
        self._config = self._load_config()

    def _load_config(self):
        """加载配置文件，如果不存在则返回默认配置"""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    return {**self.DEFAULT_CONFIG, **json.load(f)}
            except (json.JSONDecodeError, IOError):
                return self.DEFAULT_CONFIG.copy()
        return self.DEFAULT_CONFIG.copy()

    @property
    def warning_threshold(self):
        return self._config.get("warning_threshold", 85)

    @property
    def auto_clean(self):
        return self._config.get("auto_clean", False)

    @property
    def auto_clean_threshold(self):
        return self._config.get("auto_clean_threshold", 80)

    @property
    def refresh_interval(self):
        return self._config.get("refresh_interval", 5)

    def save(self):
        """保存当前配置到文件"""
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self._config, f, indent=2, ensure_ascii=False)

    @warning_threshold.setter
    def warning_threshold(self, value):
        self._config["warning_threshold"] = value

    @auto_clean.setter
    def auto_clean(self, value):
        self._config["auto_clean"] = value

    @auto_clean_threshold.setter
    def auto_clean_threshold(self, value):
        self._config["auto_clean_threshold"] = value

    @refresh_interval.setter
    def refresh_interval(self, value):
        self._config["refresh_interval"] = value
