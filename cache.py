from collections import OrderedDict

class LocalCache:

    # Cache initialization with a max dimension
    def __init__(self):
        self.cache = OrderedDict()
        self.max_dim = 100

    # Control cache does not exceed max dimension
    def set(self, key, value):
        if len(self.cache) >= self.max_dim:
            self.cache.popitem(last=False)
        self.cache[key] = value

    # Get all items in cache
    def get_all_items(self):
        return self.cache.items()

    # Clear cache
    def clear(self):
        self.cache.clear()
