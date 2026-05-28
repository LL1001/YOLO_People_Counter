# YOLO_People_Counter

YOLO_People_Counter 是一个基于 YOLO 的实时人数统计与智能监测系统，计划使用 Python、PySide6、OpenCV、ultralytics YOLO、YOLOv8n 和 PyInstaller 开发为 Windows 桌面软件。

## 功能规划

- 图片人数检测与结果保存
- 视频人数检测与结果保存
- 摄像头实时人数统计
- FPS 监控与显示
- 告警规则管理
- 检测日志记录
- CSV 结果导出
- PyInstaller 打包为 Windows exe

## 当前阶段

Phase 1 仅创建项目骨架，包含基础目录、配置文件、入口文件和模块占位代码。

本阶段暂不接入 YOLO，暂不实现图片、视频、摄像头检测，也暂不实现复杂 GUI。

## 运行方式

1. 创建并激活 Python 虚拟环境。
2. 安装依赖：

```bash
pip install -r requirements.txt
```

3. 启动程序：

```bash
python main.py
```

## 打包方式

在项目根目录执行：

```bat
build.bat
```

## 项目结构

```text
YOLO_People_Counter/
├── main.py
├── config.py
├── requirements.txt
├── build.bat
├── README.md
├── assets/
│   ├── qss/
│   │   └── dark_theme.qss
│   └── icons/
├── models/
│   └── yolov8n.pt
├── ui/
│   ├── main_window.py
│   ├── video_widget.py
│   ├── stats_panel.py
│   └── log_table.py
├── core/
│   ├── detector.py
│   ├── image_processor.py
│   ├── video_processor.py
│   ├── camera_processor.py
│   ├── alert_manager.py
│   └── fps_monitor.py
├── threads/
│   ├── video_thread.py
│   └── camera_thread.py
├── utils/
│   ├── csv_export.py
│   ├── draw_utils.py
│   ├── file_utils.py
│   └── logger.py
├── results/
│   ├── images/
│   ├── videos/
│   ├── screenshots/
│   └── csv/
└── demo/
    ├── images/
    └── videos/
```
