class Prerequisite:
    def __init__(self, prerequisite):
        self.prerequisite = prerequisite

    def __repr__(self):
        return self.prerequisite


class PrerequisiteList:
    def __init__(self, prerequisites):
        self.prerequisites = []

        if isinstance(prerequisites, str):
            prerequisites = [prerequisites]

        for prerequisite in prerequisites:
            self.prerequisites.append(Prerequisite(prerequisite))

    def __repr__(self):
        return "- " + "\n- ".join([str(p) for p in self.prerequisites]) + "\n"

    def __contains__(self, prerequisite):
        return prerequisite in self.prerequisites
