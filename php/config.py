from fabric.api import *
import re
from os import listdir
from os.path import isfile, join
from fabric.contrib.files import exists, append


class Config:
    @staticmethod
    def copy_configs(config_directory, remote_directory, config, user):
        files = [f for f in listdir(config_directory) if isfile(join(config_directory, f))]
        for file_name in files:
            file_path = config_directory + '/' + file_name
            file_content = Config.replace_variables(config, file_path)
            Config.upload_file(remote_directory, file_name, file_content, user)

    @staticmethod
    def upload_file(remote_directory, file_name, file_content, user):
        file_path = remote_directory + "/" + file_name
        if exists(file_path):
            sudo("rm " + file_path, user=user)

        sudo("touch " + file_path, user=user)
        # todo use put()?
        with hide("everything"):
            append(file_path, file_content)

    @staticmethod
    def replace_variables(config, file_path):
        file_content = open(file_path, 'r').read()

        pattern = re.compile(r'{{ (.*) }}')
        for match in re.findall(pattern, file_content):
            file_content = file_content.replace('{{ ' + match + ' }}', config[match])

        return file_content
