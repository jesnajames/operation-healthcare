from datetime import datetime, timedelta
import os
from typing import Dict, List

import pandas

from config import ROOT_DIR


class TransactionJoinsSKU:
    def __init__(self):
        self.transactions_source_path = os.path.join(ROOT_DIR, 'repositories', 'transactions_db.csv')
        self.sku_source_path = os.path.join(ROOT_DIR, 'repositories', 'sku_db.csv')
        self.transactions = pandas.read_csv(filepath_or_buffer=self.transactions_source_path, header=[0])
        self.skus = pandas.read_csv(filepath_or_buffer=self.sku_source_path, header=[0])

    @staticmethod
    def filter_transactions_by_date(transactions: List[Dict], num_of_days: int) -> List[Dict]:
        """
        Returns list of those transactions that occurred in the last n days.
        """
        filtered_transactions = list()
        today = datetime.today()
        start_date = today - timedelta(days=num_of_days)
        for transaction in transactions:
            transaction_date = datetime.strptime(transaction["transaction_datetime"], "%d/%m/%Y")
            if transaction_date.date() >= start_date.date():
                filtered_transactions.append(transaction)
        return filtered_transactions

    def list_transactions(self, filter_query: Dict = None) -> List[Dict]:
        """
        Performs join operation of transactions and SKU information.
        Returns list of either all transactions or those that satisfy provided filter conditions.
        """
        joint_transactions = self.transactions.merge(self.skus).to_dict(orient='records')
        if filter_query["days"]:
            return self.filter_transactions_by_date(joint_transactions, filter_query["days"])
