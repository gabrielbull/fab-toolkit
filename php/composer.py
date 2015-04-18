from fabric.api import *
from toolkit.permission.permission import Permission


class Composer:
    @staticmethod
    def install(directory, user=None):
        with cd(directory):
            sudo("curl -sS https://getcomposer.org/installer | php", user=user)
            sudo("php composer.phar  install --no-dev", user=user)
            sudo("rm -Rf composer.phar", user=user)
