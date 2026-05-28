"""视频处理线程模块。"""

from PySide6.QtCore import QThread, Signal


class VideoThread(QThread):
    """视频处理线程占位类。

    后续阶段将在此线程中读取视频，避免阻塞 GUI。
    """

    frame_ready = Signal(object)
    finished_signal = Signal()

    def __init__(self, video_path: str = "") -> None:
        """初始化视频线程。"""
        super().__init__()
        self.video_path = video_path
        self.is_running = False

    def run(self) -> None:
        """线程执行入口占位方法。"""
        # Phase 1 暂不处理视频帧。
        self.is_running = True
        self.is_running = False
        self.finished_signal.emit()

    def stop(self) -> None:
        """停止视频线程。"""
        self.is_running = False
