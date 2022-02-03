from itertools import groupby
from typing import Dict, List

from models import TransactionSummary, TransactionMetadata
from repository_keeper import TransactionRepository, SKURepository, TransactionJoinsSKU


class TransactionQueryProcessor:
    @classmethod
    def get_transaction(cls, transaction_id: str) -> TransactionMetadata:
        transaction = TransactionRepository().get_transaction_record(transaction_id)
        sku = SKURepository().get_sku_record(transaction.sku_id)
        return TransactionMetadata(
            transaction_id=transaction.transaction_id,
            sku_name=sku.sku_name,
            sku_price=transaction.sku_price,
            transaction_datetime=transaction.transaction_datetime
        )

    @classmethod
    def sku_func(cls, t: Dict):
        return t["sku_id"]

    @classmethod
    def category_func(cls, t: Dict):
        return t["sku_category"]

    @classmethod
    def aggregate_transaction_amount(cls, transactions: List) -> float:
        total_amount = 0
        for transaction in transactions:
            total_amount += transaction.get("sku_price", 0)
        return round(total_amount, 2)

    @classmethod
    def summarize_by_sku(cls, duration: int) -> List[TransactionSummary]:
        transactions = TransactionJoinsSKU().list_transactions({"days": duration})
        sorted_transactions = sorted(transactions, key=cls.sku_func)
        transaction_summary = list()
        for key, value in groupby(sorted_transactions, cls.sku_func):
            total_amount = cls.aggregate_transaction_amount(list(value))
            sku = SKURepository().get_sku_record(key)
            transaction_summary.append(TransactionSummary(sku_name=sku.sku_name, total_amount=total_amount))
        return transaction_summary

    @classmethod
    def summarize_by_category(cls, duration: int) -> List[TransactionSummary]:
        transactions = TransactionJoinsSKU().list_transactions({"days": duration})
        sorted_transactions = sorted(transactions, key=cls.category_func)
        transaction_summary = list()
        for key, value in groupby(sorted_transactions, cls.category_func):
            total_amount = cls.aggregate_transaction_amount(list(value))
            transaction_summary.append(TransactionSummary(sku_category=key, total_amount=total_amount))
        return transaction_summary
