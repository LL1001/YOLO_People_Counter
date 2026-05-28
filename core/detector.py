"""YOLO 检测器模块。"""


class Detector:
    """检测器占位类。

    Phase 1 暂不加载 YOLO 模型，后续阶段再接入 ultralytics。
    """

    def __init__(self, model_path: str) -> None:
        """保存模型路径配置。"""
        self.model_path = model_path

    def detect(self, image):
        """检测图片占位方法。"""
        # 本阶段不执行检测，返回空结果。
        _ = image
        return []
