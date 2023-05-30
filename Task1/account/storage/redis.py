from typing import Optional, List
import redis
import random
from account.model import Account
from account.storage.protocol import AccountsStorageProtocol
import json

class AccountsRedisStorage(AccountsStorageProtocol):
    def __init__(self):
        self.db_client = redis.Redis(host='localhost', port=6379)
        self.accounts_key = 'accounts'

    def get_all_accounts(self) -> List[Account]:
        account_records = self.db_client.hgetall(self.accounts_key)
        accounts = []

        for account_id, account_data in account_records.items():
            account_data_str = account_data.decode('utf-8')
            account_data_dict = json.loads(account_data_str)

            account = Account(**account_data_dict)
            accounts.append(account)

        return accounts

    def get_account_by_id(self, account_id: int) -> Optional[Account]:
        account_data = self.db_client.hget(self.accounts_key, account_id)
        if account_data:
            account_data_str = account_data.decode('utf-8')
            account_data_dict = json.loads(account_data_str)
            account = Account(**account_data_dict)
            return account
        return None

    def mark_account_as_blocked(self, account_id: int):
        account_data = self.db_client.hget(self.accounts_key, account_id)
        if account_data:
            account_data_str = account_data.decode('utf-8')
            account_data_dict = json.loads(account_data_str)

            account_data_dict['status'] = 'blocked'

            updated_account_data_str = json.dumps(account_data_dict)
            updated_account_data = updated_account_data_str.encode('utf-8')

            self.db_client.hset(self.accounts_key, account_id, updated_account_data)

    def add_account(self) -> int:
        random_id = random.randint(1000, 9999)
        random_phone = f'8910{random_id}'
        account = Account(random_id, random_phone, 'password0000')

        account_data = {
            'id': account.id,
            'phone_number': account.phone_number,
            'password': account.password,
            'status': account.status.value
        }

        serialized_account_data = json.dumps(account_data)
        self.db_client.hset(self.accounts_key, account.id, serialized_account_data)
        return account.id

    def set_account_processing(self, account_id: int) -> None:
        account_data = self.db_client.hget(self.accounts_key, account_id)
        if account_data:
            account_data_str = account_data.decode('utf-8')
            account_data_dict = json.loads(account_data_str)

            account_data_dict['status'] = 'processing'

            updated_account_data_str = json.dumps(account_data_dict)
            updated_account_data = updated_account_data_str.encode('utf-8')

            self.db_client.hset(self.accounts_key, account_id, updated_account_data)

    def set_account_pending(self, account_id: int):
        account_data = self.db_client.hget(self.accounts_key, account_id)
        if account_data:
            account_data_str = account_data.decode('utf-8')
            account_data_dict = json.loads(account_data_str)

            account_data_dict['status'] = 'pending'

            updated_account_data_str = json.dumps(account_data_dict)
            updated_account_data = updated_account_data_str.encode('utf-8')

            self.db_client.hset(self.accounts_key, account_id, updated_account_data)









































# import redis
# import random
# from typing import Optional, List
# from account.model import Account
# from account.storage.protocol import AccountsStorageProtocol


# class AccountsRedisStorage(AccountsStorageProtocol):
#     def __init__(self):
#         self.db_client = redis.Redis(host='localhost', port=6379, db=0)

#     def get_all_accounts(self) -> List[Account]:
#         list_of_ids = []
#         list_of_accounts = []

#         for key in self.db_client.scan_iter("account:*"):
#             account_id = int(key.decode().split(":")[1])
#             list_of_ids.append(account_id)

#         for account_id in list_of_ids:
#             list_of_accounts.append(self.get_account_by_id(account_id))

#         return list_of_accounts

#     def get_account_by_id(self, account_id: int) -> Optional[Account]:
#         account_key = f"account:{account_id}"
#         if self.db_client.exists(account_key):
#             account_data = self.db_client.hgetall(account_key)
#             account = Account(
#                 account_id,
#                 account_data[b'phone_number'].decode(),
#                 account_data[b'password'].decode(),
#                 account_data[b'status'].decode()
#             )
#             return account
#         return None

#     def mark_account_as_blocked(self, account_id: int):
#         account_key = f"account:{account_id}"
#         if self.db_client.exists(account_key):
#             self.db_client.hset(account_key, "status", "blocked")

#     def add_account(self) -> int:
#         random_id = random.randint(1000, 9999)
#         random_phone = f'8910{random_id}'
#         account_id = random_id
#         account = Account(account_id, random_phone, 'password0000')

#         account_key = f"account:{account_id}"
#         account_data = {
#             "id": account.id,
#             "phone_number": account.phone_number,
#             "password": account.password,
#             "status": account.status.value
#         }
#         self.db_client.hmset(account_key, account_data)

#         return account_id

#     def set_account_processing(self, account_id: int) -> Optional[Account]:
#         account_key = f"account:{account_id}"
#         if self.db_client.exists(account_key):
#             self.db_client.hset(account_key, "status", "processing")
#             return self.get_account_by_id(account_id)
#         return None

#     def set_account_pending(self, account_id: int) -> Optional[Account]:
#         account_key = f"account:{account_id}"
#         if self.db_client.exists(account_key):
#             self.db_client.hset(account_key, "status", "pending")
#             return self.get_account_by_id(account_id)
#         return None
