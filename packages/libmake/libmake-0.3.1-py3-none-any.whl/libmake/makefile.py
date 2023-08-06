from .elements.rule import Rule
from .elements.target import Target
from .elements.prerequisite import Prerequisite
from .globals import rule_vars


class Makefile:
    def __init__(self):
        self.rules = []
        self.default = None

    def add_rule(self, target, prerequisites=None, default=False):
        def get_recipe(recipe):
            rule = Rule(target, prerequisites, recipe)
            if default:
                if self.default is None:
                    self.default = rule
                else:
                    raise ValueError("Only a single default rule is allowed")
            else:
                self.rules.append(rule)

        return get_recipe

    def run_default(self):
        if self.default:
            rule = self.default
        else:
            rule = self.rules[0]

        rule.run(self.rules)

    def run(self, targets):
        if len(targets) == 0:
            self.run_default()
        else:
            for target in targets:
                # start dependency chain: any target is always a prerequisite
                # before, and so also the initial ones
                rule = Prerequisite(target).find_rule(self.rules)
                # update vaariable to be used in recipes
                rule_vars.target << Target(target)
                # to run a rule should determine if any prerequisite should run
                # before
                rule.run(self.rules)
