"""主窗口模块。"""

from datetime import datetime

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFileDialog,
    QFrame,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
)

from config import QSS_DIR
from core.detector import ModelLoadError
from core.image_processor import ImageProcessor
from threads.camera_thread import CameraThread
from threads.video_thread import VideoThread
from ui.log_table import LogTable
from ui.stats_panel import StatsPanel
from ui.video_widget import VideoWidget


class MainWindow(QMainWindow):
    """AI 人数统计与智能监测系统主窗口。

    支持图片检测、视频检测和摄像头实时检测。
    """

    def __init__(self) -> None:
        """初始化主窗口。"""
        super().__init__()
        self.current_mode = "未选择"
        self.image_processor = ImageProcessor()
        self.video_thread: VideoThread | None = None
        self.camera_thread: CameraThread | None = None
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
            if mode == "图片检测":
                button.clicked.connect(self._handle_image_detection)
            elif mode == "视频检测":
                button.clicked.connect(self._handle_video_detection)
            elif mode == "摄像头检测":
                button.clicked.connect(self._handle_camera_detection)
            elif mode == "停止检测":
                button.clicked.connect(self._handle_stop_detection)
            else:
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

    def _handle_image_detection(self) -> None:
        """处理图片检测按钮点击事件。"""
        if self._has_running_stream():
            QMessageBox.information(self, "提示", "实时检测正在运行，请先停止检测。")
            return

        image_path, _ = QFileDialog.getOpenFileName(
            self,
            "选择图片",
            "",
            "图片文件 (*.jpg *.jpeg *.png *.bmp)",
        )
        if not image_path:
            return

        self.current_mode = "图片检测"
        self.stats_panel.update_mode("图片检测")
        self.stats_panel.update_alert_status("检测中")

        try:
            result = self.image_processor.process_image(image_path)
        except ModelLoadError as exc:
            self._show_error("模型加载失败", str(exc), "图片检测失败：模型不可用")
            return
        except Exception as exc:
            self._show_error("图片检测失败", str(exc), "图片检测失败：处理异常")
            return

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.video_widget.show_bgr_image(result.annotated_image)
        self.stats_panel.update_stats(result.people_count, result.fps)
        self.stats_panel.update_mode("图片检测")
        self.stats_panel.update_alert_status("正常")
        self.log_table.add_log(
            time_text=now,
            mode="图片检测",
            people_count=result.people_count,
            fps=result.fps,
            status="检测完成",
            result_path=str(result.output_path),
        )

    def _show_error(self, title: str, message: str, log_status: str) -> None:
        """弹窗提示异常，并同步写入日志表格。"""
        QMessageBox.warning(self, title, message)
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.stats_panel.update_mode("图片检测")
        self.stats_panel.update_stats(0, 0.0)
        self.stats_panel.update_alert_status("正常")
        self.log_table.add_log(
            time_text=now,
            mode="图片检测",
            people_count=0,
            fps=0.0,
            status=log_status,
            result_path="-",
        )

    def _handle_video_detection(self) -> None:
        """处理视频检测按钮点击事件。"""
        if self._is_camera_running():
            QMessageBox.information(self, "提示", "摄像头检测正在运行，请先停止当前检测。")
            return
        if self._is_video_running():
            QMessageBox.information(self, "提示", "视频检测正在运行，请先停止当前检测。")
            return

        video_path, _ = QFileDialog.getOpenFileName(
            self,
            "选择视频",
            "",
            "视频文件 (*.mp4 *.avi *.mov *.mkv)",
        )
        if not video_path:
            return

        self.current_mode = "视频检测"
        self.stats_panel.update_mode("视频检测")
        self.stats_panel.update_stats(0, 0.0)
        self.stats_panel.update_alert_status("正常")
        self.video_widget.show_mode_hint("视频检测")

        self.video_thread = VideoThread(video_path)
        self.video_thread.frame_ready.connect(self._update_video_frame)
        self.video_thread.error_signal.connect(self._handle_video_error)
        self.video_thread.finished_signal.connect(self._handle_video_finished)
        self.video_thread.start()

        self._add_log(
            mode="视频检测",
            people_count=0,
            fps=0.0,
            status="视频检测开始",
            result_path="-",
        )

    def _handle_stop_detection(self) -> None:
        """处理停止检测按钮点击事件。"""
        if self._is_video_running() and self.video_thread is not None:
            self.stats_panel.update_alert_status("停止中")
            self.video_thread.stop()
            return
        if self._is_camera_running() and self.camera_thread is not None:
            self.stats_panel.update_alert_status("停止中")
            self.camera_thread.stop()
            return

        self._handle_nav_click("停止检测")

    def _update_video_frame(self, frame, people_count: int, fps: float) -> None:
        """接收视频线程结果并刷新 GUI。"""
        self.video_widget.show_bgr_image(frame)
        self.stats_panel.update_stats(people_count, fps)
        self.stats_panel.update_mode("视频检测")
        self.stats_panel.update_alert_status("正常")

    def _handle_video_error(self, message: str) -> None:
        """处理视频线程异常提示。"""
        QMessageBox.warning(self, "视频检测失败", message)

    def _handle_video_finished(self, status: str, result_path: str, people_count: int, fps: float) -> None:
        """视频线程结束后写入日志并清理线程引用。"""
        status_text_map = {
            "completed": "视频检测完成",
            "stopped": "视频检测停止",
            "error": "视频检测异常",
        }
        status_text = status_text_map.get(status, "视频检测结束")

        self.stats_panel.update_stats(people_count, fps)
        self.stats_panel.update_mode("视频检测")
        self.stats_panel.update_alert_status("正常")
        self._add_log(
            mode="视频检测",
            people_count=people_count,
            fps=fps,
            status=status_text,
            result_path=result_path,
        )

        if self.video_thread is not None:
            self.video_thread.deleteLater()
            self.video_thread = None

    def _handle_camera_detection(self) -> None:
        """处理摄像头检测按钮点击事件。"""
        if self._is_camera_running():
            QMessageBox.information(self, "提示", "摄像头检测正在运行，请勿重复打开。")
            return
        if self._is_video_running():
            QMessageBox.information(self, "提示", "视频检测正在运行，请先停止视频检测。")
            return

        self.current_mode = "摄像头检测"
        self.stats_panel.update_mode("摄像头检测")
        self.stats_panel.update_stats(0, 0.0)
        self.stats_panel.update_alert_status("正常")
        self.video_widget.show_mode_hint("摄像头检测")

        self.camera_thread = CameraThread(camera_index=0)
        self.camera_thread.frame_ready.connect(self._update_camera_frame)
        self.camera_thread.error_signal.connect(self._handle_camera_error)
        self.camera_thread.finished_signal.connect(self._handle_camera_finished)
        self.camera_thread.start()

        self._add_log(
            mode="摄像头检测",
            people_count=0,
            fps=0.0,
            status="摄像头检测开始",
            result_path="-",
        )

    def _update_camera_frame(self, frame, people_count: int, fps: float) -> None:
        """接收摄像头线程结果并刷新 GUI。"""
        self.video_widget.show_bgr_image(frame)
        self.stats_panel.update_stats(people_count, fps)
        self.stats_panel.update_mode("摄像头检测")
        self.stats_panel.update_alert_status("正常")

    def _handle_camera_error(self, message: str) -> None:
        """处理摄像头线程异常提示。"""
        QMessageBox.warning(self, "摄像头检测失败", message)

    def _handle_camera_finished(self, status: str, people_count: int, fps: float) -> None:
        """摄像头线程结束后写入日志并清理线程引用。"""
        status_text_map = {
            "stopped": "摄像头检测停止",
            "open_failed": "摄像头打开失败",
            "error": "摄像头检测异常",
        }
        status_text = status_text_map.get(status, "摄像头检测停止")

        self.stats_panel.update_stats(people_count, fps)
        self.stats_panel.update_mode("摄像头检测")
        self.stats_panel.update_alert_status("正常")
        self._add_log(
            mode="摄像头检测",
            people_count=people_count,
            fps=fps,
            status=status_text,
            result_path="-",
        )

        if self.camera_thread is not None:
            self.camera_thread.deleteLater()
            self.camera_thread = None

    def _is_video_running(self) -> bool:
        """判断视频检测线程是否正在运行。"""
        return self.video_thread is not None and self.video_thread.isRunning()

    def _is_camera_running(self) -> bool:
        """判断摄像头检测线程是否正在运行。"""
        return self.camera_thread is not None and self.camera_thread.isRunning()

    def _has_running_stream(self) -> bool:
        """判断视频或摄像头实时检测是否正在运行。"""
        return self._is_video_running() or self._is_camera_running()

    def _add_log(self, mode: str, people_count: int, fps: float, status: str, result_path: str) -> None:
        """向底部日志表格写入统一格式日志。"""
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.log_table.add_log(
            time_text=now,
            mode=mode,
            people_count=people_count,
            fps=fps,
            status=status,
            result_path=result_path,
        )

    def closeEvent(self, event) -> None:
        """关闭窗口时安全停止视频和摄像头线程。"""
        if self._is_video_running() and self.video_thread is not None:
            self.video_thread.stop()
            self.video_thread.wait(3000)
        if self._is_camera_running() and self.camera_thread is not None:
            self.camera_thread.stop()
            self.camera_thread.wait(3000)
        super().closeEvent(event)
