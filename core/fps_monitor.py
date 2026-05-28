"""FPS 监控模块。"""

import time


class FPSMonitor:
    """FPS 监控工具类。

    视频检测和后续摄像头检测都可以复用该类计算实时 FPS。
    """

    def __init__(self) -> None:
        """初始化 FPS 状态。"""
        self.fps = 0.0
        self.last_time = time.perf_counter()

    def update(self) -> float:
        """更新并返回当前 FPS。"""
        current_time = time.perf_counter()
        elapsed = current_time - self.last_time
        self.last_time = current_time
        if elapsed > 0:
            self.fps = 1.0 / elapsed
        return self.fps

    def reset(self) -> None:
        """重置 FPS 状态。"""
        self.fps = 0.0
        self.last_time = time.perf_counter()
