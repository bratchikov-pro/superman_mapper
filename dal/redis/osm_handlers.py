import json

from redis import Redis

from dal.entities import Location, Node


class OSMRedisHelper:
    def __init__(self, redis: Redis):
        self.redis = redis

    async def set_location_info(self, chat_id: int, location: Location):
        return self.redis.hset(str(chat_id), key="location", value=json.dumps({
            "latitude": location.latitude,
            "longitude": location.longitude,
            "search_distance": location.search_distance,
        }))

    def get_location_by_chat_id(self, chat_id: int) -> Location:
        location_data = self.redis.hget(str(chat_id), "location")
        if location_data:
            return Location(**json.loads(location_data))

    async def set_user_choice(self, chat_id: int, choice: Node):
        return self.redis.hset(str(chat_id), key="choice", value=json.dumps({
            "name": choice.name,
            "latitude": choice.latitude,
            "longitude": choice.longitude,
        }))

    def get_choice_by_chat_id(self, chat_id: str) -> Node:
        choice_data = self.redis.hget(chat_id, "choice")
        if choice_data:
            return Node(**json.loads(choice_data))
