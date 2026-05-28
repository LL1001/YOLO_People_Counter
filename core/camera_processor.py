"""摄像头处理模块。"""

from dataclasses import dataclass
from typing import Callable

import cv2

from config import YOLOV8N_MODEL_PATH
from core.detector import Detector
from core.fps_monitor import FPSMonitor
from utils.draw_utils import draw_detection_boxes


@dataclass
class CameraProcessSummary:
    """摄像头检测处理摘要。"""

    status: str
    last_people_count: int
    last_fps: float


class CameraProcessor:
    """摄像头人数统计处理器。

    负责摄像头读取、检测帧控制和资源释放，不直接操作 GUI。
    """

    def __init__(
        self,
        camera_index: int = 0,
        detector: Detector | None = None,
        detect_interval: int = 3,
    ) -> None:
        """初始化摄像头处理器。"""
        self.camera_index = camera_index
        self.detector = detector or Detector(YOLOV8N_MODEL_PATH)
        self.detect_interval = max(1, detect_interval)
        self.capture = None
        self.fps_monitor = FPSMonitor()

    def process_camera(
        self,
        frame_callback: Callable[[object, int, float], None],
        should_stop: Callable[[], bool],
    ) -> CameraProcessSummary:
        """循环读取摄像头画面并执行实时人数统计。"""
        self.capture = cv2.VideoCapture(self.camera_index, cv2.CAP_DSHOW)
        if not self.capture.isOpened():
            self.release()
            raise ValueError(f"摄像头打开失败：无法打开编号为 {self.camera_index} 的摄像头")

        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        frame_index = 0
        last_detections: list[dict] = []
        last_people_count = 0
        last_fps = 0.0
        status = "stopped"
        self.fps_monitor.reset()

        while not should_stop():
            success, frame = self.capture.read()
            if not success:
                status = "open_failed"
                break

            if frame_index % self.detect_interval == 0:
                last_detections = self.detector.detect_person(frame)
                last_people_count = len(last_detections)

            annotated_frame = draw_detection_boxes(frame.copy(), last_detections)
            last_fps = self.fps_monitor.update()
            frame_callback(annotated_frame, last_people_count, last_fps)
            frame_index += 1

        self.release()
        return CameraProcessSummary(
            status=status,
            last_people_count=last_people_count,
            last_fps=last_fps,
        )

    def release(self) -> None:
        """释放摄像头资源。"""
        if self.capture is not None:
            self.capture.release()
            self.capture = None
