# Windows 内存清理工具实施计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 开发一个 Windows 托盘常驻工具，用于清理系统内存缓存，解决开发环境长时间运行后内存占用过高导致的卡顿问题。

**Architecture:** 三层架构 - 托盘界面层 (pystray/tkinter) + 业务逻辑层 (监控/清理/配置) + 数据访问层 (psutil/pywin32)。程序以后台托盘图标常驻，定时监控内存状态，用户可手动触发清理。

**Tech Stack:** Python 3.8+, pystray, psutil, pywin32, tkinter (内置), PyInstaller (打包)

---

## 前置准备

### Task 1: 项目初始化

**Files:**
- Create: `requirements.txt`
- Create: `src/__init__.py`
- Create: `config.json`
- Create: `logs/.gitkeep`
- Create: `icons/.gitkeep`

**Step 1: 创建项目结构和依赖文件**

```bash
# 创建目录结构
mkdir -p src logs icons docs/plans

# 创建 requirements.txt
cat > requirements.txt << 'EOF'
pystray>=0.19.5
psutil>=5.9.5
pywin32>=305
EOF
```

**Step 2: 创建空的 Python 包文件**

```bash
# 创建 src/__init__.py
touch src/__init__.py

# 创建占位文件
touch logs/.gitkeep
touch icons/.gitkeep
```

**Step 3: 创建默认配置文件**

```json
{
  "warning_threshold": 85,
  "auto_clean": false,
  "auto_clean_threshold": 80,
  "refresh_interval": 5
}
```

保存到: `config.json`

**Step 4: 安装依赖**

```bash
pip install -r requirements.txt
```

**Step 5: 初始化 Git 仓库并提交**

```bash
git init
git add .
git commit -m "chore: initialize project structure and dependencies"
```

---

## 核心模块开发

### Task 2: 实现配置管理模块

**Files:**
- Create: `src/config.py`
- Create: `tests/test_config.py`

**Step 1: 编写配置读取的失败测试**

```python
# tests/test_config.py
import pytest
import os
import json
from src.config import ConfigManager

def test_load_default_config():
    """测试加载默认配置"""
    manager = ConfigManager()
    assert manager.warning_threshold == 85
    assert manager.auto_clean == False
    assert manager.auto_clean_threshold == 80
    assert manager.refresh_interval == 5
```

**Step 2: 运行测试验证失败**

```bash
pytest tests/test_config.py::test_load_default_config -v
```

Expected: `ModuleNotFoundError: No module named 'src.config'`

**Step 3: 实现最小化的 ConfigManager 类**

```python
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
```

**Step 4: 运行测试验证通过**

```bash
pytest tests/test_config.py::test_load_default_config -v
```

Expected: PASS

**Step 5: 编写配置保存的测试**

```python
# tests/test_config.py 新增
import tempfile

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
```

**Step 6: 运行测试验证失败**

```bash
pytest tests/test_config.py::test_save_config -v
```

Expected: AttributeError (没有 save 方法)

**Step 7: 实现配置保存功能**

```python
# src/config.py 新增方法

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
```

**Step 8: 运行测试验证通过**

```bash
pytest tests/test_config.py -v
```

Expected: 全部 PASS

**Step 9: 提交**

```bash
git add src/config.py tests/test_config.py
git commit -m "feat: implement ConfigManager with load and save functionality"
```

---

### Task 3: 实现内存监控模块

**Files:**
- Create: `src/memory_monitor.py`
- Create: `tests/test_memory_monitor.py`

**Step 1: 编写获取内存信息的失败测试**

```python
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
```

**Step 2: 运行测试验证失败**

```bash
pytest tests/test_memory_monitor.py::test_get_memory_info -v
```

Expected: `ModuleNotFoundError: No module named 'src.memory_monitor'`

**Step 3: 实现最小化的 MemoryMonitor 类**

