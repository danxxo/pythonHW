from dataclasses import dataclass
from enum import Enum


class AccountStatus(Enum):
    BLOCKED : str = 'blocked'
    PENDING : str = 'pending'
    PROCESSING : str = 'processing'


@dataclass
class Account:
    id: int
    phone_number: str
    password: str
    status: AccountStatus = AccountStatus.PENDING


