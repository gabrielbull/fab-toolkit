from fabric.contrib.files import *
import tempfile
import tkFileDialog


class User:
    def run(self):
        action = raw_input('What do you want to do ? (create/delete): ')
        if action == 'create':
            self.create()

    def create(self):
        user = raw_input('Username: ')
        self.create_user(user)
        self.setup_user_directory(user)
        self.create_user_key(user)
        self.make_user_sudoer(user)

    def create_user(self, user):
        with hide('running', 'stdout', 'stderr'):
            if not sudo("getent passwd " + user, quiet=True):
                sudo("useradd " + user)

    def setup_user_directory(self, user):
        with cd("/home/" + user):
            with hide('running', 'stdout', 'stderr'):
                sudo("mkdir -m 0700 -p .ssh", user=user)
                sudo("touch .ssh/authorized_keys", user=user)
                sudo("touch .ssh/known_hosts", user=user)
                sudo("chmod 600 .ssh/authorized_keys", user=user)

    def create_user_key(self, user):
        with hide('running', 'stdout', 'stderr'):
            temp = tempfile.NamedTemporaryFile()
            local('rm ' + temp.name)
            local('ssh-keygen -t rsa -N "" -f ' + temp.name)

            f = open(temp.name, 'r')
            private_key = f.read()
            f.close()

            f = open(temp.name + '.pub', 'r')
            public_key = f.read()
            f.close()

            temp.close()

            with cd("/home/" + user):
                append(".ssh/authorized_keys", public_key, use_sudo=True)

        save_path = tkFileDialog.askdirectory()

        f = open(save_path + '/' + user + '_' + env.host_string + '.pem', 'w')
        f.write(private_key)
        f.close()

    def make_user_sudoer(self, user):
        with hide('running', 'stdout', 'stderr'):
            sudo(
                "sed -i.bak -r -e '/" + user + "[ \\t]*ALL=\\(ALL\\)[ \\t]*NOPASSWD: ALL/" +
                "{ N; s/" + user + "[ \\t]*ALL=\\(ALL\\)[ \\t]*NOPASSWD: ALL\\n// }' \"$(echo /etc/sudoers)\"" +
                " && " +
                "sed -i.bak -r -e 's/(root[ \\t]*ALL=\\(ALL\\)[ \\t]*ALL)/" +
                "\\1\\n" + user + "    ALL=\\(ALL\\)       NOPASSWD: ALL" +
                "/g' \"$(echo /etc/sudoers)\""
            )
