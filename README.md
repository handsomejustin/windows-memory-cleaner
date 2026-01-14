# Windows 内存清理工具

一个简洁的 Windows 托盘常驻工具，用于清理系统内存缓存。

## 系统要求

- Windows 10 或更高版本
- Python 3.8+
- 建议以管理员权限运行以获得最佳清理效果

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

### 打包

```bash
pip install pyinstaller
pyinstaller clean_mem.spec
```

打包后的可执行文件位于 `dist/clean_mem.exe`。

## 测试

运行测试套件：

```bash
pytest tests/
```

## 配置

编辑 `config.json` 可以自定义配置：

| 配置项 | 说明 |
|--------|------|
| warning_threshold | 警告阈值 (默认: 85) |
| auto_clean | 自动清理开关，暂未实现 (默认: false) |
| auto_clean_threshold | 自动清理阈值 (默认: 80) |
| refresh_interval | 状态刷新间隔，单位秒 (默认: 5) |

## 技术栈

- Python 3.8+
- pystray - 托盘图标
- psutil - 系统信息
- pywin32 - Windows API
- tkinter - 状态窗口
- Pillow - 图标绘制

## 许可

MIT License
