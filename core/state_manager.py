# core/state_manager.py
import redis
import json
from utils.config import CONFIG

redis_client = redis.from_url(CONFIG["REDIS_URL"], decode_responses=True)

class SessionManager:
    def get_session(self, session_id):
        try:
            data = redis_client.get(f"session:{session_id}")
            if data:
                return json.loads(data)
        except redis.RedisError as e:
            print(f"Redis read error: {e}")
        return {"history": [], "last_appointment": None}

    def save_session(self, session_id, data):
        try:
            redis_client.set(f"session:{session_id}", json.dumps(data), ex=3600*24)
        except redis.RedisError as e:
            print(f"Redis write error: {e}")
