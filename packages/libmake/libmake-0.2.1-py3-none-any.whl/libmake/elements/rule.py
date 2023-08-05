from .mobject import MObject
from .recipe import Recipe
from ..globals import rule_vars


class Rule:
    def __init__(self, target, prerequisites, recipe):
        self.target = MObject(target, children=prerequisites)
        self.recipe = Recipe(recipe)

    def __contains__(self, target):
        """Match given target with the target pattern of Rule.

        Tell the caller if the definite target he's looking for match the
        abstract one assigned to the current rule.

        Parameters
        ----------
        target : str
            definite target

        Returns
        -------
        bool

        """
        return self.target.match(target)

    def __lt__(self, prerequisite):
        """Match given target in prerequisites of Rule.

        Tell the caller if the definite prerequisite he's looking for match any
        abstract prerequisite of the current rule.

        Parameters
        ----------
        prerequisite : str
            definite prerequisite

        Returns
        -------
        bool

        """
        return prerequisite in self.target.prerequisites

    def run(self):
        if rule_vars.target() is None:
            rule_vars.target << self.target
        rule_vars.prereqs << self.target.prerequisites
        self.recipe()
