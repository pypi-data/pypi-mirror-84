import abc


class Alias(abc.ABC):
    def __init__(self, name):
        self.name = name

    @property
    @abc.abstractstaticmethod
    def store():
        pass

    def __lshift__(self, value):
        self.store[self.name] = value

    def __repr__(self):
        return str(self.store[self.name])

    def __call__(self):
        return self.store[self.name]
