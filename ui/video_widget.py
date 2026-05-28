"""中间画面显示组件模块。"""

import cv2

from PySide6.QtCore import Qt
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QLabel


class VideoWidget(QLabel):
    """图片、视频和摄像头画面的统一显示区域。

    Phase 2 仅显示提示文字，后续阶段再接入真实画面。
    """

    def __init__(self) -> None:
        """初始化视频显示控件。"""
        super().__init__()
        self.setObjectName("videoDisplay")
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setMinimumSize(760, 480)
        self.setText("请选择检测模式")
        self._current_pixmap: QPixmap | None = None

    def update_frame(self, frame) -> None:
        """更新视频帧占位方法。

        Args:
            frame: 待显示的视频帧，本阶段暂不处理。
        """
        if frame is None:
            return
        self.show_bgr_image(frame)

    def show_mode_hint(self, mode_text: str) -> None:
        """显示当前选择的检测模式提示。"""
        self._current_pixmap = None
        self.clear()
        self.setText(f"{mode_text}\n\nGUI 框架测试中，暂未接入检测功能")

    def show_bgr_image(self, image) -> None:
        """显示 OpenCV BGR 图片，并按控件大小等比缩放。"""
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        height, width, channels = rgb_image.shape
        bytes_per_line = channels * width
        q_image = QImage(
            rgb_image.data,
            width,
            height,
            bytes_per_line,
            QImage.Format.Format_RGB888,
        ).copy()
        self._current_pixmap = QPixmap.fromImage(q_image)
        self._refresh_pixmap()

    def resizeEvent(self, event) -> None:
        """窗口尺寸变化时保持图片等比缩放显示。"""
        super().resizeEvent(event)
        self._refresh_pixmap()

    def _refresh_pixmap(self) -> None:
        """刷新当前图片显示，保持比例且不拉伸变形。"""
        if self._current_pixmap is None:
            return

        scaled_pixmap = self._current_pixmap.scaled(
            self.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        self.setText("")
        self.setPixmap(scaled_pixmap)
