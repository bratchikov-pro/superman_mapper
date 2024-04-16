import json

from redis import Redis

from dal.entities import Location


class OSMRedisHelper:
    def __init__(self, redis: Redis):
        self.redis = redis

    async def set_location_info(self, chat_id: int, location: Location):
        await self.redis.set(str(chat_id), json.dumps(location))

    async def get_location_by_chat_id(self, chat_id: int) -> Location:
        location_data = await self.redis.get(str(chat_id))
        if location_data:
            return Location(**json.loads(location_data))
