from fabric.api import *


class Npm:
    @staticmethod
    def install(directory, user=None):
        with cd(directory):
            sudo("npm install")

    @staticmethod
    def update(directory, user=None):
        with cd(directory):
            sudo("npm update")
