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
