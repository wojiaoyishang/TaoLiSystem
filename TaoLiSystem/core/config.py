# 全局配置文件
global_var = {}

class Config:
    def __init__(self, filename='TaoLiSystem/data/config.ini'):
        self.filename = filename

    def _load_config(self):
        config = {}
        with open(self.filename, 'r') as f:
            section = ""
            for line in f:
                line = line.strip()
                if line.startswith('[') and line.endswith(']'):
                    section = line[1:-1]
                    config[section] = {}
                elif '=' in line:
                    key, value = [item.strip() for item in line.split('=', 1)]
                    config[section][key] = value
        return config

    def read(self, section, key, default=None):
        config = self._load_config()
        value = config.get(section, {}).get(key)
        if value is None:
            return default
        return value

    def write(self, section, key, value):
        config = self._load_config()
        if section not in config:
            config[section] = {}
        config[section][key] = value
        self._save_config(config)

    def _save_config(self, config):
        with open(self.filename, 'w') as f:
            for section in config:
                f.write('[{}]\n'.format(section))
                for key, value in config[section].items():
                    f.write('{}={}\n'.format(key, value))

# 初始化系统配置文件
configData = Config()

# 触摸按键灵敏度
touchPad_sensitivity = configData.read("system", "touchPad_sensitivity")
if touchPad_sensitivity is None or touchPad_sensitivity.strip() == "0":
    touchPad_sensitivity = 250
    