"""文件工具模块。"""

from datetime import datetime
from pathlib import Path


def ensure_dir(directory: str | Path) -> Path:
    """确保目录存在。"""
    path = Path(directory)
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_file_suffix(file_path: str | Path) -> str:
    """获取文件后缀名。"""
    return Path(file_path).suffix.lower()


def generate_timestamp_filename(prefix: str, suffix: str) -> str:
    """生成带时间戳的文件名，避免结果文件覆盖。"""
    safe_prefix = prefix.strip() or "result"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    return f"{safe_prefix}_{timestamp}{suffix}"
