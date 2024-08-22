
def getValue(redisCli, key):
    v = redisCli.get(key)
    if v is None:
        return None, None
    return v.decode('utf-8'), redisCli.ttl(key)


