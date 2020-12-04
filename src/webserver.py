import uvicorn
from aioredis import Redis
from fastapi import FastAPI, Query, Depends, HTTPException
from typing import Literal

from models import ConvertResponse, UpdateDataModel
from redis_helper import get_redis, bulk_update, convert_currency

api = FastAPI()


@api.get('/convert')
async def convert(to: str, amount: int, from_: str = Query(..., alias='from'),
                  redis: Redis = Depends(get_redis)) -> ConvertResponse:
    try:
        result = await convert_currency(from_, to, amount, redis)
    except ValueError as e:
        raise HTTPException(422, str(e))
    response_data = {'from': from_, 'to': to, 'amount': amount, 'result': result}
    return ConvertResponse(**response_data)


@api.post('/database')
async def update_db(merge: Literal['0', '1'], new_data: UpdateDataModel,
                    redis: Redis = Depends(get_redis)) -> str:
    await bulk_update(new_data.new_data, redis=redis)
    return 'ok'


if __name__ == '__main__':
    uvicorn.run(api)
