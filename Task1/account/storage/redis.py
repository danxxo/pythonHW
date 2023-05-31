import redis
import random
from typing import Optional, List
from account.model import Account
from account.storage.protocol import AccountsStorageProtocol
import json


class AccountsRedisStorage(AccountsStorageProtocol):
    def __init__(self):
        self.db_client = redis.Redis(host="localhost", port=6379)
        self.accounts_key = "accounts"
        self.db_client.flushdb()

    def get_all_accounts(self) -> List[Account]:
        account_records = self._get_account_records()
        accounts = []

        for account_data in account_records:
            account = Account.as_dict(account_data)
            accounts.append(account)

        return accounts

    def get_account_by_id(self, account_id: int) -> Optional[Account]:
        account_records = self._get_account_records()

        for account_data in account_records:
            if account_data["id"] == account_id:
                account = Account(**account_data)
                return account

        return None

    def mark_account_as_blocked(self, account_id: int):
        account_records = self._get_account_records()

        for index, account_data in enumerate(account_records):

            if account_data["id"] == account_id:
                account_data["status"] = "blocked"

                updated_account_data_str = json.dumps(account_data)
                updated_account_data = updated_account_data_str.encode("utf-8")

                self.db_client.lset(self.accounts_key, index, updated_account_data)
                break

    def add_account(self) -> int:
        random_id = random.randint(1000, 9999)
        random_phone = f"8910{random_id}"
        account = Account(random_id, random_phone, "password0000")

        account_data = {
            "id": account.id,
            "phone_number": account.phone_number,
            "password": account.password,
            "status": account.status.value,
        }

        serialized_account_data = json.dumps(account_data)
        self.db_client.rpush(self.accounts_key, serialized_account_data)
        return account.id

    def set_account_processing(self, account_id: int) -> None:
        print(f"account {account_id} status to 'processing'")
        account_records = self._get_account_records()

        for index, account_data in enumerate(account_records):

            if account_data["id"] == account_id:
                account_data["status"] = "processing"

                updated_account_data_str = json.dumps(account_data)
                updated_account_data = updated_account_data_str.encode("utf-8")

                self.db_client.lset(self.accounts_key, index, updated_account_data)
                break

    def set_account_pending(self, account_id: int):
        print(f"account {account_id} status to 'pending'")
        account_records = self._get_account_records()

        for index, account_data in enumerate(account_records):

            if account_data["id"] == account_id:
                account_data["status"] = "pending"

                updated_account_data_str = json.dumps(account_data)
                updated_account_data = updated_account_data_str.encode("utf-8")

                self.db_client.lset(self.accounts_key, index, updated_account_data)
                break

    def _get_account_records(self) -> List[dict]:
        account_records = self.db_client.lrange(self.accounts_key, 0, -1)
        return [json.loads(record) for record in account_records]
