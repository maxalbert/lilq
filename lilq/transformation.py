class Transformation:
    def __init__(self, *, query, rules):
        self.query = query
        self.rules = rules

    def apply(self, item):
        if self.query.matches(item):
            item.__dict__.update(self.rules)
        return item
