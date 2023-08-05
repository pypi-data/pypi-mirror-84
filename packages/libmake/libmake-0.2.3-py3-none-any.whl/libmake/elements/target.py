import fnmatch


class Target:
    """Target.

    Note
    ----
    The main goal of this class is to provide an API to be used by MObject, and
    not to be used directly.

    So :meth:`__init__` will be replaced and not used, but it is here as an
    interface to specify the requirements to be fullfilled to be able to use the
    defined API, and on the other side what is available for API development.

    """

    def __init__(self, pattern):
        self.pattern = pattern

    def match(self, target):
        return fnmatch.fnmatch(target, self.pattern)
