def wrap(item):
    if not isinstance(item, (list, tuple)):
        return [item]
    return item
