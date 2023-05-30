import random
from typing import Optional, List

import psycopg2
from psycopg2.extras import DictCursor

from account.model import Account, AccountStatus
from account.storage.protocol import AccountsStorageProtocol


class AccountsPostgresStorage(AccountsStorageProtocol):
    def __init__(self):
        self.conn = psycopg2.connect(
            host='localhost',
            port=5432,
            database='maga',
            user='maga142rus',
            password='maga142rus'
        )
        self._create_table()


    def _create_table(self):
        with self.conn.cursor() as cursor:
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    phone_number VARCHAR(15) NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    status VARCHAR(10) NOT NULL
                )
                """
            )
            self.conn.commit()


    def _drop_table(self):
        with self.conn.cursor() as cursor:
            cursor.execute("DROP TABLE IF EXISTS users")
            self.conn.commit()


    def __del__(self):
        self._drop_table()


    def get_all_accounts(self) -> List[Account]:
        accounts = []

        with self.conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute("SELECT * FROM users")
            rows = cursor.fetchall()
            for row in rows:
                account = Account(
                    id=row['id'],
                    phone_number=row['phone_number'],
                    password=row['password'],
                    status=AccountStatus(row['status'])
                )
                accounts.append(account)

        return accounts
        

    def mark_account_as_blocked(self, account_id: int):
        with self.conn.cursor() as cursor:
            cursor.execute("UPDATE users SET status = %s WHERE id = %s", (AccountStatus.BLOCKED.value, account_id))
            self.conn.commit()

    def add_account(self) -> int:
        random_id = random.randint(1000, 9999)
        random_phone = f'8910{random_id}'
        account = Account(random_id, random_phone, 'password0000', AccountStatus.PENDING)
        
        with self.conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO users (id, phone_number, password, status) VALUES (%s, %s, %s, %s)",
                (account.id, account.phone_number, account.password, account.status.value)
            )
            self.conn.commit()
        
        return account.id

    def set_account_processing(self, account_id: int) -> Optional[Account]:
        with self.conn.cursor() as cursor:
            cursor.execute("UPDATE users SET status = %s WHERE id = %s", (AccountStatus.PROCESSING.value, account_id))
            self.conn.commit()

    def set_account_pending(self, account_id: int) -> Optional[Account]:
        with self.conn.cursor() as cursor:
            cursor.execute("UPDATE users SET status = %s WHERE id = %s", (AccountStatus.PENDING.value, account_id))
            self.conn.commit()
