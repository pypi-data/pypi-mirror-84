from .elements.rule import Rule
from .elements.target import Target
from . import rule_vars


class Makefile:
    def __init__(self):
        self.rules = []
        self.default = None

        # to be used inside rules' definition
        self.target = None
        self.prerequisites = None

    def add_rule(self, target, prerequisites, default=False):
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

    def find_rule(self, target):
        for rule in self.rules:
            if target in rule:
                return rule

        raise ValueError(f"No rule matches the target: {target}")

    def run_default(self):
        if self.default:
            rule = self.default
        else:
            rule = self.rules[0]

        rule.run()

    def run(self, targets):
        if len(targets) == 0:
            self.run_default()
        else:
            for target in targets:
                rule = self.find_rule(target)
                rule_vars.target << Target(target)
                rule.run()
