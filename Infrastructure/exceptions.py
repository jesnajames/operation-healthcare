from dataclasses import dataclass


@dataclass
class RecordNotFoundException(Exception):
    error_description: str
    error_code: int = 404


@dataclass
class BadRequestException(Exception):
    error_description: str
    error_code: int = 400
