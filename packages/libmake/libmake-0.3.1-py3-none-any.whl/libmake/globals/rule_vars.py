from .alias import Alias


class RuleAlias(Alias):
    store = {
        "target": None,
        "first_prerequisite": None,
        "prerequisites": None,
    }


target = RuleAlias("target")
t = RuleAlias("target")

first_prerequisite = RuleAlias("first_prerequisite")
prereq = RuleAlias("first_prerequisite")
fp = RuleAlias("first_prerequisite")
p = RuleAlias("first_prerequisite")

prerequisites = RuleAlias("prerequisites")
prereqs = RuleAlias("prerequisites")
ps = RuleAlias("prerequisites")


def set_prerequistes(prerequisites):
    if isinstance(prerequisites, str):
        prerequisites = [prerequisites]
    prereqs << prerequisites
    if len(prerequisites) > 0:
        first_prerequisite << prerequisites[0]
