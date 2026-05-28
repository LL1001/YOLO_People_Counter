"""底部日志表格模块。"""

from PySide6.QtWidgets import QAbstractItemView, QHeaderView, QTableWidget, QTableWidgetItem


class LogTable(QTableWidget):
    """检测操作日志表格。

    Phase 6 只记录课程展示所需的关键检测事件。
    """

    HEADERS = ["时间", "模式", "人数", "FPS", "状态", "结果路径"]

    def __init__(self) -> None:
        """初始化日志表格。"""
        super().__init__(0, len(self.HEADERS))
        self.setObjectName("logTable")
        self.setHorizontalHeaderLabels(self.HEADERS)
        self.setAlternatingRowColors(True)
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

    def add_log(
        self,
        time_text: str,
        mode: str,
        people_count: int,
        fps: float,
        status: str,
        result_path: str = "-",
    ) -> None:
        """添加一条检测操作日志。"""
        row = self.rowCount()
        self.insertRow(row)

        values = [
            time_text,
            mode,
            str(people_count),
            f"{fps:.2f}",
            status,
            result_path,
        ]
        for column, value in enumerate(values):
            self.setItem(row, column, QTableWidgetItem(value))

        self.scrollToBottom()
