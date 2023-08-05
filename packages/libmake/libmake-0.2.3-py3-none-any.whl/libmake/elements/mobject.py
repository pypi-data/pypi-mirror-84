from anytree import NodeMixin

from .prerequisite import Prerequisite
from .target import Target

from ..utils.file import File


class PrerequisiteList(list):
    def __init__(self, prerequisites):
        super().__init__()

        if isinstance(prerequisites, str):
            prerequisites = [prerequisites]

        for prerequisite in prerequisites:
            self.append(MObject(prerequisite))

    def __repr__(self):
        return "- " + "\n- ".join([str(p) for p in self.prerequisites]) + "\n"


class MObject(Target, Prerequisite, NodeMixin):
    store = {}

    def __init__(self, pattern, parent=None, children=None):
        if pattern in self.store:
            raise
        self.pattern = pattern
        self.prerequisites = None

        if children:
            # a children attribute is needed for exploiting 'anytree'
            self.children = PrerequisiteList(children)
            # reference the previous attribute with a meaningful name
            self.prerequisites = self.children

    def __repr__(self):
        return self.pattern

    def is_up_to_date(self):
        try:
            File(self.pattern)
        except ValueError:
            # if the target it's not a path it's not up-to-date by definition
            return False
