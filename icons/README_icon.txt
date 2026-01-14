Icon File Placeholder
=====================

The PyInstaller spec file (clean_mem.spec) references 'icons/app.ico' as the application icon.

To use a custom icon:
1. Create or convert an image to .ico format
2. Save it as 'icons/app.ico'
3. Rebuild the application with PyInstaller

For now, PyInstaller will use its default icon if app.ico is not found.

Recommended icon sizes:
- 16x16, 32x32, 48x48, 256x256 (for best compatibility)
