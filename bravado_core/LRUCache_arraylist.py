def lru_cache_a(maxsize=128):
    if isinstance(maxsize, int) and maxsize <= 0:
        raise TypeError('Expected maxsize to be an integer that bigger than 0')
    if maxsize is not None and not isinstance(maxsize, int):
        raise TypeError('Expected maxsize to be an integer or None')

    cache = {}
    full = False
    cache_len = cache.__len__
    keys = []

    def decorator(user_function):

        if maxsize is None:
            def wrapper(*args, **kwds):
                key = id(args[1])
                try:
                    result = cache[key]
                    return result
                except KeyError:
                    result = user_function(*args, **kwds)
                    cache[key] = result
                    return result
            return wrapper
        else:
            def wrapper(*args, **kwds):
                nonlocal keys, full
                key = id(args[1])
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
