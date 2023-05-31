from dataclasses import dataclass
from enum import Enum


class AccountStatus(Enum):
    BLOCKED: str = "blocked"
    PENDING: str = "pending"
    PROCESSING: str = "processing"


@dataclass
class Account:
    id: int
    phone_number: str
    password: str
    status: AccountStatus = AccountStatus.PENDING

    @classmethod
    def as_dict(cls, account_dict: dict):
        match account_dict['status']:
            case 'pending':
                account_status = AccountStatus.PENDING
            case 'blocked':
                account_status = AccountStatus.BLOCKED
            case 'processing':
                account_status = AccountStatus.PROCESSING

        return cls (
            account_dict['id'],
            account_dict['phone_number'],
            account_dict['password'],
            account_status
        )
