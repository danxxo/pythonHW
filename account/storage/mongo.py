#docker run -d -p 27017:27017 --name test-mongo mongo:latest

from typing import Optional, List

from account.model import Account
from account.storage.protocol import AccountsStorageProtocol

import pymongo
import random


class AccountsMongoStorage(AccountsStorageProtocol):
    def __init__(self):
        self.db_client = pymongo.MongoClient("mongodb://localhost:27017/")

        self.current_db = self.db_client["pyloungedb"]

        self.collection = self.current_db["users"]

    def get_all_accounts(self) -> List[Account]:
        ...
    
    def get_account_by_id(self, account_id: int) -> Optional[Account]:
        account = self.collection.find_one({"id" : account_id})
        return account

    def mark_account_as_blocked(self, account_id: int):
        ...

    def add_account(self) -> int:
        random_id = random.randint(1000, 9999)
        random_phone = f'8910{random_id}'

        account = Account(random_id, random_phone, 'password0000')

        self.collection.insert_one({
            "id" : account.id,
            "phone_number" : account.phone_number,
            "password" : account.password,
            "status" : account.status.value
        })

        print(f'account {random_id} created')


    def set_account_processing(self, account_id: int) -> Optional[Account]:
        ...

    def set_account_pending(self, account_id: int) -> Optional[Account]:
        ...



# db_client = pymongo.MongoClient("mongodb://localhost:27017/")

# current_db = db_client["pyloungedb"]

# collection = current_db["users"]

# pylounge = {
#     "id" : 1,
#     "phone_number" : "89101369672",
#     "password" : "popopo"
# }

# ins_result = collection.insert_one(pylounge)
# print(ins_result.inserted_id)
# print(collection.find_one({"id" : 0}))