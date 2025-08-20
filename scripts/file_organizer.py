# scripts/file_organizer.py
"""文件整理脚本（简化版）"""

import sys
import shutil
from pathlib import Path
from collections import defaultdict

# 添加父目录到路径
sys.path.append(str(Path(__file__).parent.parent))

from utils.logger import get_logger
from utils.config import config

def organize_files(source_dir, target_dir=None, dry_run=False):
    """整理文件"""
    logger = get_logger("file_organizer")

    source = Path(source_dir)
    if not source.exists():
        logger.error(f"源目录不存在: {source}")
        return False

    # 目标目录
    target = Path(target_dir) if target_dir else source / "organized"

    # 文件类型映射
    file_types = {}
    for category, extensions in config.get('file_organizer', {}).items():
        for ext in extensions:
            file_types[ext] = category

    # 收集文件
    files_to_move = defaultdict(list)
    for file_path in source.glob('*'):
        if file_path.is_file():
            ext = file_path.suffix.lower()
            category = file_types.get(ext, 'others')
            files_to_move[category].append(file_path)

    # 显示计划
    logger.info(f"整理 {source} -> {target}")
    for category, files in files_to_move.items():
        logger.info(f"  {category}: {len(files)} 个文件")

    if dry_run:
        logger.info("预览模式，不实际移动文件")
        return True

    # 执行整理
    for category, files in files_to_move.items():
        category_dir = target / category
        category_dir.mkdir(parents=True, exist_ok=True)

        for file_path in files:
            try:
                target_file = category_dir / file_path.name
                # 如果文件已存在，添加序号
                counter = 1
                while target_file.exists():
                    stem = file_path.stem
                    suffix = file_path.suffix
                    target_file = category_dir / f"{stem}_{counter}{suffix}"
                    counter += 1

                shutil.move(str(file_path), str(target_file))
                logger.info(f"移动: {file_path.name} -> {category}")
            except Exception as e:
                logger.error(f"移动失败 {file_path.name}: {e}")

    logger.info("整理完成")
    return True

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="文件整理工具")
    parser.add_argument("source", help="源目录")
    parser.add_argument("--target", "-t", help="目标目录")
    parser.add_argument("--dry-run", "-d", action="store_true", help="预览模式")

    args = parser.parse_args()
    organize_files(args.source, args.target, args.dry_run)
