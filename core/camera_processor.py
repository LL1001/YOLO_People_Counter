"""摄像头处理模块。"""


class CameraProcessor:
    """摄像头处理占位类。"""

    def open_camera(self, camera_index: int = 0) -> bool:
        """打开摄像头占位方法。"""
        # Phase 1 暂不访问摄像头。
        _ = camera_index
        return False

    def release(self) -> None:
        """释放摄像头资源占位方法。"""
        pass
