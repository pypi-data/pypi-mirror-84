from .target import Target
from .prerequisite import PrerequisiteList
from .recipe import Recipe
from .. import rule_vars


class Rule:
    def __init__(self, target, prerequisites, recipe):
        self.target = Target(target)
        self.prerequisites = PrerequisiteList(prerequisites)
        self.recipe = Recipe(recipe)

    def __contains__(self, target):
        return self.target.match(target)

    def __lt__(self, prerequisite):
        return prerequisite in self.prerequisites

    def run(self):
        if rule_vars.target() is None:
            rule_vars.target << self.target
        rule_vars.prereqs << self.prerequisites
        self.recipe()
