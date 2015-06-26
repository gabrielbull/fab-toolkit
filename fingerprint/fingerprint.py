from fabric.api import *
from fabric.contrib.files import exists


class Fingerprint:
    @staticmethod
    def add(host):
        if not exists("~/.ssh"):
            run('mkdir ~/.ssh')

        if not exists("~/.ssh/known_hosts"):
            run('touch ~/.ssh/known_hosts')

        if not exists("/root/.ssh",use_sudo=True):
            sudo('mkdir /root/.ssh')

        if not exists("/root/.ssh/known_hosts"):
            sudo('touch /root/.ssh/known_hosts')

        run('ssh-keyscan bitbucket.org >> ~/.ssh/known_hosts')
        sudo('ssh-keyscan bitbucket.org >> ~/.ssh/known_hosts')
