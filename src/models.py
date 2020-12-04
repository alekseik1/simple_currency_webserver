from typing import List
from pydantic import BaseModel, Field


class ConvertResponse(BaseModel):
    from_: str = Field(..., alias='from')
    to: str
    amount: int
    result: float


class CurrencyRecord(BaseModel):
    source: str
    dest: str
    price: float


class UpdateDataModel(BaseModel):
    new_data: List[CurrencyRecord]
