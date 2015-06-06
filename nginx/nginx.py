from fabric.api import *


class Nginx:
    @staticmethod
    def stop():
        sudo('systemctl stop nginx')

    @staticmethod
    def start():
        sudo('systemctl start nginx')

    @staticmethod
    def restart():
        sudo('systemctl restart nginx')

