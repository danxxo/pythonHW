import pymongo
import random
from typing import Optional, List
from account.model import Account, AccountStatus
from account.storage.protocol import AccountsStorageProtocol


class AccountsMongoStorage(AccountsStorageProtocol):

    def __init__(self):
        self.db_client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.current_db = self.db_client["pyloungedb"]
        self.collection = self.current_db["users"]
        if self.collection.find():
            self.collection.drop()
            self.collection = self.current_db["users"]

    def __del__(self):
        self.collection.drop()

    def get_all_accounts(self) -> List[Account]:
        list_of_ids = []

        for account in self.collection.find():
            list_of_ids.append(self.get_account_by_id(account["id"]))


        return list_of_ids

    def get_account_by_id(self, account_id: int) -> Optional[Account]:
        account = self.collection.find_one({"id": account_id})
        return Account.as_dict(account)

    def mark_account_as_blocked(self, account_id: int):
        self.collection.find_one_and_update(
            {"id": account_id}, 
            {"$set": {"status": 'blocked'}}
            )

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

    def set_account_processing(self, account_id: int) -> Optional[Account]:
        self.collection.find_one_and_update(
            {"id": account_id}, 
            {"$set": {"status": 'processing'}}
            )

    def set_account_pending(self, account_id: int) -> Optional[Account]:
        self.collection.find_one_and_update(
            {"id": account_id}, 
            {"$set": {"status": 'pending'}}
            )