import os
import pandas
from loguru import logger

from Infrastructure.config import ROOT_DIR
from Infrastructure.exceptions import RecordNotFoundException
from Infrastructure.models import TransactionRecord


class TransactionRepository:
    def __init__(self):
        self.source_path = os.path.join(ROOT_DIR, "repositories", "transactions_db.csv")
        self.transactions = pandas.read_csv(filepath_or_buffer=self.source_path, header=[0])

    def get_transaction_record(self, transaction_id: str) -> TransactionRecord:
        for transaction in self.transactions.to_dict(orient="records"):
            if str(transaction["transaction_id"]) == transaction_id:
                return TransactionRecord.parse_obj(transaction)
        else:
            raise RecordNotFoundException(error_description=f"Transaction {transaction_id} not found.")

    def add_transaction_record(self, transaction_record: str):
        with open(self.source_path, "a") as transactions_db:
            transactions_db.write(f"{transaction_record}\n")
            logger.info(f"Transaction record added to repository successfully")
