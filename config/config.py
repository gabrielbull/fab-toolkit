import sys
import yaml
import os


class Config:
    """
    @type preference: toolkit.preference.preference.Preference
    """
    def __init__(self, preference):
        self.preference = preference

    def get(self, name):
        config_file = self.preference.get('config_file:' + name + '.password')
        current_config = self.load_current_config(config_file)
        default_config = self.load_default_config()

        current_config = self.ask_config(default_config, current_config)
        self.save_config(config_file, current_config)

        return self.flatten_config(current_config)

    def flatten_config(self, config):
        return_value = {}
        if 'private' in config:
            for key in config['private']:
                return_value[key] = config['private'][key]

        if 'public' in config:
            for key in config['public']:
                return_value[key] = config['public'][key]

        return return_value

    def load_current_config(self, config_file):
        directory = os.path.dirname(config_file)
        if not os.path.exists(directory):
            os.makedirs(directory)

        if os.path.isfile(config_file):
            config = open(config_file, 'r')
        else:
            handle = open(config_file, "w")
            handle.write("")
            handle.close()
            config = ''

        if not config:
            config = {}
        else:
            #self.decrypt_config_file()
            config = yaml.load(config)

        return config

    def load_default_config(self):
        return yaml.load(open("config.yaml", 'r'))

    def decrypt_config_file(self):
        sys.stdout.write('Enter your password: ')
        password = raw_input()

    def ask_config(self, default_config, current_config):
        if not current_config:
            current_config = {}
            current_config['private'] = {}
            current_config['public'] = {}

        for key in default_config:
            default_value = default_config[key]
            if default_value.startswith('%private_'):
                config_key = 'private'
            else:
                config_key = 'public'

            if default_value.startswith('%') and default_value.endswith('%'):
                if not key in current_config[config_key]:
                    sys.stdout.write(key + ': ')
                    current_config[config_key][key] = raw_input()
            else:
                current_config[config_key][key] = default_value

        return current_config

    def save_config(self, config_file, config):
        handle = open(config_file, "w")
        handle.write(yaml.dump(config))
        handle.close()
