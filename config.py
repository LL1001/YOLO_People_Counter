"""项目基础配置模块。

本阶段仅维护路径配置，暂不接入 YOLO 检测逻辑。
"""

import sys
from pathlib import Path


def resource_path(relative_path: str | Path) -> Path:
    """获取资源文件路径，兼容源码运行和 PyInstaller exe 运行。

    Args:
        relative_path: 相对于项目根目录或 PyInstaller 临时目录的路径。

    Returns:
        资源文件的绝对路径。
    """
    if hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS) / relative_path
    return Path(__file__).resolve().parent / relative_path


# 项目根目录
BASE_DIR = resource_path("")

# 资源目录
ASSETS_DIR = BASE_DIR / "assets"
QSS_DIR = ASSETS_DIR / "qss"
ICONS_DIR = ASSETS_DIR / "icons"

# 模型目录与默认模型路径
MODELS_DIR = BASE_DIR / "models"
YOLOV8N_MODEL_PATH = MODELS_DIR / "yolov8n.pt"

# 结果保存目录
RESULTS_DIR = BASE_DIR / "results"
RESULT_IMAGES_DIR = RESULTS_DIR / "images"
RESULT_VIDEOS_DIR = RESULTS_DIR / "videos"
RESULT_SCREENSHOTS_DIR = RESULTS_DIR / "screenshots"
RESULT_CSV_DIR = RESULTS_DIR / "csv"

# 演示数据目录
DEMO_DIR = BASE_DIR / "demo"
DEMO_IMAGES_DIR = DEMO_DIR / "images"
DEMO_VIDEOS_DIR = DEMO_DIR / "videos"

# 标准教室演示图片路径，需要手动放置 classroom_standard.jpg。
DEMO_CLASSROOM_IMAGE_PATH = DEMO_IMAGES_DIR / "classroom_standard.jpg"

# 教室每排座位区域配置，坐标基于 classroom_standard.jpg 的画面尺寸。
# 使用 tools/row_calibrator.py 辅助框选 area 后，再手动填写 capacity。
CLASSROOM_ROWS = [
    # 示例：
    # {
    #     "name": "第1排",
    #     "area": (100, 220, 1120, 300),
    #     "capacity": 8,
    # },
]
