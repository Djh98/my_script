# scripts/log_cleaner.py
"""日志清理脚本"""

import sys
from pathlib import Path
from datetime import datetime, timedelta

# 添加父目录到路径
sys.path.append(str(Path(__file__).parent.parent))

from utils.logger import get_logger
from utils.config import config

def clean_logs(keep_days=None, log_dirs=None, dry_run=False):
    """清理过期日志文件"""
    logger = get_logger("log_cleaner")

    # 从配置获取默认值
    keep_days = keep_days or config.get('log_cleaner.keep_days', 30)
    log_dirs = log_dirs or config.get('log_cleaner.log_dirs', ['./logs'])

    cutoff_date = datetime.now() - timedelta(days=keep_days)

    logger.info(f"清理 {keep_days} 天前的日志文件")
    logger.info(f"截止日期: {cutoff_date.strftime('%Y-%m-%d')}")

    total_cleaned = 0
    total_size = 0

    for log_dir_path in log_dirs:
        log_dir = Path(log_dir_path)
        if not log_dir.exists():
            logger.warning(f"日志目录不存在: {log_dir}")
            continue

        logger.info(f"检查目录: {log_dir}")

        for log_file in log_dir.glob("*.log"):
            try:
                # 获取文件修改时间
                file_time = datetime.fromtimestamp(log_file.stat().st_mtime)

                if file_time < cutoff_date:
                    file_size = log_file.stat().st_size

                    if dry_run:
                        logger.info(f"[预览] 将删除: {log_file.name} ({file_size} bytes)")
                    else:
                        log_file.unlink()
                        logger.info(f"删除: {log_file.name} ({file_size} bytes)")

                    total_cleaned += 1
                    total_size += file_size

            except Exception as e:
                logger.error(f"处理文件 {log_file} 时出错: {e}")

    size_mb = total_size / 1024 / 1024
    action = "将清理" if dry_run else "已清理"
    logger.info(f"{action} {total_cleaned} 个文件，释放 {size_mb:.2f} MB 空间")

    return total_cleaned

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="日志清理工具")
    parser.add_argument("--days", "-d", type=int, help="保留天数（默认30天）")
    parser.add_argument("--dir", action="append", help="日志目录（可多次指定）")
    parser.add_argument("--dry-run", action="store_true", help="预览模式")

    args = parser.parse_args()
    clean_logs(args.days, args.dir, args.dry_run)
