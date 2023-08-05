class Alias:
    store = {"target": None, "first_prerequisite": None, "prerequisites": None}

    def __init__(self, name):
        self.name = name

    def __lshift__(self, value):
        self.store[self.name] = value

    def __repr__(self):
        return str(self.store[self.name])

    def __call__(self):
        return self.store[self.name]


target = Alias("target")
t = Alias("target")

first_prerequisite = Alias("first_prerequisite")
prereq = Alias("first_prerequisite")
fp = Alias("first_prerequisite")
p = Alias("first_prerequisite")

prerequisites = Alias("prerequisites")
prereqs = Alias("prerequisites")
ps = Alias("prerequisites")
