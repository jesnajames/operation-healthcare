from typing import Dict


def parse_date(date: str) -> Dict:
    split_date = date.split("/")
    return {"date": split_date[0], "month": split_date[1], "year": split_date[2]}