from .alias import Alias


class MakeAlias(Alias):
    store = {"phony": None}


phony = MakeAlias("phony")
