import pathlib

from ..globals.make_vars import phony


class File(pathlib.Path):
    def __init__(self, path):
        if path in phony():
            raise ValueError("A phony it's forced not to be a path")
        super().__init__(path)

    def is_newer(self, path):
        try:
            f = File(path)
        except ValueError:
            # a phony is always newer: will always trigger a target when being a
            # prerequisite
            return False

        t1 = self.stat().st_mtime
        t2 = f.stat().st_mtime

        return t1 > t2

    def __lt__(self, path):
        return self.is_newer(path)

    def __gt__(self, path):
        return not self.__lt__(path)