```python
# src/memory_monitor.py
import psutil

class MemoryMonitor:
    def get_memory_info(self):
        """
        获取系统内存信息

        Returns:
            dict: 包含 total(GB), used(GB), percent(%), available(GB)
        """
        mem = psutil.virtual_memory()

        return {
            "total": round(mem.total / (1024**3), 2),  # 转换为GB
            "used": round(mem.used / (1024**3), 2),
            "percent": round(mem.percent, 1),
            "available": round(mem.available / (1024**3), 2)
        }
```

**Step 4: 运行测试验证通过**

```bash
pytest tests/test_memory_monitor.py::test_get_memory_info -v
```

Expected: PASS

**Step 5: 编写阈值检测的测试**

```python
# tests/test_memory_monitor.py 新增

def test_check_threshold():
    """测试阈值检测"""
    monitor = MemoryMonitor()

    # 设置低阈值，应该不触发警告
    monitor.set_threshold(99)
    assert monitor.is_over_threshold() == False

    # 设置极低阈值，应该触发警告
    monitor.set_threshold(0)
    assert monitor.is_over_threshold() == True
```

**Step 6: 运行测试验证失败**

```bash
pytest tests/test_memory_monitor.py::test_check_threshold -v
```

Expected: AttributeError (没有相关方法)

**Step 7: 实现阈值检测功能**

```python
# src/memory_monitor.py 新增

class MemoryMonitor:
    def __init__(self):
        self._threshold = 85

    def set_threshold(self, percent):
        """设置警告阈值"""
        if not 0 <= percent <= 100:
            raise ValueError("阈值必须在 0-100 之间")
        self._threshold = percent

    def is_over_threshold(self):
        """检查当前内存是否超过阈值"""
        info = self.get_memory_info()
        return info["percent"] >= self._threshold
```

**Step 8: 运行测试验证通过**

```bash
pytest tests/test_memory_monitor.py -v
```

Expected: 全部 PASS

**Step 9: 提交**

```bash
git add src/memory_monitor.py tests/test_memory_monitor.py
git commit -m "feat: implement MemoryMonitor with memory info and threshold checking"
```

---

### Task 4: 实现内存清理模块

**Files:**
- Create: `src/memory_cleaner.py`
- Create: `tests/test_memory_cleaner.py`

**Step 1: 编写清理功能的测试**

```python
# tests/test_memory_cleaner.py
import pytest
from unittest.mock import patch, MagicMock
from src.memory_cleaner import MemoryCleaner

def test_clean_system_cache():
    """测试系统缓存清理"""
    cleaner = MemoryCleaner()

    # 模拟 Windows API 调用成功
    with patch('ctypes.windll.kernel32.SetProcessWorkingSetSize') as mock_api:
        mock_api.return_value = 1  # 返回成功

        result = cleaner.clean()

        # 验证返回结构
        assert "before" in result
        assert "after" in result
        assert "freed" in result
        assert "success" in result
        assert result["success"] == True
```

**Step 2: 运行测试验证失败**

```bash
pytest tests/test_memory_cleaner.py::test_clean_system_cache -v
```

Expected: `ModuleNotFoundError: No module named 'src.memory_cleaner'`

**Step 3: 实现 MemoryCleaner 类**

```python
# src/memory_cleaner.py
import ctypes
from src.memory_monitor import MemoryMonitor

class MemoryCleaner:
    def __init__(self):
        self.monitor = MemoryMonitor()
        self._kernel32 = ctypes.windll.kernel32

    def clean(self):
        """
        执行系统内存清理

        Returns:
            dict: 清理结果 {before, after, freed, success}
        """
        # 获取清理前的内存状态
        before = self.monitor.get_memory_info()

        try:
            # 调用 Windows API 清理系统缓存
            # SetProcessWorkingSetSize(-1, -1, -1) 会触发系统整理所有进程的工作集
            self._kernel32.SetProcessWorkingSetSize(-1, -1, -1)

            # 获取清理后的内存状态
            after = self.monitor.get_memory_info()

            # 计算释放的内存
            freed = round(before["used"] - after["used"], 2)

            return {
                "before": before,
                "after": after,
                "freed": max(0, freed),  # 确保不为负数
                "success": True
            }

        except Exception as e:
            return {
                "before": before,
                "after": before,
                "freed": 0,
                "success": False,
                "error": str(e)
            }
```

