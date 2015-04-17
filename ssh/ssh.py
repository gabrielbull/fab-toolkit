from fabric.api import *
import string
import random


class Ssh:
    @staticmethod
    def create_ssh_key(self, destination, name):
        with hide("everything"):
            # todo: fix passphrases, cause we can't do "ssh-add -K ~/.ssh/keyname" without
            # manually entering the passphrase
            # passphrase = passphrase_generator()
            # local("ssh-keygen -t rsa -f " + dir + "/" + name + " -N " + passphrase)
            local("ssh-keygen -t rsa -f " + destination + "/" + name + " -N \"\"")
            local("chmod 600 " + destination + "/" + name)
            local("ssh-add -K " + destination + "/" + name)
            # todo: detect environment, this command works on Mac OS X only

    @staticmethod
    def create_remote_ssh_key(self, destination, name):
        with hide("everything"):
            run("ssh-keygen -t rsa -f " + destination + "/" + name + " -N \"\"")
            run("chmod 600 " + destination + "/" + name)
            run("ssh-add " + destination + "/" + name)

    @staticmethod
    def get_remote_ssh_key(self, destination, name):
        with hide("everything"):
            pub_key = run("cat " + destination + "/" + name + ".pub")
        return pub_key

    @staticmethod
    def passphrase_generator(size=32, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
        return '' . join(random.choice(chars) for _ in range(size))
