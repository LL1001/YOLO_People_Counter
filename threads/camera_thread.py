"""摄像头处理线程模块。"""

from PySide6.QtCore import QThread, Signal

from core.camera_processor import CameraProcessor
from core.detector import ModelLoadError


class CameraThread(QThread):
    """摄像头实时检测线程。

    在线程中打开摄像头并执行 YOLO 检测，避免阻塞 GUI。
    """

    frame_ready = Signal(object, int, float)
    error_signal = Signal(str)
    finished_signal = Signal(str, int, float)

    def __init__(self, camera_index: int = 0) -> None:
        """初始化摄像头线程。"""
        super().__init__()
        self.camera_index = camera_index
        self.is_running = False
        self.processor = CameraProcessor(camera_index=camera_index)

    def run(self) -> None:
        """线程执行入口。"""
        self.is_running = True
        try:
            summary = self.processor.process_camera(
                frame_callback=self._emit_frame,
                should_stop=lambda: not self.is_running,
            )
            self.finished_signal.emit(summary.status, summary.last_people_count, summary.last_fps)
        except ModelLoadError as exc:
            self.error_signal.emit(str(exc))
            self.finished_signal.emit("error", 0, 0.0)
        except Exception as exc:
            self.error_signal.emit(str(exc))
            status = "open_failed" if "摄像头打开失败" in str(exc) else "error"
            self.finished_signal.emit(status, 0, 0.0)
        finally:
            self.is_running = False
            self.processor.release()

    def _emit_frame(self, frame, people_count: int, fps: float) -> None:
        """发送检测画面和统计数据到主线程。"""
        self.frame_ready.emit(frame, people_count, fps)

    def stop(self) -> None:
        """停止摄像头线程。"""
        self.is_running = False
