import collections

class LRUCache2(collections.OrderedDict):

    def __init__(self, maxsize=128):
        self.maxsize = maxsize
        self.cache = collections.OrderedDict()
        self.cache_len = self.cache.__len__

    def get(self, key):
        id = make_key(key)

        if self.maxsize == 0:
            return None
        elif self.maxsize is None:
            try:
                return self.cache[id]
            except KeyError:
                return None
        else:
            try:
                value = self.cache.pop(id)
                self.cache[id] = value
                return value
            except KeyError:
                return None

    def add(self, key, value):
        id = make_key(key)

        if self.maxsize > 0:
            if self.cache_len() == self.maxsize:
                old_result = self.cache.popitem(last = False)

            self.cache[id] = value
        elif maxsize is None:
            self.cache[id] = value

def make_key(key):
    return id(key)
