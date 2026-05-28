"""主窗口模块。"""

from PySide6.QtWidgets import QLabel, QMainWindow


class MainWindow(QMainWindow):
    """软件主窗口占位类。

    Phase 1 只创建最基础窗口，复杂布局和交互留到后续阶段实现。
    """

    def __init__(self) -> None:
        """初始化主窗口。"""
        super().__init__()
        self.setWindowTitle("YOLO People Counter")
        self.resize(1200, 800)
        self._init_ui()

    def _init_ui(self) -> None:
        """初始化基础界面。"""
        label = QLabel("YOLO_People_Counter 项目骨架已创建")
        label.setStyleSheet("padding: 24px;")
        self.setCentralWidget(label)
