# src/log_manager.py
import json
import logging
import os
from datetime import datetime

logger = logging.getLogger(__name__)

class LogManager:
    MAX_LOGS = 100  # 最多保留100条日志

    def __init__(self, log_file="logs/clean.log"):
        self.log_file = log_file
        self._ensure_dir()

    def _ensure_dir(self):
        """确保日志目录存在"""
        log_dir = os.path.dirname(self.log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)

    def add_clean_log(self, before_percent, after_percent, freed_gb):
        """
        添加一条清理日志

        Args:
            before_percent: 清理前内存使用率
            after_percent: 清理后内存使用率
            freed_gb: 释放的内存大小(GB)

        Raises:
            ValueError: 如果参数值无效
            TypeError: 如果参数类型无效
        """
        # Validate inputs
        if not isinstance(before_percent, (int, float)):
            raise TypeError(f"before_percent must be a number, got {type(before_percent).__name__}")
        if not isinstance(after_percent, (int, float)):
            raise TypeError(f"after_percent must be a number, got {type(after_percent).__name__}")
        if not isinstance(freed_gb, (int, float)):
            raise TypeError(f"freed_gb must be a number, got {type(freed_gb).__name__}")

        if not (0 <= before_percent <= 100):
            raise ValueError(f"before_percent must be between 0 and 100, got {before_percent}")
        if not (0 <= after_percent <= 100):
            raise ValueError(f"after_percent must be between 0 and 100, got {after_percent}")
        if freed_gb < 0:
            raise ValueError(f"freed_gb must be non-negative, got {freed_gb}")

        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "before_percent": before_percent,
            "after_percent": after_percent,
            "freed_gb": round(freed_gb, 2)
        }

        # 读取现有日志
        logs = self._load_logs()
        logs.append(log_entry)

        # 限制日志数量
        if len(logs) > self.MAX_LOGS:
            logs = logs[-self.MAX_LOGS:]

        # 保存日志
        self._save_logs(logs)

    def get_recent_logs(self, limit=10):
        """获取最近的日志"""
        logs = self._load_logs()
        return logs[-limit:] if logs else []

    def _load_logs(self):
        """加载日志文件"""
        if os.path.exists(self.log_file):
            try:
                with open(self.log_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError as e:
                logger.warning(f"Failed to decode JSON from log file {self.log_file}: {e}")
                return []
            except IOError as e:
                logger.warning(f"Failed to read log file {self.log_file}: {e}")
                return []
        return []

    def _save_logs(self, logs):
        """保存日志到文件"""
        try:
            with open(self.log_file, 'w', encoding='utf-8') as f:
                json.dump(logs, f, indent=2, ensure_ascii=False)
        except IOError as e:
            logger.error(f"Failed to write log file {self.log_file}: {e}")
            raise
