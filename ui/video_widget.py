"""中间画面显示组件模块。"""

from PySide6.QtCore import Qt
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

    def update_frame(self, frame) -> None:
        """更新视频帧占位方法。

        Args:
            frame: 待显示的视频帧，本阶段暂不处理。
        """
        # Phase 2 暂不实现图像显示逻辑，避免提前接入检测流程。
        _ = frame

    def show_mode_hint(self, mode_text: str) -> None:
        """显示当前选择的检测模式提示。"""
        self.setText(f"{mode_text}\n\nGUI 框架测试中，暂未接入检测功能")
