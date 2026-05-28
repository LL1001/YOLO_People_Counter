"""FPS 监控模块。"""


class FPSMonitor:
    """FPS 监控占位类。"""

    def __init__(self) -> None:
        """初始化 FPS 状态。"""
        self.fps = 0.0

    def update(self) -> float:
        """更新并返回 FPS 占位方法。"""
        # Phase 1 暂不计算真实 FPS。
        return self.fps

    def reset(self) -> None:
        """重置 FPS 状态。"""
        self.fps = 0.0
