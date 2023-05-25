from typing import Optional, List

from account.model import Account
from account.storage.protocol import AccountsStorageProtocol


class AccountsRedisStorage(AccountsStorageProtocol):
    def __init__(self):
        ...

    def get_all_accounts(self) -> List[Account]:
        ...
    
    def get_account_by_id(self, account_id: int) -> Optional[Account]:
        ...

    def mark_account_as_blocked(self, account_id: int):
        ...

    def add_account(self) -> int:
        ...

    def set_account_processing(self, account_id: int) -> Optional[Account]:
        ...

    def set_account_pending(self, account_id: int) -> Optional[Account]:
        ...
