import uuid
import random
from calendar import timegm
from datetime import datetime

from django.conf import settings
from django.utils.timezone import is_naive, make_aware, utc


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


def make_utc(dt, ):
    if settings.USE_TZ and is_naive(dt):
        return make_aware(dt, timezone=utc)

    return dt


def datetime_to_epoch(dt):
    return timegm(dt.utctimetuple())


def datetime_from_epoch(ts):
    return make_utc(datetime.utcfromtimestamp(ts))

