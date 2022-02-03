from typing import Any

from pydantic import BaseModel

from utils import parse_date


class Date(BaseModel):
    # TODO: Validations for date values, eg: 1<date<31
    date: int
    month: int
    year: int

    def __ge__(self, other):
        if isinstance(other, Date):
            if other.date <= self.date and other.month <= self.month and other.year <= self.year:
                return True
        return False

    def __le__(self, other):
        if isinstance(other, Date):
            if other.date >= self.date and other.month >= self.month and other.year >= self.year:
                return True
        return False


class TransactionRecord(BaseModel):
    transaction_id: str
    sku_id: str
    sku_price: float
    transaction_datetime: str
    transaction_date: Date = None

    def __init__(self, **data: Any):
        super().__init__(**data)
        self.transaction_date = Date.parse_obj(parse_date(self.transaction_datetime))


class SKURecord(BaseModel):
    sku_id: str
    sku_name: str
    sku_category: str
