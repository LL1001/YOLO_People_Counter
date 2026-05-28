"""右侧统计卡片模块。"""

from PySide6.QtWidgets import QFrame, QLabel, QLineEdit, QVBoxLayout, QWidget


class StatsPanel(QWidget):
    """人数统计与运行状态面板。

    Phase 2 只展示静态/测试状态，不计算真实检测数据。
    """

    def __init__(self) -> None:
        """初始化统计面板。"""
        super().__init__()
        self.setObjectName("statsPanel")
        self.people_value = QLabel("0")
        self.fps_value = QLabel("0.00")
        self.mode_value = QLabel("未选择")
        self.alert_value = QLabel("正常")
        self.threshold_input = QLineEdit("10")
        self._init_ui()

    def _init_ui(self) -> None:
        """初始化统计卡片布局。"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(14)

        layout.addWidget(self._create_card("当前人数", self.people_value))
        layout.addWidget(self._create_card("FPS", self.fps_value))
        layout.addWidget(self._create_card("检测模式", self.mode_value))
        layout.addWidget(self._create_card("告警状态", self.alert_value))
        layout.addWidget(self._create_threshold_card())
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

    def _create_threshold_card(self) -> QFrame:
        """创建人数阈值输入卡片。"""
        card = QFrame()
        card.setObjectName("statsCard")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(16, 14, 16, 14)
        card_layout.setSpacing(8)

        title_label = QLabel("人数阈值")
        title_label.setObjectName("cardTitle")
        self.threshold_input.setObjectName("thresholdInput")
        self.threshold_input.setPlaceholderText("请输入阈值")

        card_layout.addWidget(title_label)
        card_layout.addWidget(self.threshold_input)
        return card

    def update_stats(self, people_count: int, fps: float) -> None:
        """更新统计数据占位方法。"""
        self.people_value.setText(str(people_count))
        self.fps_value.setText(f"{fps:.2f}")

    def update_mode(self, mode_text: str) -> None:
        """更新检测模式显示。"""
        self.mode_value.setText(mode_text)

    def update_alert_status(self, status_text: str) -> None:
        """更新告警状态显示。"""
        self.alert_value.setText(status_text)
