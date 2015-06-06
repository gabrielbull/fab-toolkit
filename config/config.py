import yaml
from toolkit.config.file import File
from toolkit.config.directory import Directory


class Config:
    """
    @type config_file: toolkit.config.directory.Directory|toolkit.config.file.File
    @type preference: toolkit.preference.preference.Preference
    @type preference_key: str
    """
    def __init__(self, config_file):
        self.config_file = config_file
        self.loaded_config = {}
        self.is_config_loaded = False

    def get(self):
        if self.is_config_loaded:
            return self.loaded_config

        self.loaded_config = self.load_config()
        return self.loaded_config

    def load_config(self):
        if isinstance(self.config_file, File):
            return self.load_config_file(self.config_file)
        elif isinstance(self.config_file, Directory):
            return self.load_config_directory(self.config_file)

    def load_config_directory(self, directory):
        config = {}
        for file in directory.get_file_list():
            if isinstance(file, File):
                config[file.file().replace('.yaml', '')] = self.load_config_file(file)
            elif isinstance(file, Directory):
                config[file.directory()] = self.load_config_directory(file)

        return config

    def load_config_file(self, file):
        return yaml.load(open(file.path(), 'r'))
