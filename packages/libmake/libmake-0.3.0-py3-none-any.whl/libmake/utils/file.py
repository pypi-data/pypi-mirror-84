import os
import pathlib

from ..globals.make_vars import phony


class File:
    """File.

    Since `pathlib.Path` it implements a weird design pattern, i.e. its
    constructor always return an instance of one of its subclasses,
    according to the platform, it is quite hard to subclass, and so here a
    subclass it's faked, binding all the method not overwritten to the `path`
    member.

    """

    def __init__(self, path):
        if phony() is not None and path in phony():
            raise ValueError("A phony it's forced not to be a path")

        if isinstance(path, File):
            path = path.path
        else:
            try:
                pathlib.Path(path).stat()
            except FileNotFoundError as e:
                try:
                    winerror = e.winerror
                except AttributeError:
                    winerror = None
                new_e = FileNotFoundError(*e.args, e.filename, winerror, e.filename2)
                raise new_e

        self.path = pathlib.Path(path)

    def __getattr__(self, name):
        """Fake a `pathlib.Path` instance

        Redirect not explicitly defined methods, binding them to the `self.path`
        instance.

        Parameters
        ----------
        name : str
            attribute/method name

        """
        return getattr(self.path, name)

    def is_newer(self, path):
        """is_newer.

        a phony is always newer: will always trigger a target when being a
        prerequisite

        if the file does not exist, of course it's not up to date

        Parameters
        ----------
        path :
            path

        .. todo::
            docs
        """
        try:
            f = File(path)
        except updated_prerequisite:
            # phony - file existence check failed
            return False

        t1 = self.stat().st_mtime
        t2 = f.stat().st_mtime

        return t1 > t2

    def __gt__(self, path):
        return self.is_newer(path)

    def __lt__(self, path):
        return not self.__lt__(path)


updated_prerequisite = (ValueError, FileNotFoundError)
