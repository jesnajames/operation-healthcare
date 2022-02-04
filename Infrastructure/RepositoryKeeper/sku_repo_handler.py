import os

import pandas

from Infrastructure.config import ROOT_DIR
from Infrastructure.exceptions import RecordNotFoundException
from Infrastructure.Models import SKURecord


class SKURepository:
    def __init__(self):
        self.source_path = os.path.join(ROOT_DIR, "Repositories", "sku_db.csv")
        self.skus = pandas.read_csv(filepath_or_buffer=self.source_path, header=[0])

    def get_sku_record(self, sku_id: str) -> SKURecord:
        for sku in self.skus.to_dict(orient="records"):
            if str(sku["sku_id"]) == sku_id:
                return SKURecord.parse_obj(sku)
        else:
            raise RecordNotFoundException(error_description=f"Transaction {sku_id} not found.")
