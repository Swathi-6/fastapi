from redis.asyncio import Redis
from app.config import db_settings

_db = Redis.from_url(url=db_settings.REDIS_URL, decode_responses=True)

async def add_jwti_to_blacklist(jwti: str):
    await _db.set(jwti, "blacklisted")

async def is_jwti_blacklisted(jwti: str):
    return await _db.exists(jwti)

