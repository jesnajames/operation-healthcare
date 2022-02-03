from pydantic import BaseModel


class TransactionRecord(BaseModel):
    transaction_id: str
    sku_id: str
    sku_price: float
    transaction_datetime: str
    # TODO: Parse datetime string to Date object


class SKURecord(BaseModel):
    sku_id: str
    sku_name: str
    sku_category: str
