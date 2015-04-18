from fabric.api import *


class Fingerprint:
    @staticmethod
    def add(host):
        run('ssh-keyscan bitbucket.org >> ~/.ssh/known_hosts')
        sudo('ssh-keyscan bitbucket.org >> ~/.ssh/known_hosts')

