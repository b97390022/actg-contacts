import redis


class RedisClient:
    def __init__(self, password: str = None, db: int = 0) -> None:
        self.redis_url = "redis://redis:6379"
        self.password = password
        self.db = db

    def get_client(self):
        return redis.from_url(
            url=self.redis_url,
            db=self.db,
            decode_responses=True,
            password=self.password,
        )

    def set(self, key, value):
        with self.get_client() as redis_client:
            return redis_client.set(key, value)

    def get(self, key):
        with self.get_client() as redis_client:
            return redis_client.get(key)

    def delete(self, key):
        with self.get_client() as redis_client:
            return redis_client.delete(key)
