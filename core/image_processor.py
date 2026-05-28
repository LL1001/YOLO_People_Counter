"""图片处理模块。"""

import time
from dataclasses import dataclass
from pathlib import Path

import cv2
import numpy as np

from config import RESULT_IMAGES_DIR, YOLOV8N_MODEL_PATH
from core.detector import Detector
from utils.draw_utils import draw_detection_boxes
from utils.file_utils import ensure_dir, generate_timestamp_filename


@dataclass
class ImageProcessResult:
    """图片检测处理结果。"""

    output_path: Path
    people_count: int
    fps: float
    annotated_image: np.ndarray


class ImageProcessor:
    """图片人数统计处理器。

    负责读取图片、调用检测器、绘制结果并保存到 results/images。
    """

    def __init__(self, detector: Detector | None = None) -> None:
        """初始化图片处理器。"""
        self.detector = detector or Detector(YOLOV8N_MODEL_PATH)

    def process_image(self, image_path: str | Path) -> ImageProcessResult:
        """处理单张图片并返回检测结果。"""
        source_path = Path(image_path)
        image = self._read_image(source_path)
        if image is None:
            raise ValueError(f"图片读取失败：{source_path}")

        start_time = time.perf_counter()
        detections = self.detector.detect_person(image)
        elapsed = max(time.perf_counter() - start_time, 1e-6)
        fps = 1.0 / elapsed

        annotated_image = draw_detection_boxes(image.copy(), detections)
        output_path = self._save_result_image(annotated_image, source_path)

        return ImageProcessResult(
            output_path=output_path,
            people_count=len(detections),
            fps=fps,
            annotated_image=annotated_image,
        )

    def _read_image(self, image_path: Path):
        """读取图片，兼容包含中文的 Windows 路径。"""
        try:
            image_bytes = np.fromfile(str(image_path), dtype=np.uint8)
            return cv2.imdecode(image_bytes, cv2.IMREAD_COLOR)
        except Exception:
            return None

    def _save_result_image(self, image, source_path: Path) -> Path:
        """保存检测结果图片，文件名带时间戳避免覆盖。"""
        output_dir = ensure_dir(RESULT_IMAGES_DIR)
        output_name = generate_timestamp_filename(source_path.stem, ".jpg")
        output_path = output_dir / output_name

        success, encoded_image = cv2.imencode(".jpg", image)
        if not success:
            raise RuntimeError("检测结果图片编码失败")
        encoded_image.tofile(str(output_path))
        return output_path
