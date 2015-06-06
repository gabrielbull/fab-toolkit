from fabric.api import *
import os
from toolkit.copy.copy import Copy
from toolkit.permission.permission import Permission


class Repo:
    """
    @type config: toolkit.config._config.Config
    @type preference: toolkit.preference.preference.Preference
    """
    def __init__(self, config):
        self.config = config
        self.git_info = self.get_git_info()

    def dir(self):
        return '.cache/shared'

    def get_git_info(self):
        git_info = {}
        with hide('running'):
            git_info['remote'] = local("git config --get remote.origin.url", capture=True)
        return git_info

    def create_local_repo(self):
        if not os.path.exists(".cache/shared/.git"):
            local("git init .cache/shared")

    def add_remote(self):
        with hide('running'):
            remote = local("git --git-dir .cache/shared/.git remote", capture=True)
            if not remote == 'origin':
                local("git --git-dir .cache/shared/.git remote add origin " + self.git_info['remote'])

    def verify_branch(self):
        with hide('running'):
            local_branch = local("git --git-dir .cache/shared/.git branch", capture=True)

            if local_branch != '* ' + self.config.get()["shared"]['branch']:
                remote_exists = local("if git ls-remote " + self.git_info['remote'] + " | " +
                    "grep -sw \"" + self.config.get()["shared"]['branch'] + "\" 2>&1>/dev/null; " +
                    "then echo \"True\" ; else echo \"False\" ; fi", capture=True)

                remote_exists = True if remote_exists == 'True' else False
                if not remote_exists:
                    self.create_local_branch()
                    self.create_remote_branch()
                else:
                    self.create_local_branch_from_remote()

    def create_local_branch(self):
        with hide('everything'):
            local("git --git-dir .cache/shared/.git checkout --orphan " + self.config.get()["shared"]['branch'])
            local("touch .cache/shared/empty")
            local("git --git-dir .cache/shared/.git --work-tree=.cache/shared add empty")
            local("git --git-dir .cache/shared/.git --work-tree=.cache/shared commit -m \"initial commit\"")

    def create_remote_branch(self):
        self.add_remote()
        with hide('running'):
            local("git --git-dir .cache/shared/.git push origin " + self.config.get()["shared"]['branch'])

    def create_local_branch_from_remote(self):
        self.add_remote()
        with hide('running'):
            local("git --git-dir .cache/shared/.git fetch")
            local("git --git-dir .cache/shared/.git --work-tree=.cache/shared checkout -b " +
                self.config.get()["shared"]['branch'] + " origin/" + self.config.get()["shared"]['branch'])

    def pull(self):
        self.add_remote()
        with hide('everything'):
            local("git --git-dir .cache/shared/.git pull")

    def update(self):
        self.create_local_repo()
        self.verify_branch()
        self.pull()
