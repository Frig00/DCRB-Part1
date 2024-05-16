from collections import OrderedDict


class LocalCache:
    def __init__(self):
        self.cache = OrderedDict()
        self.max_dim = 100

    def set(self, key, value):
        if len(self.cache) >= self.max_dim:
            self.cache.popitem(last=False)
        self.cache[key] = value

    def get_all_items(self):
        return self.cache.items()

    def clear(self):
        self.cache.clear()