**Step 4: 运行测试验证通过**

```bash
pytest tests/test_memory_cleaner.py::test_clean_system_cache -v
```

Expected: PASS

**Step 5: 编写 API 调用失败的测试**

```python
# tests/test_memory_cleaner.py 新增

def test_clean_with_api_error():
    """测试 API 调用失败的情况"""
    cleaner = MemoryCleaner()

    # 模拟 API 抛出异常
    with patch('ctypes.windll.kernel32.SetProcessWorkingSetSize') as mock_api:
        mock_api.side_effect = Exception("API Error")

        result = cleaner.clean()

        assert result["success"] == False
        assert "error" in result
        assert result["freed"] == 0
```

**Step 6: 运行测试验证通过**

```bash
pytest tests/test_memory_cleaner.py::test_clean_with_api_error -v
```

Expected: PASS

**Step 7: 提交**

```bash
git add src/memory_cleaner.py tests/test_memory_cleaner.py
git commit -m "feat: implement MemoryCleaner with Windows API integration"
```

---

### Task 5: 实现日志管理模块

**Files:**
- Create: `src/log_manager.py`
- Create: `tests/test_log_manager.py`

**Step 1: 编写日志记录的测试**

```python
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
```

**Step 2: 运行测试验证失败**

```bash
pytest tests/test_log_manager.py::test_add_and_get_logs -v
```

Expected: `ModuleNotFoundError: No module named 'src.log_manager'`

**Step 3: 实现 LogManager 类**

```python
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
```

**Step 4: 运行测试验证通过**

```bash
pytest tests/test_log_manager.py::test_add_and_get_logs -v
```

Expected: PASS

**Step 5: 编写日志数量限制的测试**

```python
# tests/test_log_manager.py 新增

def test_log_limit(tmp_path):
    """测试日志数量限制"""
    log_file = os.path.join(tmp_path, "test_clean.log")
    manager = LogManager(log_file)

    # 添加超过限制的日志
    for i in range(110):
        manager.add_clean_log(80 + i, 70 + i, 1.0)

    logs = manager.get_recent_logs(limit=200)
    assert len(logs) == 100  # 应该只保留100条
```

**Step 6: 运行测试验证通过**

```bash
pytest tests/test_log_manager.py -v
```

Expected: 全部 PASS

**Step 7: 提交**

```bash
git add src/log_manager.py tests/test_log_manager.py
git commit -m "feat: implement LogManager with size limit and persistence"
```

---

### Task 6: 创建托盘应用

**Files:**
- Create: `src/tray_app.py`

**Step 1: 实现基础托盘应用**

