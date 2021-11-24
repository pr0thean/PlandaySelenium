import logging
import os
from configparser import ConfigParser


class ConfigHandler:
    def __init__(self):
        self.config_file_name = 'config.ini'
        self.section_name = 'browser'
        self.config_dir_path = ''
        self.config_file_path = ''
        self.ready_config = ''
        self.needed_capabilities = ''

        self.page_window_size = '',
        self.executable_path = ''
        self.base_page_url = ''
        self._driver = None
        self.initialize()

    def initialize(self):
        logging.info("Trying to initialize ConfigHandler")
        config = self.get_config()
        self.apply_config(config=config)

    def get_config(self):
        parent_directory = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir))
        self.config_dir_path = os.path.join(parent_directory, 'testrun_config')
        self.config_file_path = os.path.join(self.config_dir_path, self.config_file_name)
        config = ConfigParser()
        config.optionxform = str
        config.read(self.config_file_path)
        for key, value in config.items(section=self.section_name):
            if not config.get(self.section_name, key, fallback=None):
                config.set(self.section_name, str(key), str(value))
        self.ready_config = config
        return self.ready_config

    def apply_config(self, config: ConfigParser) -> dict:
        page_window_size = config.get(self.section_name, 'page_window_size', fallback=None)
        executable_path = config.get(self.section_name, 'executable_path', fallback=None)
        base_page_url = config.get(self.section_name, 'base_page_url', fallback=None)
        self.page_window_size = page_window_size
        self.executable_path = executable_path
        self.base_page_url = base_page_url
        self.needed_capabilities = {
            'page_window_size': page_window_size,
            'executable_path': executable_path,
            'base_page_url': base_page_url
        }
        return self.needed_capabilities
