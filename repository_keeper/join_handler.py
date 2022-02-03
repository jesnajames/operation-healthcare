import os
from typing import Dict

import pandas

from config import ROOT_DIR


class TransactionJoinsSKU:
    def __init__(self):
        self.transactions_source_path = os.path.join(ROOT_DIR, 'repositories', 'transactions_db.csv')
        self.sku_source_path = os.path.join(ROOT_DIR, 'repositories', 'sku_db.csv')
        self.transactions = pandas.read_csv(filepath_or_buffer=self.transactions_source_path, header=[0])
        self.skus = pandas.read_csv(filepath_or_buffer=self.sku_source_path, header=[0])

    def list_transactions(self, filter: Dict = None):
        joint = self.transactions.merge(self.skus)
        return joint.to_dict(orient='records')
