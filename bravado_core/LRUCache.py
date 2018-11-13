class LRUCache(object):

    def __init__(self, maxsize = 128):
        if maxsize is not None and not isinstance(maxsize, int):
            raise TypeError('Expected maxsize to be an integer or None')
        self.maxsize = maxsize
        self.cache = {}
        self.cache_len = self.cache.__len__
        self.key = []

    def get(self, key):
        id = make_key(key)

        if self.maxsize is None:
            try:
                return self.cache[id]
            except KeyError:
                return None
        elif self.maxsize is None:
            return None
        else:
            try:
                result = self.cache[id]
                self.key.remove(id)
                self.key.insert(0, id)
                return result
            except KeyError:
                return None

    def add(self, key, value):
        id = make_key(key)

        if self.maxsize is None:
            self.cache[id] = value
        elif self.maxsize > 0:
            if self.cache_len() == self.maxsize:
                old_key = self.key.pop()
                self.cache.pop(old_key)

            self.cache[id] = value
            self.key.insert(0, id)


def make_key(key):
    return id(key)
