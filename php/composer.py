from fabric.api import *
from toolkit.permission.permission import Permission


class Composer:
    @staticmethod
    def install(directory, user=None):
        with cd(directory):
            sudo("curl -sS https://getcomposer.org/installer | php")
            sudo("php composer.phar  install --no-dev")
            sudo("rm -Rf composer.phar")

            if user:
                Permission.owner(directory + "/vendor", user, user)
