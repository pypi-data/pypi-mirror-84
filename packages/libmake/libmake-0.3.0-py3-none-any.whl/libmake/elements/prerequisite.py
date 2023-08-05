class Prerequisite:
    """Prerequisite.

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

    def __repr__(self):
        return self.pattern

    def find_rule(self, rules):
        for rule in rules:
            if self.pattern in rule:
                return rule

        raise ValueError(f"No rule matches the target: {self.pattern}")


class PrerequisiteList(list):
    def __init__(self, prerequisites):
        super().__init__()

        if isinstance(prerequisites, str):
            prerequisites = [prerequisites]

        for prerequisite in prerequisites:
            self.append(Prerequisite(prerequisite))

    def __repr__(self):
        return "- " + "\n- ".join([str(p) for p in self]) + "\n"
