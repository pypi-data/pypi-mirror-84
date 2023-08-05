import fnmatch


class Target:
    def __init__(self, target):
        self.target = target

    def __repr__(self):
        return self.target

    def match(self, target):
        return fnmatch.fnmatch(target, self.target)
