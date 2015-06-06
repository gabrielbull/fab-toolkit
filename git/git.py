from fabric.api import *
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
            current_branch = sudo("git rev-parse --abbrev-ref HEAD")
            sudo("git remote set-url origin " + remote)
            sudo("git checkout -- .")
            if current_branch != branch:
                sudo("git checkout -b " + branch + " origin/" + branch)
            sudo("git branch --set-upstream-to=origin/" + branch)
            sudo("git pull origin " + branch)

        Permission.owner(repository, user, user)

    @staticmethod
    def submodule_update(repository, user):
        with cd(repository):
            sudo("git submodule init")
            sudo("git submodule update")

            Permission.owner(repository, user, user)
