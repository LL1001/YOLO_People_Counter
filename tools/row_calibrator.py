"""教室座位排区域标定辅助工具。

该工具仅用于开发和配置，不集成到主 GUI。
工具会打开 OpenCV 图形窗口，请在本地 Windows 桌面环境运行。
运行前请手动将标准教室图片放到 demo/images/classroom_standard.jpg。
"""

from __future__ import annotations

import sys
from pathlib import Path

import cv2


# 允许从 tools/ 目录直接运行脚本时导入项目配置。
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config import DEMO_CLASSROOM_IMAGE_PATH  # noqa: E402


WINDOW_NAME = "Classroom Row Calibrator"


class RowCalibrator:
    """鼠标拖拽矩形区域，用于标定每一排座位坐标。"""

    def __init__(self, image_path: Path, image) -> None:
        """初始化标定工具状态。"""
        self.image_path = image_path
        self.image = image
        self.preview = self.image.copy()
        self.rows: list[tuple[int, int, int, int]] = []
        self.start_point: tuple[int, int] | None = None
        self.dragging = False

    def run(self) -> None:
        """启动 OpenCV 标定窗口。"""
        print("操作说明：")
        print("1. 鼠标左键拖拽矩形，框选每一排座位区域。")
        print("2. 每次松开鼠标后，终端会输出坐标：(x1, y1, x2, y2)。")
        print("3. 按 s 键输出 CLASSROOM_ROWS 示例格式。")
        print("4. 按 q 键退出标定工具。")

        cv2.namedWindow(WINDOW_NAME)
        cv2.setMouseCallback(WINDOW_NAME, self._on_mouse)

        while True:
            cv2.imshow(WINDOW_NAME, self.preview)
            key = cv2.waitKey(20) & 0xFF
            if key == ord("s"):
                self._print_classroom_rows()
            elif key == ord("q"):
                break

        cv2.destroyAllWindows()

    def _on_mouse(self, event: int, x: int, y: int, flags: int, param) -> None:
        """处理鼠标拖拽事件。"""
        _ = (flags, param)
        if event == cv2.EVENT_LBUTTONDOWN:
            self.start_point = (x, y)
            self.dragging = True
        elif event == cv2.EVENT_MOUSEMOVE and self.dragging and self.start_point:
            self._draw_preview((x, y))
        elif event == cv2.EVENT_LBUTTONUP and self.dragging and self.start_point:
            self.dragging = False
            x1, y1 = self.start_point
            x2, y2 = x, y
            area = (min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2))
            self.rows.append(area)
            print(area)
            self._redraw_all_rows()

    def _draw_preview(self, current_point: tuple[int, int]) -> None:
        """拖拽过程中绘制临时预览框。"""
        self._redraw_all_rows()
        if self.start_point is None:
            return
        cv2.rectangle(self.preview, self.start_point, current_point, (0, 255, 255), 2)

    def _redraw_all_rows(self) -> None:
        """重绘已经标定的所有座位排区域。"""
        self.preview = self.image.copy()
        for index, area in enumerate(self.rows, start=1):
            x1, y1, x2, y2 = area
            cv2.rectangle(self.preview, (x1, y1), (x2, y2), (0, 220, 255), 2)
            cv2.putText(
                self.preview,
                f"Row {index}",
                (x1, max(y1 - 8, 20)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 220, 255),
                2,
                cv2.LINE_AA,
            )

    def _print_classroom_rows(self) -> None:
        """输出可复制到 config.py 的 CLASSROOM_ROWS 示例格式。"""
        print("\nCLASSROOM_ROWS = [")
        for index, area in enumerate(self.rows, start=1):
            print("    {")
            print(f'        "name": "第{index}排",')
            print(f'        "area": {area},')
            print('        "capacity": 8,  # 请根据实际座位数量手动修改')
            print("    },")
        print("]\n")


def main() -> int:
    """工具入口。"""
    image_path = DEMO_CLASSROOM_IMAGE_PATH
    if not image_path.exists():
        print(f"未找到标准教室图片：{image_path}")
        print("请手动将图片命名为 classroom_standard.jpg，并放入 demo/images/ 目录。")
        return 1

    image = cv2.imread(str(image_path))
    if image is None:
        print(f"图片读取失败：{image_path}")
        print("请确认图片格式正确，并可被 OpenCV 正常读取。")
        return 1

    calibrator = RowCalibrator(image_path, image)
    calibrator.run()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
