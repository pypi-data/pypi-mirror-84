from .target import Target
from .recipe import Recipe
from ..globals import rule_vars


class Rule:
    def __init__(self, target, prerequisites, recipe):
        self.target = Target(target, prerequisites)
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

    def run_prerequisites(self, rules):
        for prerequisite in self.target.prerequisites:
            try:
                rule = prerequisite.find_rule(rules)
                # use prerequisite pattern, since it's the definite one
                rule_vars.target << Target(prerequisite.pattern)
                rule_vars.set_prerequistes(rule.target.prerequisites)
                rule.run(rules)
            except ValueError:
                pass

    def run(self, rules):
        self.run_prerequisites(rules)
        if not self.target.is_up_to_date():
            if rule_vars.target() is None:
                rule_vars.target << self.target
            rule_vars.set_prerequistes(self.target.prerequisites)
            self.recipe()
