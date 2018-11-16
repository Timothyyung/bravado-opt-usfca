from _thread import RLock

def _make_key(args, kwds):
    return id(args[1])

def lru_cache(maxsize=128):
    # if isinstance(maxsize, int) and maxsize <= 0:
    #     raise TypeError('Expected maxsize to be an integer that bigger than 0')
    if maxsize is not None and not isinstance(maxsize, int):
        raise TypeError('Expected maxsize to be an integer or None')

    sentinel = object()          # unique object used to signal cache misses
    make_key = _make_key         # build a key from the function arguments
    PREV, NEXT, KEY, RESULT = 0, 1, 2, 3   # names for the link fields

    cache = {}
    full = False
    cache_get = cache.get    # bound method to lookup a key or return None
    cache_len = cache.__len__  # get cache size without calling len()
    lock = RLock()           # because linkedlist updates aren't threadsafe
    root = []                # root of the circular doubly linked list
    root[:] = [root, root, None, None]     # initialize by pointing to self

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
                nonlocal root, full
                key = make_key(args, kwds)
                with lock:
                    link = cache_get(key)
                    if link is not None:
                        link_prev, link_next, _key, result = link
                        link_prev[NEXT] = link_next
                        link_next[PREV] = link_prev
                        last = root[PREV]
                        last[NEXT] = root[PREV] = link
                        link[PREV] = last
                        link[NEXT] = root
                        return result
                result = user_function(*args, **kwds)
                with lock:
                    if key in cache:
                        pass
                    elif full:
                        oldroot = root
                        oldroot[KEY] = key
                        oldroot[RESULT] = result
                        root = oldroot[NEXT]
                        oldkey = root[KEY]
                        oldresult = root[RESULT]
                        root[KEY] = root[RESULT] = None
                        del cache[oldkey]
                        cache[key] = oldroot
                    else:
                        last = root[PREV]
                        link = [last, root, key, result]
                        last[NEXT] = root[PREV] = cache[key] = link
                        full = (cache_len() >= maxsize)
                return result

            return wrapper
    return decorator
