"""绘图工具模块。"""

import cv2


def draw_detection_boxes(image, detections: list[dict]):
    """在图片上绘制检测框、置信度和类别名称。"""
    for detection in detections:
        x1, y1, x2, y2 = detection["box"]
        confidence = detection["confidence"]
        class_name = detection["class_name"]
        label = f"{class_name} {confidence:.2f}"

        # 蓝青色检测框，契合科技风界面。
        box_color = (255, 220, 40)
        text_bg_color = (32, 150, 220)
        text_color = (255, 255, 255)

        cv2.rectangle(image, (x1, y1), (x2, y2), box_color, 2)

        text_size, _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
        text_width, text_height = text_size
        text_y = max(y1 - 8, text_height + 8)
        cv2.rectangle(
            image,
            (x1, text_y - text_height - 8),
            (x1 + text_width + 8, text_y + 4),
            text_bg_color,
            -1,
        )
        cv2.putText(
            image,
            label,
            (x1 + 4, text_y - 2),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            text_color,
            2,
            cv2.LINE_AA,
        )

    return image
