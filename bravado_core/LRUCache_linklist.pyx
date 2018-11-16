def lru_cache_l(maxsize):
    try:
        if maxsize <= 0:
            raise TypeError('Expected maxsize to be an integer that bigger than 0')
        lru_cache_l_inner(maxsize)
    except TypeError:
        raise TypeError('Expected maxsize to be an integer that bigger than 0')

def lru_cache_l_inner(int maxsize=128):
    #if maxsize <= 0:
        #raise TypeError('Expected maxsize to be an integer that bigger than 0')
    #if maxsize is not None and not isinstance(maxsize, int):
        #raise TypeError('Expected maxsize to be an integer or None')

    cdef int PREV, NEXT, KEY, RESULT
    cdef dict cache
    cdef bint full
    cdef cache_len
    cdef list root

    PREV = 0
    NEXT = 1
    KEY = 2
    RESULT = 3

    #PREV, NEXT, KEY, RESULT = 0, 1, 2, 3

    cache = {}
    full = False
    cache_len = cache.__len__
    root = []
    root[:] = [root, root, None, None]

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
                nonlocal root, full
                key = id(args[1])
                try:
                    link = cache[key]
                    link_prev, link_next, _key, result = link
                    link_prev[NEXT] = link_next
                    link_next[PREV] = link_prev
                    last = root[PREV]
                    last[NEXT] = root[PREV] = link
                    link[PREV] = last
                    link[NEXT] = root
                    return result
                except KeyError:
                    result = user_function(*args, **kwds)
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
