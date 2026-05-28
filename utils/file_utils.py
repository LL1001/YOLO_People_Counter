"""文件工具模块。"""

from pathlib import Path


def ensure_dir(directory: str | Path) -> Path:
    """确保目录存在。"""
    path = Path(directory)
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_file_suffix(file_path: str | Path) -> str:
    """获取文件后缀名。"""
    return Path(file_path).suffix.lower()
