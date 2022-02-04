from pydantic import BaseModel


class TransactionMetadata(BaseModel):
    transaction_id: str
    sku_name: str
    sku_price: float
    transaction_datetime: str


class SKUSummary(BaseModel):
    sku_name: str
    total_amount: float


class CategorySummary(BaseModel):
    sku_category: str
    total_amount: float
