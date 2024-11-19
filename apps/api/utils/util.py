from urllib.parse import urlencode
from django_redis import get_redis_connection

def get_cache_key(base_key, params):
    query_string = urlencode(params)
    return f"{base_key}?{query_string}"


def delete_cache_by_pattern(pattern):
    redis_conn = get_redis_connection()
    keys = redis_conn.scan_iter(f":1:{pattern}")
    for key in keys:
        redis_conn.delete(key)
