from fabric.api import *


class Permission:
    @staticmethod
    def owner(directory, user, group):
        sudo("chown -R " + user + ":" + group + " " + directory)

    @staticmethod
    def permissions(files, perm):
        for filename in files:
            sudo("chmod " + perm + " " + filename)
