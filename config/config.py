import sys
import yaml
import pickle
from toolkit.config.file import File
from toolkit.config.directory import Directory


class Config:
    """
    @type config_file: toolkit.config.directory.Directory|toolkit.config.file.File
    @type preference: toolkit.preference.preference.Preference
    @type preference_key: str
    """
    def __init__(self, config_file, preference, preference_key):
        self.preference = preference
        self.config_file = config_file
        self.preference_key = preference_key
        self.__config = self.__get_preference(preference_key)

    def reset(self):
        self.preference.set('_config_' + self.preference_key, None)

    def get(self):
        return self.__config

    def __get_preference(self, name):
        saved_config = self.load_saved_config(self.preference.get('_config_' + name))
        default_config = self.load_config()

        config = self.merge_config(default_config, saved_config)
        self.save_config(config, name)

        return config

    def load_saved_config(self, saved_config):
        if saved_config:
            return pickle.loads(saved_config)
        return None

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

    def merge_config(self, default_config, saved_config):
        if isinstance(default_config, dict):
            return_config = {}
        elif isinstance(default_config, list):
            return_config = []
        else:
            return_config = None

        for item in default_config:
            if isinstance(item, str):
                default_value = default_config[item]
                saved_value = None
                #if isinstance(saved_config, dict):
                    #saved_value = saved_config[item] if (saved_config and saved_config[item]) else None

                if isinstance(default_value, dict) or isinstance(default_value, list):
                    return_config[item] = self.merge_config(default_value, saved_value)
                else:
                    if saved_value:
                        return_config[item] = saved_value
                    else:
                        return_config[item] = default_value

            elif isinstance(item, dict):
                item_return_config = {}
                for key, default_value in item.iteritems():
                    saved_value = None
                    #if isinstance(saved_config, dict):
                        #saved_value = saved_config[key] if (saved_config and saved_config[key]) else None

                    if isinstance(default_value, dict) or isinstance(default_value, list):
                        item_return_config[key] = self.merge_config(default_value, saved_value)
                    else:
                        if saved_value:
                            print key
                            item_return_config[key] = saved_value
                        else:
                            item_return_config[key] = default_value

                if isinstance(return_config, list):
                    return_config.append(item_return_config)

        return return_config

    def save_config(self, config, name):
        self.preference.set('_config_' + name, pickle.dumps(config))
