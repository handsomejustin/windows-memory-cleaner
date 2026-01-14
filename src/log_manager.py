# src/log_manager.py
import json
import os
from datetime import datetime

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
        """
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
            except (json.JSONDecodeError, IOError):
                return []
        return []

    def _save_logs(self, logs):
        """保存日志到文件"""
        with open(self.log_file, 'w', encoding='utf-8') as f:
            json.dump(logs, f, indent=2, ensure_ascii=False)
