# src/config.py
import json
import os
import logging

logger = logging.getLogger(__name__)

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
            except json.JSONDecodeError as e:
                logger.warning(f"Config file {self.config_path} is corrupt (invalid JSON). Using default configuration. Error: {e}")
                return self.DEFAULT_CONFIG.copy()
            except IOError as e:
                logger.warning(f"Failed to read config file {self.config_path}. Using default configuration. Error: {e}")
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
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self._config, f, indent=2, ensure_ascii=False)
        except IOError as e:
            logger.error(f"Failed to save config to {self.config_path}. Error: {e}")
            raise

    @warning_threshold.setter
    def warning_threshold(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("warning_threshold must be a number")
        if not 0 <= value <= 100:
            raise ValueError("warning_threshold must be between 0 and 100")
        self._config["warning_threshold"] = value

    @auto_clean.setter
    def auto_clean(self, value):
        if not isinstance(value, bool):
            raise TypeError("auto_clean must be a boolean")
        self._config["auto_clean"] = value

    @auto_clean_threshold.setter
    def auto_clean_threshold(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("auto_clean_threshold must be a number")
        if not 0 <= value <= 100:
            raise ValueError("auto_clean_threshold must be between 0 and 100")
        self._config["auto_clean_threshold"] = value

    @refresh_interval.setter
    def refresh_interval(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("refresh_interval must be a number")
        if value <= 0:
            raise ValueError("refresh_interval must be a positive integer")
        self._config["refresh_interval"] = value
