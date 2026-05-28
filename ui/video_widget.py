"""视频显示控件模块。"""

from PySide6.QtWidgets import QLabel


class VideoWidget(QLabel):
    """视频画面显示控件占位类。"""

    def __init__(self) -> None:
        """初始化视频显示控件。"""
        super().__init__()
        self.setText("视频显示区域")

    def update_frame(self, frame) -> None:
        """更新视频帧占位方法。

        Args:
            frame: 待显示的视频帧，本阶段暂不处理。
        """
        # Phase 1 暂不实现图像显示逻辑。
        _ = frame
