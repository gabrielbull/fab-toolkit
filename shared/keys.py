from fabric.api import *
import tempfile
import os


class Keys:
    @staticmethod
    def file_get_contents(filename):
        with open(filename) as f:
            return f.read()

    @staticmethod
    def create():
        tmp_directory = tempfile.mkdtemp()
        with hide("running", "stdout"):
            private_key_file = os.path.join(tmp_directory, 'key_pair')
            public_key_file = os.path.join(tmp_directory, 'key_pair.pub')
            local("ssh-keygen -t rsa -f " + private_key_file + " -N \"\"")
            private_key = Keys.file_get_contents(private_key_file)
            public_key = Keys.file_get_contents(public_key_file)

        return {
            'private_key': private_key,
            'public_key': public_key
        }
