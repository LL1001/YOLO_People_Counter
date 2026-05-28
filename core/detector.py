"""YOLO 检测器模块。"""

import os
from pathlib import Path

from config import RESULTS_DIR


class ModelLoadError(RuntimeError):
    """模型加载失败异常，用于向界面返回友好提示。"""


class Detector:
    """YOLO person 检测器。

    封装 person 类别检测，供图片和视频处理复用。
    """

    PERSON_CLASS_ID = 0
    _model_cache: dict[Path, object] = {}

    def __init__(self, model_path: str | Path) -> None:
        """初始化检测器并保存模型路径。"""
        self.model_path = Path(model_path)
        self.model = self._model_cache.get(self.model_path)

    def load_model(self) -> None:
        """加载 YOLO 模型。

        Raises:
            ModelLoadError: 模型文件不存在、为空或 ultralytics 加载失败。
        """
        if self.model is not None:
            return

        if not self.model_path.exists():
            raise ModelLoadError(f"模型文件不存在：{self.model_path}")
        if self.model_path.stat().st_size == 0:
            raise ModelLoadError(f"模型文件为空，请放入有效的 YOLOv8n 模型：{self.model_path}")

        try:
            # 指定 ultralytics 配置目录，避免受限环境写入系统用户目录失败。
            yolo_config_dir = RESULTS_DIR / "ultralytics"
            yolo_config_dir.mkdir(parents=True, exist_ok=True)
            os.environ.setdefault("YOLO_CONFIG_DIR", str(yolo_config_dir))

            from ultralytics import YOLO

            self.model = YOLO(str(self.model_path))
            self._model_cache[self.model_path] = self.model
        except Exception as exc:
            raise ModelLoadError(f"YOLO 模型加载失败：{exc}") from exc

    def detect_person(self, image) -> list[dict]:
        """检测图片中的 person 类别。

        Args:
            image: OpenCV 读取的 BGR 图片。

        Returns:
            person 检测结果列表，每项包含检测框、置信度和类别名称。
        """
        self.load_model()

        try:
            results = self.model(image, classes=[self.PERSON_CLASS_ID], verbose=False)
        except Exception as exc:
            raise RuntimeError(f"YOLO 检测失败：{exc}") from exc

        detections: list[dict] = []
        if not results:
            return detections

        boxes = results[0].boxes
        if boxes is None:
            return detections

        for box in boxes:
            class_id = int(box.cls[0].item())
            if class_id != self.PERSON_CLASS_ID:
                continue

            x1, y1, x2, y2 = box.xyxy[0].tolist()
            confidence = float(box.conf[0].item())
            detections.append(
                {
                    "box": (int(x1), int(y1), int(x2), int(y2)),
                    "confidence": confidence,
                    "class_id": class_id,
                    "class_name": "person",
                }
            )

        return detections
