class Recipe:
    def __init__(self, recipe):
        self.recipe = recipe

    # def __call__(self, target, prerequisites):
    # self.recipe(target, prerequisites)
    def __call__(self):
        self.recipe()
