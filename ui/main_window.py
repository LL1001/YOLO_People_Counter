"""主窗口模块。"""

from datetime import datetime

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
)

from config import QSS_DIR
from ui.log_table import LogTable
from ui.stats_panel import StatsPanel
from ui.video_widget import VideoWidget


class MainWindow(QMainWindow):
    """AI 人数统计与智能监测系统主窗口。

    Phase 2 仅实现科技风 GUI 框架，所有按钮只写入测试日志。
    """

    def __init__(self) -> None:
        """初始化主窗口。"""
        super().__init__()
        self.current_mode = "未选择"
        self.setWindowTitle("AI人数统计与智能监测系统")
        self.resize(1400, 860)
        self.setMinimumSize(1180, 760)
        self._load_style()
        self._init_ui()

    def _load_style(self) -> None:
        """加载深色科技风 QSS 样式。"""
        qss_path = QSS_DIR / "dark_theme.qss"
        if qss_path.exists():
            self.setStyleSheet(qss_path.read_text(encoding="utf-8"))

    def _init_ui(self) -> None:
        """初始化主界面布局。"""
        root = QWidget()
        root.setObjectName("rootWidget")
        root_layout = QVBoxLayout(root)
        root_layout.setContentsMargins(18, 18, 18, 18)
        root_layout.setSpacing(14)

        root_layout.addWidget(self._create_header())
        root_layout.addLayout(self._create_main_content(), stretch=1)

        self.log_table = LogTable()
        root_layout.addWidget(self.log_table, stretch=0)

        self.setCentralWidget(root)

    def _create_header(self) -> QFrame:
        """创建顶部标题栏。"""
        header = QFrame()
        header.setObjectName("headerBar")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(18, 12, 18, 12)

        title = QLabel("AI人数统计与智能监测系统")
        title.setObjectName("windowTitle")
        subtitle = QLabel("Phase 2 GUI Preview")
        subtitle.setObjectName("windowSubtitle")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(subtitle)
        return header

    def _create_main_content(self) -> QHBoxLayout:
        """创建左中右主体布局。"""
        content_layout = QHBoxLayout()
        content_layout.setSpacing(14)

        content_layout.addWidget(self._create_nav_panel(), stretch=0)

        self.video_widget = VideoWidget()
        content_layout.addWidget(self.video_widget, stretch=1)

        self.stats_panel = StatsPanel()
        content_layout.addWidget(self.stats_panel, stretch=0)

        return content_layout

    def _create_nav_panel(self) -> QFrame:
        """创建左侧导航按钮区域。"""
        nav = QFrame()
        nav.setObjectName("navPanel")
        nav.setFixedWidth(180)
        nav_layout = QVBoxLayout(nav)
        nav_layout.setContentsMargins(14, 16, 14, 16)
        nav_layout.setSpacing(12)

        nav_title = QLabel("功能导航")
        nav_title.setObjectName("navTitle")
        nav_layout.addWidget(nav_title)

        buttons = [
            ("图片检测", "图片检测"),
            ("视频检测", "视频检测"),
            ("摄像头检测", "摄像头检测"),
            ("停止检测", "停止检测"),
            ("保存截图", "保存截图"),
            ("导出 CSV", "导出 CSV"),
        ]
        for text, mode in buttons:
            button = QPushButton(text)
            button.setObjectName("navButton")
            button.clicked.connect(lambda checked=False, mode_text=mode: self._handle_nav_click(mode_text))
            nav_layout.addWidget(button)

        nav_layout.addStretch()
        return nav

    def _handle_nav_click(self, mode_text: str) -> None:
        """处理按钮点击事件，仅写入测试日志。"""
        self.current_mode = mode_text
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.stats_panel.update_mode(mode_text)
        self.stats_panel.update_stats(0, 0.0)
        self.stats_panel.update_alert_status("测试")
        self.video_widget.show_mode_hint(mode_text)
        self.log_table.add_log(
            time_text=now,
            mode=mode_text,
            people_count=0,
            fps=0.0,
            status="测试日志：GUI 按钮已点击",
            result_path="-",
        )
