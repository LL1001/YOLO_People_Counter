"""视频处理模块。"""

from dataclasses import dataclass
from pathlib import Path
from typing import Callable

import cv2

from config import RESULT_VIDEOS_DIR, YOLOV8N_MODEL_PATH
from core.detector import Detector
from core.fps_monitor import FPSMonitor
from utils.draw_utils import draw_detection_boxes
from utils.file_utils import ensure_dir, generate_timestamp_filename


@dataclass
class VideoProcessSummary:
    """视频检测处理摘要。"""

    status: str
    output_path: Path | None
    last_people_count: int
    last_fps: float


class VideoProcessor:
    """视频人数统计处理器。

    负责读取视频、逐帧调用 YOLO、绘制结果、可选保存结果视频。
    该类不直接操作 GUI。
    """

    def __init__(self, detector: Detector | None = None, save_output: bool = True) -> None:
        """初始化视频处理器。"""
        self.detector = detector or Detector(YOLOV8N_MODEL_PATH)
        self.save_output = save_output
        self.capture = None
        self.writer = None
        self.output_path: Path | None = None
        self.fps_monitor = FPSMonitor()

    def process_video(
        self,
        video_path: str | Path,
        frame_callback: Callable[[object, int, float], None],
        should_stop: Callable[[], bool],
    ) -> VideoProcessSummary:
        """逐帧处理视频并通过回调返回检测结果帧。"""
        source_path = Path(video_path)
        self.capture = cv2.VideoCapture(str(source_path))
        if not self.capture.isOpened():
            self.release()
            raise ValueError(f"视频打开失败：{source_path}")

        self._prepare_writer(source_path)
        self.fps_monitor.reset()
        last_people_count = 0
        last_fps = 0.0
        status = "completed"

        while not should_stop():
            success, frame = self.capture.read()
            if not success:
                break

            detections = self.detector.detect_person(frame)
            annotated_frame = draw_detection_boxes(frame.copy(), detections)
            last_people_count = len(detections)
            last_fps = self.fps_monitor.update()

            if self.writer is not None:
                self.writer.write(annotated_frame)

            frame_callback(annotated_frame, last_people_count, last_fps)

        if should_stop():
            status = "stopped"

        self.release()
        return VideoProcessSummary(
            status=status,
            output_path=self.output_path,
            last_people_count=last_people_count,
            last_fps=last_fps,
        )

    def _prepare_writer(self, source_path: Path) -> None:
        """创建视频保存器，保存到 results/videos。"""
        if not self.save_output or self.capture is None:
            return

        output_dir = ensure_dir(RESULT_VIDEOS_DIR)
        output_name = generate_timestamp_filename(source_path.stem, ".mp4")
        self.output_path = output_dir / output_name

        width = int(self.capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        source_fps = self.capture.get(cv2.CAP_PROP_FPS)
        if source_fps <= 0:
            source_fps = 25.0

        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        self.writer = cv2.VideoWriter(str(self.output_path), fourcc, source_fps, (width, height))
        if not self.writer.isOpened():
            self.writer = None
            self.output_path = None

    def release(self) -> None:
        """释放视频读取和保存资源。"""
        if self.capture is not None:
            self.capture.release()
            self.capture = None
        if self.writer is not None:
            self.writer.release()
            self.writer = None
