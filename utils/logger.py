# utils/logger.py
"""简单的日志工具"""

import logging
from pathlib import Path

def get_logger(name="my_script"):
    """获取日志记录器"""
    logger = logging.getLogger(name)

    if logger.handlers:  # 避免重复设置
        return logger

    logger.setLevel(logging.INFO)

    # 控制台输出
    console = logging.StreamHandler()
    console.setFormatter(logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'
    ))
    logger.addHandler(console)

    # 文件输出
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    file_handler = logging.FileHandler(log_dir / f"{name}.log", encoding='utf-8')
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    ))
    logger.addHandler(file_handler)

    return logger
