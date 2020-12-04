from aioredis import Redis, create_redis_pool
from typing import List, Tuple


from models import CurrencyRecord


async def get_redis() -> Redis:
    pool = await create_redis_pool(f'redis://localhost')
    try:
        yield pool
    finally:
        pool.close()
        await pool.wait_closed()


async def get_currency(key: Tuple[str, str], redis: Redis) -> float:
    coeff = await redis.get(str(key), encoding='utf-8')
    if coeff is None:
        raise ValueError(f'Pair {key} not found in database')
    return float(coeff)


async def convert_currency(source: str, dest: str, amount: int, redis: Redis) -> float:
    curr = await get_currency(key=(source, dest), redis=redis)
    return amount * curr


async def bulk_update(new_data: List[CurrencyRecord], redis: Redis):
    tr = redis.multi_exec()
    for one_line in new_data:
        tr.set(str((one_line.source, one_line.dest)), one_line.price)
        tr.set(str((one_line.dest, one_line.source)), 1./one_line.price)
    await tr.execute()
