"""
Config utils
"""
import json
import os
home_dir = os.path.expanduser('~')
config_dir = os.path.join(home_dir, '.config/ipamd')
output_dir = os.path.join(home_dir, 'ipamd_output')
default_config = {
    'result_dir': output_dir,
    'output_level': 0,
    'auto_load': True,
    'external_plugin_dir': [
    ],
    'sakuanna_plugin_dir': [
    ],
    'simulation_plugin_dir': [
    ],
    'builder_plugin_dir': [
    ],
    'analyse_plugin_dir': [
    ],
    'default_ff': 'Calvados3'
}

class Config:
    """
    Config class
    """
    def __init__(self):
        self.__config_file_path = os.path.join(config_dir, 'config.json')
        self.__config = {}
        try:
            with open(self.__config_file_path, 'r', encoding='utf-8') as f:
                self.__config = json.load(f)
        except Exception:
            self.__config = default_config
            self.__save_config()

    def get(self, target):
        """
        Get config value
        @param target: Config key
        @return: Config value
        """
        if target in self.__config:
            return self.__config[target]
        else:
            if target in default_config:
                return default_config[target]
            else:
                return None

    def set(self, target, value):
        """
        Set config value
        @param target: Config key
        @param value: Config value
        """
        self.__config[target] = value
        self.__save_config()

    def __save_config(self):
        """
        Save config to file
        """
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
        with open(self.__config_file_path, 'w', encoding='utf-8') as f:
            json.dump(self.__config, f, indent=4)
