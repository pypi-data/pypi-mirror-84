import functools

cache = {}

def hash_object(object):
    """
    Calculates hash of an object if it's hashable

    :param object: object to be hashed

    :return: Returns hash of object if it's hashable
             Returns 0 otherwise
    """
    try:
        return hash(object)
    except:
        return 0

def cacheable(func):
    """
    Caches the function's response or returns its previous response
    if it has already been hashed

    Shall be used as a decorator
    """
    @functools.wraps(func)
    def _cacheable(*args, **kwargs):
        global cache
        func_id = id(func)
        _hash = hash((func_id,
                      tuple([hash_object(arg) for arg in args]),
                      frozenset({k: hash_object(v) for k, v in kwargs.items()})))
        if func_id in cache.keys() and _hash in cache[func_id].keys():
            return cache[func_id][_hash]
        value = func(*args, **kwargs)
        if value != None:
            if func_id not in cache.keys():
                cache[func_id] = {}
            cache[func_id][_hash] = value
        return value
    _cacheable._func_id = id(func)
    return _cacheable

def nocache(*funcs):
    """
    Clears the cache of specified functions

    Shall be used as a decorator

    :param funcs: functions whose cache must be cleared
    """
    def _nocache(func):
        def _nocache_wrapper(*args, **kwargs):
            global cache
            for _func in funcs:
                func_id = _func._func_id
                if func_id in cache.keys():
                    del cache[func_id]
            return func(*args, **kwargs)
        return _nocache_wrapper
    return _nocache

def nocacheall(func):
    """
    Clears the cache of all functions

    Shall be used as a decorator
    """
    def _nocacheall(*args, **kwargs):
        global cache
        cache = {}
        return func(*args, **kwargs)
    return _nocacheall