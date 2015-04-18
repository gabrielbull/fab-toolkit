import os


class File:
    """
    @type filename: str
    """
    def __init__(self, filename, path=None):
        if path:
            self.__path = path
        elif filename.startswith('/'):
            self.__path = ""
        else:
            self.__path = os.getcwd()
        self.__filename = filename

    def file(self, filename=None):
        if filename:
            self.__filename = filename
            return self
        return self.__filename

    def path(self):
        return os.path.join(self.__path, self.__filename)
