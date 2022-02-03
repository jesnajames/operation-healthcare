from dataclasses import dataclass


@dataclass
class RecordNotFoundException(Exception):
    error_description: str
    error_code: int = 404
