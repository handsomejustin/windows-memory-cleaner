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

### 打包

```bash
pip install pyinstaller
pyinstaller clean_mem.spec
```

打包后的可执行文件位于 `dist/clean_mem.exe`。

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
- Pillow - 图标绘制

## 许可

MIT License
