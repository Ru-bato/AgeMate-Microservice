import redis

def get_redis_client():
    """Initialize and return a Redis client."""
    return redis.Redis(host='localhost', port=6379, db=0)