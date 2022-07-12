import redis
import mm_constants
class RedisHandler:
    
    def __init__(self):
        print("redis handler init")
        
        host = mm_constants.REDIS_HOST
        
        port = mm_constants.REDIS_PORT
        
        self.redis = redis.Redis(
            host=host,
            port=port
        )
    
    def set(self,key,value):
        self.redis.set(
            key,
            value
        )
    
    def get(self,key):
        return self.redis.get(key)