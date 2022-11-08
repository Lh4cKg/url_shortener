import uuid
import random


def generate_key(url, length=7, shuffle=False):
    key = str(uuid.uuid5(uuid.NAMESPACE_URL, url))
    if shuffle:
        keys = list(key)
        random.shuffle(keys)
        return ''.join(random.sample(keys, length))

    return key[:length]


async def agenerate_key(url, length=7, shuffle=False):
    key = str(uuid.uuid5(uuid.NAMESPACE_URL, url))
    if shuffle:
        keys = list(key)
        random.shuffle(keys)
        return ''.join(random.sample(keys, length))

    return key[:length]
