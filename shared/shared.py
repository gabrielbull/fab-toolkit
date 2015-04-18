import os
from toolkit.shared.repo import Repo
from toolkit.shared.keys import Keys
import getpass
from fabric.utils import *


class Shared:
    """
    @type config: toolkit.config.config.Config
    @type preference: toolkit.preference.preference.Preference
    """
    def __init__(self, config, preference):
        self.config = config
        self.preference = preference
        self.repo = Repo(config)
        self.private_key = None
        self.public_key = None
        #self.repo.update()
        self.init_shared()
        self.init_key_pair()

    def init_shared(self):
        empty_file = os.path.join(self.repo.dir(), "empty")
        if os.path.exists(empty_file):
            os.unlink(empty_file)

    def init_key_pair(self):
        user = getpass.getuser()
        self.private_key = self.preference.get("private_key")
        if not self.private_key:
            public_key_file = os.path.join(self.repo.dir(), "keys", user + ".pub")
            if os.path.exists(public_key_file):
                error("User " + user + " already exists")

            keys = Keys.create()

            directory = os.path.dirname(public_key_file)
            if not os.path.exists(directory):
                os.makedirs(directory)

            with open(public_key_file, 'w') as fout:
                fout.write(keys['public_key'])

            self.preference.set('private_key', keys['private_key'])