```python
# src/tray_app.py
import pystray
import threading
from PIL import Image, ImageDraw
from src.memory_monitor import MemoryMonitor
from src.memory_cleaner import MemoryCleaner
from src.config import ConfigManager
from src.log_manager import LogManager

class MemoryTrayApp:
    def __init__(self):
        self.config = ConfigManager()
        self.monitor = MemoryMonitor()
        self.cleaner = MemoryCleaner()
        self.logger = LogManager()
        self.running = False

    def create_icon(self, color="green"):
        """创建托盘图标"""
        # 创建一个简单的内存条图标
        width, height = 64, 64
        image = Image.new('RGB', (width, height), color='white')
        draw = ImageDraw.Draw(image)

        # 绘制内存条
        colors = {
            "green": (0, 200, 0),
            "yellow": (255, 200, 0),
            "red": (255, 0, 0)
        }
        fill_color = colors.get(color, (0, 200, 0))

        # 绘制外框
        draw.rectangle([8, 16, 56, 48], outline=(100, 100, 100), width=2)

        # 绘制内存填充
        mem_info = self.monitor.get_memory_info()
        fill_height = int(28 * mem_info["percent"] / 100)
        if fill_height > 0:
            draw.rectangle([10, 47 - fill_height, 54, 46], fill=fill_color)

        return image

    def get_icon_color(self, percent):
        """根据内存使用率返回图标颜色"""
        if percent < 70:
            return "green"
        elif percent < 85:
            return "yellow"
        else:
            return "red"

    def update_tooltip(self):
        """更新托盘图标的悬浮提示"""
        mem_info = self.monitor.get_memory_info()
        return f"内存: {mem_info['used']}/{mem_info['total']}GB ({mem_info['percent']}%)"

    def on_clean(self, icon=None, item=None):
        """清理内存回调"""
        result = self.cleaner.clean()
        if result["success"]:
            self.logger.add_clean_log(
                before_percent=result["before"]["percent"],
                after_percent=result["after"]["percent"],
                freed_gb=result["freed"]
            )
            print(f"清理成功: 释放 {result['freed']}GB")
        else:
            print(f"清理失败: {result.get('error', '未知错误')}")
        self.update_icon_state()

    def on_quit(self, icon=None, item=None):
        """退出回调"""
        self.running = False
        icon.stop()

    def update_icon_state(self):
        """更新图标状态（颜色和提示）"""
        mem_info = self.monitor.get_memory_info()
        color = self.get_icon_color(mem_info["percent"])
        self.icon.icon = self.create_icon(color)
        self.icon.title = self.update_tooltip()

    def run(self):
        """启动托盘应用"""
        self.running = True

        # 创建菜单
        menu = pystray.Menu(
            pystray.MenuItem("显示内存状态", self.on_show_status),
            pystray.MenuItem("立即清理内存", self.on_clean),
            pystray.MenuItem("退出", self.on_quit)
        )

        # 创建图标
        mem_info = self.monitor.get_memory_info()
        initial_color = self.get_icon_color(mem_info["percent"])
        self.icon = pystray.Icon(
            "memory_cleaner",
            self.create_icon(initial_color),
            menu=menu,
            title=self.update_tooltip()
        )

        # 启动图标
        self.icon.run()

    def on_show_status(self, icon=None, item=None):
        """显示状态窗口"""
        print(self.update_tooltip())
        logs = self.logger.get_recent_logs(limit=5)
        print("\n最近清理记录:")
        for log in logs[-5:]:
            print(f"  {log['timestamp']}: {log['before_percent']}% -> {log['after_percent']}%, 释放 {log['freed']}GB")

if __name__ == "__main__":
    app = MemoryTrayApp()
    app.run()
```

**Step 2: 更新 requirements.txt 添加 PIL**

```bash
# requirements.txt 添加:
Pillow>=10.0.0
```

**Step 3: 安装新依赖并测试**

```bash
pip install -r requirements.txt
python src/tray_app.py
```

手动测试：
- 右键菜单是否正常
- 点击"立即清理内存"是否有输出
- 点击"退出"是否正常退出

**Step 4: 提交**

```bash
git add src/tray_app.py requirements.txt
git commit -m "feat: implement system tray application with menu"
```

---

### Task 7: 创建状态窗口

**Files:**
- Create: `src/status_window.py`

**Step 1: 实现状态窗口**

