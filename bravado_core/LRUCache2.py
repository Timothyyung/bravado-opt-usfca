import collections

class LRUCache2(collections.OrderedDict):

    def __init__(self, maxsize=128):
        if maxsize is not None and not isinstance(maxsize, int):
            raise TypeError('Expected maxsize to be an integer or None')
        if isinstance(maxsize, int):
            if maxsize <= 0:
                raise TypeError('Expected maxsize to be bigger than 0')
        self.maxsize = maxsize
        self.cache = collections.OrderedDict()
        self.cache_len = self.cache.__len__

    def get(self, key):
        id = make_key(key)

        if self.maxsize is None:
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

        if maxsize is None:
            self.cache[id] = value
        else:
            if self.cache_len() == self.maxsize:
                old_result = self.cache.popitem(last = False)

            self.cache[id] = value

def make_key(key):
    return id(key)
