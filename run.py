# run.py
"""统一的脚本运行入口"""

import sys
import importlib
from pathlib import Path

def list_scripts():
    """列出所有可用的脚本"""
    scripts_dir = Path("scripts")
    scripts = []

    for script_file in scripts_dir.glob("*.py"):
        if not script_file.name.startswith("_"):
            scripts.append(script_file.stem)

    return scripts

def run_script(script_name, args=None):
    """运行指定的脚本"""
    try:
        # 动态导入脚本模块
        module = importlib.import_module(f"scripts.{script_name}")

        # 如果有参数，修改sys.argv
        if args:
            old_argv = sys.argv
            sys.argv = [f"scripts/{script_name}.py"] + args

        # 执行脚本的main部分
        if hasattr(module, 'main'):
            module.main()
        else:
            # 如果没有main函数，执行模块（触发if __name__ == "__main__"）
            importlib.reload(module)

        # 恢复argv
        if args:
            sys.argv = old_argv

    except ImportError:
        print(f"脚本不存在: {script_name}")
        return False
    except Exception as e:
        print(f"执行脚本时出错: {e}")
        return False

    return True

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python run.py <脚本名> [参数...]")
        print("可用脚本:")
        for script in list_scripts():
            print(f"  {script}")
        print("示例:")
        print("  python run.py file_organizer ~/Downloads --dry-run")
        print("  python run.py log_cleaner --days 7 --dry-run")
        return

    script_name = sys.argv[1]
    script_args = sys.argv[2:] if len(sys.argv) > 2 else None

    run_script(script_name, script_args)

if __name__ == "__main__":
    main()
