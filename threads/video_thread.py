"""视频处理线程模块。"""

from PySide6.QtCore import QThread, Signal

from core.detector import ModelLoadError
from core.video_processor import VideoProcessor


class VideoThread(QThread):
    """视频检测线程。

    在线程中读取视频并执行 YOLO 检测，避免阻塞 GUI。
    """

    frame_ready = Signal(object, int, float)
    error_signal = Signal(str)
    finished_signal = Signal(str, str, int, float)

    def __init__(self, video_path: str = "") -> None:
        """初始化视频线程。"""
        super().__init__()
        self.video_path = video_path
        self.is_running = False
        self.processor = VideoProcessor()

    def run(self) -> None:
        """线程执行入口。"""
        self.is_running = True
        try:
            summary = self.processor.process_video(
                video_path=self.video_path,
                frame_callback=self._emit_frame,
                should_stop=lambda: not self.is_running,
            )
            output_path = str(summary.output_path) if summary.output_path else "-"
            self.finished_signal.emit(
                summary.status,
                output_path,
                summary.last_people_count,
                summary.last_fps,
            )
        except ModelLoadError as exc:
            self.error_signal.emit(str(exc))
            self.finished_signal.emit("error", "-", 0, 0.0)
        except Exception as exc:
            self.error_signal.emit(f"视频检测失败：{exc}")
            self.finished_signal.emit("error", "-", 0, 0.0)
        finally:
            self.is_running = False
            self.processor.release()

    def _emit_frame(self, frame, people_count: int, fps: float) -> None:
        """发送检测后的帧和统计数据到主线程。"""
        self.frame_ready.emit(frame, people_count, fps)

    def stop(self) -> None:
        """停止视频线程。"""
        self.is_running = False
