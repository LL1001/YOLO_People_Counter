"""统计面板模块。"""

from PySide6.QtWidgets import QLabel, QWidget, QVBoxLayout


class StatsPanel(QWidget):
    """人数统计与状态信息面板占位类。"""

    def __init__(self) -> None:
        """初始化统计面板。"""
        super().__init__()
        self.count_label = QLabel("人数：0")
        self.fps_label = QLabel("FPS：0")
        self._init_ui()

    def _init_ui(self) -> None:
        """初始化基础布局。"""
        layout = QVBoxLayout(self)
        layout.addWidget(self.count_label)
        layout.addWidget(self.fps_label)

    def update_stats(self, people_count: int, fps: float) -> None:
        """更新统计数据占位方法。"""
        self.count_label.setText(f"人数：{people_count}")
        self.fps_label.setText(f"FPS：{fps:.2f}")
