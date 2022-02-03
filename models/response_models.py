from pydantic import BaseModel
from typing import Optional


class TransactionMetadata(BaseModel):
    transaction_id: str
    sku_name: str
    sku_price: float
    transaction_datetime: str


class TransactionSummary(BaseModel):
    # TODO: Add check to ensure either sku_name or sku_category is present
    sku_name: Optional[str]
    sku_category: Optional[str]
    total_amount: float
