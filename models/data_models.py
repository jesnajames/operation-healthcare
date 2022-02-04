from datetime import datetime
from typing import Any

from pydantic import BaseModel


class TransactionRecord(BaseModel):
    transaction_id: str
    sku_id: str
    sku_price: float
    transaction_datetime: str
    transaction_date: datetime = None

    def __init__(self, **data: Any):
        super().__init__(**data)
        self.transaction_date = datetime.strptime(self.transaction_datetime, "%d/%m/%Y")


class SKURecord(BaseModel):
    sku_id: str
    sku_name: str
    sku_category: str
