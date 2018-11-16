def _make_key(args, kwds):
    return id(args[1])

def lru_cache_a(maxsize=128):
    if isinstance(maxsize, int) and maxsize <= 0:
        raise TypeError('Expected maxsize to be an integer that bigger than 0')
    if maxsize is not None and not isinstance(maxsize, int):
        raise TypeError('Expected maxsize to be an integer or None')

    sentinel = object()
    make_key = _make_key

    cache = {}
    full = False
    cache_get = cache.get
    cache_len = cache.__len__
    keys = []

    def decorator(user_function):

        if maxsize is None:
            def wrapper(*args, **kwds):
                key = make_key(args, kwds)
                result = cache_get(key, sentinel)
                if result is not sentinel:
                    return result
                result = user_function(*args, **kwds)
                cache[key] = result
                return result
            return wrapper
        else:
            def wrapper(*args, **kwds):
                nonlocal keys, full
                key = make_key(args, kwds)
                try:
                    result = cache[key]
                    keys.remove(key)
                    keys.insert(0, key)
                    return result
                except KeyError:
                    result = user_function(*args, **kwds)
                    if key in cache:
                        pass
                    elif full:
                        oldkey = keys.pop()
                        cache.pop(oldkey)
                        cache[key] = result
                        keys.insert(0, key)
                    else:
                        cache[key] = result
                        keys.insert(0, key)
                        full = (cache_len() >= maxsize)
                    return result

            return wrapper
    return decorator
