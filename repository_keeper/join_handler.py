import datetime
import os
from copy import deepcopy
from typing import Dict, List

import pandas

from config import ROOT_DIR
from models import Date
from utils import parse_date


class TransactionJoinsSKU:
    def __init__(self):
        self.transactions_source_path = os.path.join(ROOT_DIR, 'repositories', 'transactions_db.csv')
        self.sku_source_path = os.path.join(ROOT_DIR, 'repositories', 'sku_db.csv')
        self.transactions = pandas.read_csv(filepath_or_buffer=self.transactions_source_path, header=[0])
        self.skus = pandas.read_csv(filepath_or_buffer=self.sku_source_path, header=[0])

    def get_start_date(self, days):
        # TODO: Consider month and year for start_date
        current_date = datetime.date.today().strftime("%d/%m/%Y")
        today = Date.parse_obj(parse_date(current_date))
        start_date = deepcopy(today)
        if days < today.date:
            start_date.date = today.date - days
        return start_date

    def filter_transactions_by_date(self, transactions: List[Dict], days: int):
        filtered_transactions = list()
        start_date = self.get_start_date(days)
        for transaction in transactions:
            transaction_date = (Date.parse_obj(parse_date(transaction["transaction_datetime"])))
            if transaction_date >= start_date:
                filtered_transactions.append(transaction)
        return filtered_transactions

    def list_transactions(self, filter_query: Dict = None):
        joint_transactions = self.transactions.merge(self.skus).to_dict(orient='records')
        if filter_query["days"]:
            return self.filter_transactions_by_date(joint_transactions, filter_query["days"])

