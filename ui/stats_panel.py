"""右侧统计卡片模块。"""

from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout, QWidget


class StatsPanel(QWidget):
    """人数统计与运行状态面板。

    用于课程展示时呈现核心指标：人数、FPS、模式和检测状态。
    """

    def __init__(self) -> None:
        """初始化统计面板。"""
        super().__init__()
        self.setObjectName("statsPanel")
        self.people_value = QLabel("0")
        self.fps_value = QLabel("0.00")
        self.mode_value = QLabel("未选择")
        self.status_value = QLabel("未开始")
        self.people_value.setProperty("metric", "people")
        self.fps_value.setProperty("metric", "fps")
        self.mode_value.setProperty("metric", "mode")
        self.status_value.setProperty("metric", "status")
        self.status_value.setProperty("status", "未开始")
        self._init_ui()

    def _init_ui(self) -> None:
        """初始化统计卡片布局。"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(14)

        layout.addWidget(self._create_card("当前人数", self.people_value))
        layout.addWidget(self._create_card("FPS", self.fps_value))
        layout.addWidget(self._create_card("检测模式", self.mode_value))
        layout.addWidget(self._create_card("检测状态", self.status_value))
        layout.addStretch()

    def _create_card(self, title: str, value_label: QLabel) -> QFrame:
        """创建统一样式的统计卡片。"""
        card = QFrame()
        card.setObjectName("statsCard")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(16, 14, 16, 14)
        card_layout.setSpacing(8)

        title_label = QLabel(title)
        title_label.setObjectName("cardTitle")
        value_label.setObjectName("cardValue")

        card_layout.addWidget(title_label)
        card_layout.addWidget(value_label)
        return card

    def update_stats(self, people_count: int, fps: float) -> None:
        """更新人数和 FPS 统计数据。"""
        self.people_value.setText(str(people_count))
        self.fps_value.setText(f"{fps:.2f}")

    def update_mode(self, mode_text: str) -> None:
        """更新检测模式显示。"""
        self.mode_value.setText(mode_text)

    def update_detection_status(self, status_text: str) -> None:
        """更新检测状态，并刷新状态颜色。"""
        self.status_value.setText(status_text)
        self.status_value.setProperty("status", status_text)
        self.status_value.style().unpolish(self.status_value)
        self.status_value.style().polish(self.status_value)

    def update_alert_status(self, status_text: str) -> None:
        """兼容旧调用，实际更新检测状态。"""
        self.update_detection_status(status_text)
