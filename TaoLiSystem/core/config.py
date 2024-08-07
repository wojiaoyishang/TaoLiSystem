# 全局配置文件
global_var = {}

# class Config:
#     def __init__(self, filename='TaoLiSystem/data/config.ini'):
#         self.filename = filename
# 
#     def _load_config(self):
#         config = {}
#         try:
#             f = open(self.filename, 'r')
#         except OSError:
#             f = open(self.filename, 'w')
#         section = ""
#         for line in f:
#             line = line.strip()
#             if line.startswith('[') and line.endswith(']'):
#                 section = line[1:-1]
#                 config[section] = {}
#             elif '=' in line:
#                 key, value = [item.strip() for item in line.split('=', 1)]
#                 config[section][key] = value
#         f.close()
#         return config
# 
#     def read(self, section, key, default=None):
#         config = self._load_config()
#         value = config.get(section, {}).get(key)
#         if value is None:
#             return default
#         return value
# 
#     def write(self, section, key, value):
#         config = self._load_config()
#         if section not in config:
#             config[section] = {}
#         config[section][key] = value
#         self._save_config(config)
# 
#     def _save_config(self, config):
#         with open(self.filename, 'w') as f:
#             for section in config:
#                 f.write('[{}]\n'.format(section))
#                 for key, value in config[section].items():
#                     f.write('{}={}\n'.format(key, value))

import os
import btree

class Config:
    def __init__(self, filename='TaoLiSystem/data/config.db'):
        self.filename = filename
        self.db = self._open_db()

    def _open_db(self):
        try:
            f = open(self.filename, 'r+b')
        except OSError:
            f = open(self.filename, 'w+b')
        return btree.open(f)

    def read(self, section, key, default=None):
        try:
            value = self.db[(section + ':' + key).encode()]
            return value.decode()
        except KeyError:
            return default

    def write(self, section, key, value):
        self.db[(section + ':' + key).encode()] = str(value).encode()
        self.db.flush()

    def close(self):
        self.db.close()

# 判断是否存在配置文件夹
try: os.mkdir('TaoLiSystem/data')
except: pass

# 初始化系统配置文件
configData = Config()

# 触摸按键灵敏度
touchPad_sensitivity = configData.read("system", "touchPad_sensitivity")
if touchPad_sensitivity is None or touchPad_sensitivity.strip() == "0":
    touchPad_sensitivity = 250
else:
    touchPad_sensitivity = int(touchPad_sensitivity)
    