from fabric.api import *


class PhpFpm:
    @staticmethod
    def stop():
        sudo('systemctl stop php-fpm')

    @staticmethod
    def start():
        sudo('systemctl start php-fpm')

    @staticmethod
    def restart():
        sudo('systemctl restart php-fpm')

