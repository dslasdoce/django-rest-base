import re
import os
import uuid
import django_rq
import redis
import functools
from django.conf import settings
from Crypto.Cipher import AES


# encryption algorithm
AES_ENCRYPTOR = AES.new(b'WrX2lI4%yV725h3W', AES.MODE_ECB)


# high priority queue
_rq_high_queue = django_rq.get_queue(
    'high',
    result_ttl=5,
    default_timeout=settings.RQ_QUEUES['high']['DEFAULT_TIMEOUT'],
    connection=redis.StrictRedis(
        host=settings.RQ_QUEUES['high']['HOST'],
        port=settings.RQ_QUEUES['high']['PORT'],
        db=settings.RQ_QUEUES['high']['DB'],
    )
)

# low priority queue
_rq_low_queue = django_rq.get_queue(
    'low',
    result_ttl=5,
    default_timeout=settings.RQ_QUEUES['low']['DEFAULT_TIMEOUT'],
    connection=redis.StrictRedis(
        host=settings.RQ_QUEUES['low']['HOST'],
        port=settings.RQ_QUEUES['low']['PORT'],
        db=settings.RQ_QUEUES['low']['DB'],
    ),

)

# default priority queue
_rq_default_queue = django_rq.get_queue(
    'default',
    result_ttl=5,
    default_timeout=settings.RQ_QUEUES['default']['DEFAULT_TIMEOUT'],
    connection=redis.StrictRedis(
        host=settings.RQ_QUEUES['default']['HOST'],
        port=settings.RQ_QUEUES['default']['PORT'],
        db=settings.RQ_QUEUES['default']['DB'],
    )
)


def encrypt_value(value):
    if isinstance(value, int):
        return AES_ENCRYPTOR.encrypt(f'{value:016}'.encode('utf-8')).hex()
    elif isinstance(value, str):
        return AES_ENCRYPTOR.encrypt(value.encode('utf-8')).hex()
    else:
        return value


def rq_default_args_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result_ttl = kwargs.pop('result_ttl', 5)
        kwargs['result_ttl'] = result_ttl
        return func(*args, **kwargs)
    return wrapper


@rq_default_args_decorator
def rq_enqueue(func, *args, **kwargs):
    if not settings.TESTING_MODE:
        _rq_default_queue.enqueue(func, *args, **kwargs)


@rq_default_args_decorator
def rq_enqueue_low(func, *args, **kwargs):
    if not settings.TESTING_MODE:
        _rq_low_queue.enqueue(func, *args, **kwargs)


@rq_default_args_decorator
def rq_enqueue_high(func, *args, **kwargs):
    if not settings.TESTING_MODE:
        _rq_high_queue.enqueue(func, *args, **kwargs)


def file_upload_to(instance, filename):
    """
    This is used for files and images saving if you wish it to have
    a generated filename
    """
    fpath = re.sub(r'[^\w]', '_', instance._meta.db_table).lower()
    ext = filename.split('.')[-1]
    filename = uuid.uuid1().hex
    full_path = os.path.join(fpath, f'{filename}.{ext}')
    return full_path


def copy_attributes(copy_to, copy_from, attributes):
    for attr in attributes:
        setattr(copy_to, attr, getattr(copy_from, attr))
