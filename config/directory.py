import os
from toolkit.config.file import File


class Directory:
    """
    @type directory: str
    """
    def __init__(self, directory, path=None):
        if path:
            self.__path = path
        else:
            self.__path = os.getcwd()
        self.__directory = directory

    def directory(self, directory=None):
        if directory:
            self.__directory = directory
            return self
        return self.__directory

    def get_file_list(self):
        files = []
        for item in os.walk(os.path.join(self.__path, self.__directory)):
            path = item[0]
            if item[1]:
                for directory in item[1]:
                    files.append(Directory(directory, path))

            for filename in item[2]:
                files.append(File(filename, path))

            break

        return files
