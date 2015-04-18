from fabric.api import *
from toolkit.copy.copy import Copy
from toolkit.permission.permission import Permission


class Git:
    @staticmethod
    def get_temp_dir():
        temp = run("mktemp")
        run("rm -f " + temp)
        return temp

    @staticmethod
    def clone(destination, remote, branch, user):
        temp = Git.get_temp_dir()
        run("git clone -b " + branch + " " + remote + " " + temp)
        sudo("mv " + temp + " " + destination)
        Permission.owner(destination, user, user)

    @staticmethod
    def pull(repository, remote, branch, user):
        with cd(repository):
            sudo("git remote set-url origin " + remote)
            sudo("git checkout -- .")
            sudo("git pull origin " + branch)

        Permission.owner(repository, user, user)

    @staticmethod
    def submodule_update(repository, user):
        with cd(repository):
            run("git submodule init")
            run("git submodule update")

            Permission.owner(repository, user, user)