```python
# src/status_window.py
import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
from src.memory_monitor import MemoryMonitor
from src.memory_cleaner import MemoryCleaner
from src.log_manager import LogManager

class StatusWindow:
    def __init__(self, on_clean_callback):
        self.on_clean_callback = on_clean_callback
        self.monitor = MemoryMonitor()
        self.logger = LogManager()
        self.window = None
        self.updating = False

    def show(self):
        """显示状态窗口"""
        if self.window and self.window.winfo_exists():
            self.window.lift()
            return

        self.window = tk.Tk()
        self.window.title("内存清理工具")
        self.window.geometry("400x350")
        self.window.resizable(False, False)

        self._create_widgets()
        self._update_display()

        # 关闭窗口时隐藏而非退出
        self.window.protocol("WM_DELETE_WINDOW", self.hide)

        # 启动自动刷新
        self._start_update_timer()

    def hide(self):
        """隐藏窗口"""
        if self.window:
            self.window.withdraw()

    def _create_widgets(self):
        """创建界面组件"""
        # 标题
        title_label = tk.Label(
            self.window,
            text="内存使用状态",
            font=("Microsoft YaHei", 14, "bold")
        )
        title_label.pack(pady=10)

        # 内存信息框架
        info_frame = ttk.LabelFrame(self.window, text="当前状态", padding=10)
        info_frame.pack(fill="x", padx=15, pady=5)

        # 内存使用率进度条
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            info_frame,
            variable=self.progress_var,
            maximum=100,
            length=350,
            mode='determinate'
        )
        self.progress_bar.pack(pady=5)

        # 详细信息标签
        self.info_label = tk.Label(
            info_frame,
            text="加载中...",
            font=("Microsoft YaHei", 10)
        )
        self.info_label.pack(pady=5)

        # 清理按钮
        clean_btn = ttk.Button(
            self.window,
            text="立即清理内存",
            command=self._on_clean
        )
        clean_btn.pack(pady=10)

        # 最近记录框架
        log_frame = ttk.LabelFrame(self.window, text="最近清理记录", padding=10)
        log_frame.pack(fill="both", expand=True, padx=15, pady=5)

        # 日志文本框
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            height=8,
            font=("Consolas", 9),
            state='disabled'
        )
        self.log_text.pack(fill="both", expand=True)

    def _update_display(self):
        """更新显示内容"""
        # 获取内存信息
        mem_info = self.monitor.get_memory_info()

        # 更新进度条
        self.progress_var.set(mem_info["percent"])

        # 更新颜色
        style = ttk.Style()
        if mem_info["percent"] < 70:
            color = "green"
        elif mem_info["percent"] < 85:
            color = "yellow"
        else:
            color = "red"

        # 更新信息标签
        self.info_label.config(
            text=f"已用: {mem_info['used']} GB / {mem_info['total']} GB ({mem_info['percent']}%)"
        )

        # 更新日志
        self._update_logs()

    def _update_logs(self):
        """更新日志显示"""
        self.log_text.config(state='normal')
        self.log_text.delete(1.0, tk.END)

        logs = self.logger.get_recent_logs(limit=10)
        if not logs:
            self.log_text.insert(tk.END, "暂无清理记录")
        else:
            for log in reversed(logs):
                timestamp = log['timestamp'][:19]  # 去掉毫秒
                line = f"[{timestamp}] {log['before_percent']}% -> {log['after_percent']}%, 释放 {log['freed']}GB\n"
                self.log_text.insert(tk.END, line)

        self.log_text.config(state='disabled')

    def _on_clean(self):
        """清理按钮回调"""
        result = self.on_clean_callback()
        self._update_display()

    def _start_update_timer(self):
        """启动定时更新"""
        if self.window and self.window.winfo_exists():
            self._update_display()
            self.window.after(3000, self._start_update_timer)  # 每3秒更新
```

**Step 2: 更新 tray_app.py 集成状态窗口**

```python
# src/tray_app.py 修改

from src.status_window import StatusWindow

class MemoryTrayApp:
    def __init__(self):
        # ... 现有代码 ...
        self.status_window = None

    def run(self):
        """启动托盘应用"""
        self.running = True
        self.status_window = StatusWindow(self.on_clean_with_update)

        # 创建菜单
        menu = pystray.Menu(
            pystray.MenuItem("显示内存状态", self.on_show_status),
            pystray.MenuItem("立即清理内存", self.on_clean),
            pystray.MenuItem("退出", self.on_quit)
        )

        # ... 其余代码 ...

    def on_show_status(self, icon=None, item=None):
        """显示状态窗口"""
        if self.status_window:
            self.status_window.show()

    def on_clean_with_update(self):
        """清理并返回结果（供状态窗口调用）"""
        result = self.cleaner.clean()
        if result["success"]:
            self.logger.add_clean_log(
                before_percent=result["before"]["percent"],
                after_percent=result["after"]["percent"],
                freed_gb=result["freed"]
            )
            self.update_icon_state()
        return result
```

**Step 3: 测试状态窗口**

```bash
python src/tray_app.py
```

测试：
- 右键菜单选择"显示内存状态"
- 窗口是否正常显示
- 进度条和内存信息是否正确
- 点击"立即清理内存"是否有效

**Step 4: 提交**

