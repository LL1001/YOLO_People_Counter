"""摄像头处理线程模块。"""

from PySide6.QtCore import QThread, Signal


class CameraThread(QThread):
    """摄像头处理线程占位类。

    后续阶段将在此线程中读取摄像头画面，避免阻塞 GUI。
    """

    frame_ready = Signal(object)
    finished_signal = Signal()

    def __init__(self, camera_index: int = 0) -> None:
        """初始化摄像头线程。"""
        super().__init__()
        self.camera_index = camera_index
        self.is_running = False

    def run(self) -> None:
        """线程执行入口占位方法。"""
        # Phase 1 暂不读取摄像头。
        self.is_running = True
        self.is_running = False
        self.finished_signal.emit()

    def stop(self) -> None:
        """停止摄像头线程。"""
        self.is_running = False
