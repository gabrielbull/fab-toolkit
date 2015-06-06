import json
import sys
import os.path


class Preference:
    preference_file = '.cache/preference.json'
    preference_loaded = False
    preference = {}

    def set(self, key, value=None):
        if key == 'local_ssh_dir':
            sys.stdout.write('Location of your ssh keys (~/.ssh): ')
            value = self.parse_input(self, raw_input())

        self.preference[key] = value
        self.save_preference()

    def ask(self, key, question=""):
        if not self.preference_loaded:
            self.load_preference()

        if key in self.preference:
            return self.preference[key]
        else:
            if question:
                sys.stdout.write(question + ': ')
            else:
                sys.stdout.write(key + ': ')
            value = self.parse_input(self, raw_input())
            self.set(key, value)
            return value

    @staticmethod
    def parse_input(self, value):
        user_dir = os.path.expanduser("~")
        return value.replace("~", user_dir)

    def get(self, key):
        if not self.preference_loaded:
            self.load_preference()

        if key in self.preference:
            return self.preference[key]
        else:
            self.set(key)
            if key in self.preference:
                return self.preference[key]

    def load_preference(self):
        if os.path.isfile(self.preference_file):
            handle = open(self.preference_file, "r")
            data = handle.read()
            handle.close()
            try:
                self.preference = json.loads(data)
            except ValueError:
                self.preference = {}

        self.preference_loaded = True

    def save_preference(self):
        directory = os.path.dirname(self.preference_file)
        if not os.path.exists(directory):
            os.makedirs(directory)

        content = json.dumps(self.preference, sort_keys=True, indent=4, separators=(',', ': '))
        handle = open(self.preference_file, "w")
        handle.write(content)
        handle.close()

    def reset_preference(self):
        os.remove(self.preference_file)
