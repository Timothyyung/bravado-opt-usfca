import collections

def _make_key(args, kwds):
    return id(args[1])

def lru_cache_o(maxsize=128):
    if isinstance(maxsize, int) and maxsize <= 0:
        raise TypeError('Expected maxsize to be an integer that bigger than 0')
    if maxsize is not None and not isinstance(maxsize, int):
        raise TypeError('Expected maxsize to be an integer or None')

    sentinel = object()
    make_key = _make_key

    cache = cache = collections.OrderedDict()
    full = False
    cache_get = cache.get
    cache_len = cache.__len__

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
                nonlocal full
                key = make_key(args, kwds)
                try:
                    result = cache.pop(key)
                    cache[key] = result
                    return result
                except KeyError:
                    result = user_function(*args, **kwds)
                    if key in cache:
                        pass
                    elif full:
                        oldresult = cache.popitem(last = False)
                        cache[key] = result
                    else:
                        cache[key] = result
                        full = (cache_len() >= maxsize)
                    return result

            return wrapper
    return decorator
