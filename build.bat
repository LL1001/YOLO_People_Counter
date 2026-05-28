@echo off
REM 基础 PyInstaller 打包命令，后续阶段可按资源文件和图标继续完善。
pyinstaller --noconfirm --onefile --windowed --name YOLO_People_Counter main.py
pause
