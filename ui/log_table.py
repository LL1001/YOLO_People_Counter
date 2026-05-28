"""日志表格模块。"""

from PySide6.QtWidgets import QTableWidget


class LogTable(QTableWidget):
    """检测日志表格占位类。"""

    def __init__(self) -> None:
        """初始化日志表格。"""
        super().__init__(0, 4)
        self.setHorizontalHeaderLabels(["时间", "来源", "人数", "备注"])

    def add_log(self, time_text: str, source: str, people_count: int, note: str = "") -> None:
        """添加日志占位方法。

        Phase 1 暂不填充表格数据，后续阶段实现。
        """
        _ = (time_text, source, people_count, note)
