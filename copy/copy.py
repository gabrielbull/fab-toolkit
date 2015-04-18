from fabric.api import *
from fabric.contrib.files import exists


class Copy:
    @staticmethod
    def copy(source, destination, user):
        if exists(destination):
            sudo("rm -Rf " + destination)
        sudo("cp -R " + source + " " + destination, user=user)

    @staticmethod
    def backup(source, user):
        destination = source.rstrip('/') + '.bak'
        Copy.copy(source, destination, user)
        return destination

    @staticmethod
    def copy_files(source, destination, files, user):
        source = source.rstrip('/') + '/'
        destination = destination.rstrip('/') + '/'
        for filename in files:
            if exists(source + filename):
                if exists(destination + filename):
                    sudo("rm -Rf " + destination + filename, user=user)
                sudo("cp -R " + source + filename + " " + destination + filename, user=user)

    @staticmethod
    def swap(source, destination, user):
        tmp_destination = destination.rstrip('/') + '_tmp'
        pre_command = ""
        if exists(destination):
            pre_command = "mv " + destination + " " + tmp_destination + " && "

        sudo(pre_command + "mv " + source + " " + destination, user=user)
        sudo("mv " + tmp_destination + " " + source, user=user)
