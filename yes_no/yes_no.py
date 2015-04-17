import sys


def ask(question):
    valid = {
        "yes": True,
        "y": True,
        "ye": True,
        "no": False,
        "n": False
    }
    while True:
        sys.stdout.write(question + ' [y/N] ')
        choice = raw_input().lower()
        if choice == '':
            return False
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")
