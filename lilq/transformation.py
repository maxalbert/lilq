def get_transformer_for(item):
    if isinstance(item, tuple) and hasattr(item, "_replace"):
        return lambda item, rules: item._replace(**rules)
    elif hasattr(item, "__dict__"):
        return lambda item, rules: item.__dict__.update(**rules)
    else:
        raise NotImplementedError(f"No transformer available for item: {item} (type: {type(item)})")


class Transformation:
    def __init__(self, *, query, rules):
        self.query = query
        self.rules = rules

    def apply(self, item):
        if not self.query.matches(item):
            return item

        func_transformer = get_transformer_for(item)
        transformed_item = func_transformer(item, self.rules)
        return transformed_item
