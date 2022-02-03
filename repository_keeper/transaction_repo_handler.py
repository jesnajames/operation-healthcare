import os
import pandas
from typing import Dict

from config import ROOT_DIR
from models import TransactionRecord
from exceptions import RecordNotFoundException


class TransactionRepository:
    def __init__(self):
        self.source_path = os.path.join(ROOT_DIR, 'repositories', 'transactions_db.csv')
        self.transactions = pandas.read_csv(filepath_or_buffer=self.source_path, header=[0])

    def get_transaction_record(self, transaction_id: str) -> TransactionRecord:
        for transaction in self.transactions.to_dict(orient="records"):
            if str(transaction["transaction_id"]) == transaction_id:
                return TransactionRecord.parse_obj(transaction)
        else:
            raise RecordNotFoundException(error_description=f"Transaction {transaction_id} not found.")

    def list_transactions(self, filter: Dict = None):
        transactions = self.transactions.to_dict(orient="records")
        return transactions
