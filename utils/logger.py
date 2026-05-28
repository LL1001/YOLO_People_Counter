"""日志工具模块。"""

import logging


def get_logger(name: str = "YOLO_People_Counter") -> logging.Logger:
    """获取基础日志对象。"""
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger
