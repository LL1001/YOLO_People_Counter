# YOLO_People_Counter

YOLO_People_Counter 是一个基于 YOLOv8n 的实时人数统计课程展示项目。项目使用 Python、PySide6、OpenCV 和 ultralytics YOLO 开发，提供深色科技风桌面界面，支持图片、视频和摄像头三种人数统计模式。

本项目定位为课程作业和答辩演示，不包含商用系统中的 CSV 导出、人数超限告警、告警截图和告警日志等复杂功能。

## 功能特点

- 图片人数统计：选择本地图片后检测 person 类别，显示检测框、人数和 FPS，并保存结果图片。
- 视频人数统计：选择本地视频后在线程中逐帧检测，实时显示检测结果，并可保存检测后视频。
- 摄像头实时统计：打开默认摄像头，实时检测画面中的人数，每 3 帧执行一次 YOLO 检测。
- 科技风 GUI：左侧功能导航，中间大画面显示，右侧统计卡片，底部关键事件日志。
- 检测状态显示：支持未开始、检测中、已完成、已停止、出错等状态。
- 保存截图：可将当前中间画面保存到 `results/screenshots/`。
- 标准教室 demo 支持：可手动放置固定教室图片，并使用辅助工具标定每排座位区域。
- 稳定性增强：模型缺失、视频读取失败、摄像头打开失败等情况会给出友好提示。

## 技术栈

- Python
- PySide6
- OpenCV
- ultralytics YOLO
- YOLOv8n
- NumPy
- PyInstaller

## 项目结构

```text
YOLO_People_Counter/
├── main.py                    # 程序入口
├── config.py                  # 基础路径和资源路径配置
├── requirements.txt           # 项目依赖
├── build.bat                  # PyInstaller 打包命令
├── README.md                  # 项目说明
├── assets/
│   ├── qss/
│   │   └── dark_theme.qss     # 深色科技风样式
│   └── icons/                 # 图标资源目录
├── models/
│   └── yolov8n.pt             # 默认 YOLOv8n 模型
├── ui/
│   ├── main_window.py         # 主窗口和按钮事件
│   ├── video_widget.py        # 中间画面显示组件
│   ├── stats_panel.py         # 右侧统计卡片
│   └── log_table.py           # 底部日志表格
├── core/
│   ├── detector.py            # YOLO 模型加载和 person 检测
│   ├── image_processor.py     # 图片检测处理
│   ├── video_processor.py     # 视频检测处理
│   ├── camera_processor.py    # 摄像头检测处理
│   └── fps_monitor.py         # FPS 计算
├── threads/
│   ├── video_thread.py        # 视频检测线程
│   └── camera_thread.py       # 摄像头检测线程
├── tools/
│   └── row_calibrator.py      # 教室座位排区域标定辅助工具
├── utils/
│   ├── draw_utils.py          # 检测框绘制
│   ├── file_utils.py          # 文件和时间戳工具
│   └── logger.py              # 日志工具
├── results/
│   ├── images/                # 图片检测结果
│   ├── videos/                # 视频检测结果
│   └── screenshots/           # 手动保存截图
└── demo/
    ├── images/                # 演示图片，可放 classroom_standard.jpg
    └── videos/                # 演示视频
```

## 安装依赖

建议使用虚拟环境：

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## 运行程序

```bash
python main.py
```

运行前请确认默认模型文件存在：

```text
models/yolov8n.pt
```

如果模型文件不存在或无效，程序会弹窗提示，不会直接崩溃。

## 使用说明

1. 点击“图片检测”，选择 `jpg/jpeg/png/bmp` 图片，检测完成后结果保存到 `results/images/`。
2. 点击“视频检测”，选择 `mp4/avi/mov/mkv` 视频，检测过程在线程中运行，结果视频保存到 `results/videos/`。
3. 点击“摄像头检测”，打开默认 0 号摄像头并实时统计人数。
4. 点击“停止检测”，可停止正在运行的视频或摄像头检测。
5. 点击“保存截图”，将当前中间画面保存到 `results/screenshots/`。

同一时间只允许一种实时检测模式运行，避免视频和摄像头同时占用资源。

## 标准教室 Demo 图片

为了方便课程作业展示，可以准备一张固定教室视角图片作为标准样例。

放置方式：

1. 将标准教室图片命名为 `classroom_standard.jpg`。
2. 将图片放入 `demo/images/` 目录。
3. 最终路径应为：

```text
demo/images/classroom_standard.jpg
```

项目中已在 [config.py](config.py) 提供路径配置：

```python
DEMO_CLASSROOM_IMAGE_PATH = DEMO_IMAGES_DIR / "classroom_standard.jpg"
```

如果该图片不存在，主程序不会报错；需要使用教室展示或座位区域标定时，再手动添加即可。

## 座位区域配置

固定教室画面中的每一排座位区域可在 [config.py](config.py) 的 `CLASSROOM_ROWS` 中配置。坐标必须基于 `demo/images/classroom_standard.jpg` 的画面尺寸。

示例：

```python
CLASSROOM_ROWS = [
    {
        "name": "第1排",
        "area": (100, 220, 1120, 300),
        "capacity": 8,
    },
    {
        "name": "第2排",
        "area": (90, 320, 1130, 410),
        "capacity": 8,
    },
]
```

说明：

- `area` 表示该排座位区域的矩形坐标 `(x1, y1, x2, y2)`。
- `capacity` 需要根据实际教室每一排座位数量手动修改。
- 如果更换标准教室图片，或图片分辨率发生变化，需要重新调整 `CLASSROOM_ROWS` 坐标。

## 座位区域标定工具

项目提供一个简单的 OpenCV 标定辅助工具，仅用于开发和配置，不集成到主 GUI。

注意：该工具会打开 OpenCV 图形窗口，需要在本地 Windows 桌面环境运行。不要在无图形界面的远程环境、自动化环境或 Codex 工具环境中运行该脚本。

运行方式：

```bash
python tools/row_calibrator.py
```

使用方式：

1. 工具会打开 `demo/images/classroom_standard.jpg`。
2. 鼠标左键拖拽矩形，框选每一排座位区域。
3. 每次拖拽完成后，终端会输出该矩形坐标：`(x1, y1, x2, y2)`。
4. 支持连续框选多排座位。
5. 按 `s` 键输出 `CLASSROOM_ROWS` 示例格式。
6. 按 `q` 键退出标定工具。

如果 demo 图片不存在，工具会在终端给出友好提示：

```text
请手动将图片命名为 classroom_standard.jpg，并放入 demo/images/ 目录。
```

## 打包为 exe

在项目根目录执行：

```bat
build.bat
```

当前 `build.bat` 提供基础 PyInstaller 打包命令，后续可根据图标、模型和资源文件继续扩展。

## 课程展示建议

- 先展示主界面整体布局和右侧统计卡片。
- 使用一张人物图片演示图片人数统计。
- 使用一段短视频演示实时检测和停止检测。
- 使用摄像头演示实时人数统计和 FPS 变化。
- 最后演示“保存截图”和结果目录。

## 已裁剪功能

为保持课程展示简洁，本项目暂不实现：

- CSV 导出
- 人数超限告警
- 告警截图保存
- 告警日志
