from fabric.api import *
from toolkit.permission.permission import Permission


class Bower:
    @staticmethod
    def install(directory, user=None):
        with cd(directory):
            sudo("bower --config.interactive=false --allow-root install")

    @staticmethod
    def update(directory, user=None):
        with cd(directory):
            sudo("bower --config.interactive=false --allow-root update")
