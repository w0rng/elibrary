from redis import Redis


redis = Redis(host="redis", port=6379)

__all__ = [
    "redis",
]