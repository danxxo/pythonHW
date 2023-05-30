import redis
import random
from typing import Optional, List
from account.model import Account
from account.storage.protocol import AccountsStorageProtocol


class AccountsRedisStorage(AccountsStorageProtocol):
    def __init__(self):
        self.db_client = redis.Redis(host='localhost', port=6379, db=0)

    def get_all_accounts(self) -> List[Account]:
        list_of_ids = []
        list_of_accounts = []

        for key in self.db_client.scan_iter("account:*"):
            account_id = int(key.decode().split(":")[1])
            list_of_ids.append(account_id)

        for account_id in list_of_ids:
            list_of_accounts.append(self.get_account_by_id(account_id))

        return list_of_accounts

    def get_account_by_id(self, account_id: int) -> Optional[Account]:
        account_key = f"account:{account_id}"
        if self.db_client.exists(account_key):
            account_data = self.db_client.hgetall(account_key)
            account = Account(
                account_id,
                account_data[b'phone_number'].decode(),
                account_data[b'password'].decode(),
                account_data[b'status'].decode()
            )
            return account
        return None

    def mark_account_as_blocked(self, account_id: int):
        account_key = f"account:{account_id}"
        if self.db_client.exists(account_key):
            self.db_client.hset(account_key, "status", "blocked")

    def add_account(self) -> int:
        random_id = random.randint(1000, 9999)
        random_phone = f'8910{random_id}'
        account_id = random_id
        account = Account(account_id, random_phone, 'password0000')

        account_key = f"account:{account_id}"
        account_data = {
            "id": account.id,
            "phone_number": account.phone_number,
            "password": account.password,
            "status": account.status.value
        }
        self.db_client.hmset(account_key, account_data)

        return account_id

    def set_account_processing(self, account_id: int) -> Optional[Account]:
        account_key = f"account:{account_id}"
        if self.db_client.exists(account_key):
            self.db_client.hset(account_key, "status", "processing")
            return self.get_account_by_id(account_id)
        return None

    def set_account_pending(self, account_id: int) -> Optional[Account]:
        account_key = f"account:{account_id}"
        if self.db_client.exists(account_key):
            self.db_client.hset(account_key, "status", "pending")
            return self.get_account_by_id(account_id)
        return None
