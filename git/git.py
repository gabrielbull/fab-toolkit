from fabric.api import *
from toolkit.copy.copy import Copy


class Git:
    @staticmethod
    def clone(destination, remote, branch, user):
        run("git clone -b " + branch + " " + remote + " " + destination)
        Copy().owner(destination, user, user)

    @staticmethod
    def pull(repository, remote, branch, user):
        with cd(repository):
            run("git remote set-url origin " + remote)
            run("git checkout -- .")
            run("git pull origin " + branch)

        Copy.owner(repository, user, user)

    @staticmethod
    def submodule_update(repository, user):
        with cd(repository):
            run("git submodule init")
            run("git submodule update")

        Copy.owner(repository, user, user)