```bash
git add src/status_window.py src/tray_app.py
git commit -m "feat: add status window with memory display and clean history"
```

---

### Task 8: 创建主入口文件

**Files:**
- Create: `main.py`

**Step 1: 创建主入口**

```python
# main.py
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Windows 内存清理工具
用于清理系统内存缓存，解决长时间运行后内存占用过高的问题
"""

import sys
import os

# 添加 src 目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.tray_app import MemoryTrayApp

def main():
    """主入口函数"""
    print("Windows 内存清理工具启动中...")
    app = MemoryTrayApp()
    app.run()

if __name__ == "__main__":
    main()
```

**Step 2: 测试主入口**

```bash
python main.py
```

**Step 3: 提交**

```bash
git add main.py
git commit -m "feat: add main entry point"
```

---

## 打包与部署

### Task 9: PyInstaller 打包配置

**Files:**
- Create: `clean_mem.spec`

**Step 1: 创建 PyInstaller 规格文件**

```python
# clean_mem.spec
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('config.json', '.'), ('icons', 'icons')],
    hiddenimports=[
        'pystray',
        'PIL._tkinter_finder',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='clean_mem',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # 不显示控制台窗口
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icons/app.ico',  # 需要准备图标文件
)
```

**Step 2: 准备图标文件**

创建或下载一个简单的图标文件保存到 `icons/app.ico`

**Step 3: 打包测试**

```bash
pip install pyinstaller
pyinstaller clean_mem.spec
```

**Step 4: 测试打包后的 exe**

运行 `dist/clean_mem.exe` 验证功能

**Step 5: 提交**

```bash
git add clean_mem.spec
git commit -m "build: add PyInstaller spec file for packaging"
```

---

## 文档完善

### Task 10: 编写 README 文档

**Files:**
- Create: `README.md`

**Step 1: 创建 README**

```markdown
# Windows 内存清理工具

一个简洁的 Windows 托盘常驻工具，用于清理系统内存缓存。

## 功能特点

- 托盘常驻，不占用任务栏空间
- 实时显示内存使用状态
- 一键清理系统缓存
- 保留清理历史记录
- 完全本地运行，无网络请求

## 使用方法

### 从源码运行

```bash
pip install -r requirements.txt
python main.py
```

### 使用打包版本

直接运行 `clean_mem.exe` 即可。

## 配置

编辑 `config.json` 可以自定义配置：

```json
{
  "warning_threshold": 85,      // 警告阈值
  "auto_clean": false,           // 自动清理（未实现）
  "auto_clean_threshold": 80,    // 自动清理阈值
  "refresh_interval": 5          // 刷新间隔（秒）
}
```

## 技术栈

- Python 3.8+
- pystray - 托盘图标
- psutil - 系统信息
- pywin32 - Windows API
- tkinter - 状态窗口

## 许可

MIT License
```

**Step 2: 提交**

```bash
git add README.md
git commit -m "docs: add README documentation"
```

---

## 完成检查

### Task 11: 最终验证

**Step 1: 运行所有测试**

```bash
pytest tests/ -v
```

**Step 2: 手动功能验证清单**

- [ ] 托盘图标正常显示
- [ ] 图标颜色根据内存使用率变化
- [ ] 悬浮提示显示正确的内存信息
- [ ] 右键菜单正常工作
- [ ] 点击"显示内存状态"打开窗口
- [ ] 状态窗口显示正确的内存信息
- [ ] 点击"立即清理内存"成功清理
- [ ] 清理日志正确记录
- [ ] 点击"退出"正常退出程序

**Step 3: 打包测试**

```bash
pyinstaller clean_mem.spec --onefile
# 运行 dist/clean_mem.exe 进行测试
```

**Step 4: 最终提交**

```bash
git add .
git commit -m "chore: final polish and testing complete"
```

---

## 总结

完成以上所有任务后，你将拥有一个功能完整的 Windows 内存清理工具，包括：

1. 完整的单元测试覆盖
2. 托盘常驻应用
3. 内存监控和清理功能
4. 可视化状态窗口
5. 日志记录功能
6. 可打包的 exe 文件

总提交数预计: ~15 commits
