from itertools import groupby
from typing import Dict, List

from Infrastructure.models import CategorySummary, SKUSummary, TransactionMetadata
from Infrastructure.repository_keeper import TransactionRepository, SKURepository, TransactionJoinsSKU


class TransactionQueryProcessor:
    @classmethod
    def get_transaction(cls, transaction_id: str) -> TransactionMetadata:
        """
        Gets details of a transaction along with SKU name mapped with SKU ID.
        """
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
        """
        Computes total sum of all transactions' values.
        """
        total_amount = 0
        for transaction in transactions:
            total_amount += transaction.get("sku_price", 0)
        return round(total_amount, 2)

    @classmethod
    def summarize_by_sku(cls, num_of_days: int) -> List[SKUSummary]:
        """
        Fetches transactions performed in the last n days, groups them by SKU ID and computes total value of each group.
        """
        transactions = TransactionJoinsSKU().list_transactions({"days": num_of_days})
        sorted_transactions = sorted(transactions, key=cls.sku_func)
        transaction_summary = list()
        for key, value in groupby(sorted_transactions, cls.sku_func):
            total_amount = cls.aggregate_transaction_amount(list(value))
            sku = SKURepository().get_sku_record(key)
            transaction_summary.append(SKUSummary(sku_name=sku.sku_name, total_amount=total_amount))
        return transaction_summary

    @classmethod
    def summarize_by_category(cls, num_of_days: int) -> List[CategorySummary]:
        """
        Fetches transactions performed in the last n days, groups them by SKU category and
        computes total value of each group.
        """
        transactions = TransactionJoinsSKU().list_transactions({"days": num_of_days})
        sorted_transactions = sorted(transactions, key=cls.category_func)
        transaction_summary = list()
        for key, value in groupby(sorted_transactions, cls.category_func):
            total_amount = cls.aggregate_transaction_amount(list(value))
            transaction_summary.append(CategorySummary(sku_category=key, total_amount=total_amount))
        return transaction_summary
