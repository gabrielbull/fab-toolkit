from fabric.api import *
from toolkit.copy.copy import Copy


class Composer:
    @staticmethod
    def install(directory, user):
        with cd(directory):
            run("curl -sS https://getcomposer.org/installer | php")
            run("php composer.phar install")
            run("rm -Rf composer.phar")

        Copy.owner(directory, user, user)
