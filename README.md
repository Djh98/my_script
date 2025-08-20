# 我的脚本工具集

个人使用的 Python 脚本集合，用于日常工作自动化。

## 项目结构

```text
my-scripts/                     # 工程根目录
├── config/                     # 配置目录
│   └── settings.yaml           # 默认配置文件（文件分类规则、日志清理规则等）
│
├── logs/                       # 日志目录（运行脚本时自动生成日志文件）
│   └── *.log                   # 比如 file_organizer.log、log_cleaner.log
│
├── scripts/                    # 存放具体功能脚本
│   ├── file_organizer.py       # 文件整理脚本：把目录下的文件分类到子目录
│   └── log_cleaner.py          # 日志清理脚本：清理过期日志文件
│
├── utils/                      # 工具模块（给 scripts 提供通用功能）
│   ├── __init__.py             # 让 utils 变成一个 Python 包
│   ├── config.py               # 配置加载工具（读取 settings.yaml）
│   └── logger.py               # 日志工具（封装 logging，输出到控制台+文件）
│
├── run.py                      # 统一入口，支持 "python run.py <脚本名> [参数]"
│
├── requirements.txt            # Python 依赖（目前只有 pyyaml）
│
├── .gitignore                  # Git 忽略文件配置
│
└── README.md                   # 项目说明文档（安装、使用示例）

```bash
git clone https://github.com/Djh98/my_script.git
cd my-scripts
pip install -r requirements.txt
