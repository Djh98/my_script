# utils/config.py
"""简单的配置管理"""

import yaml
from pathlib import Path

class Config:
    def __init__(self):
        config_file = Path(__file__).parent.parent / "config" / "settings.yaml"
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                self.data = yaml.safe_load(f) or {}
        except:
            self.data = {}

    def get(self, key, default=None):
        """获取配置，支持 app.name 这种格式"""
        keys = key.split('.')
        value = self.data
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k, {})
            else:
                return default
        return value if value != {} else default

# 全局配置实例
config = Config()
