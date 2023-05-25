from account.model import AccountStatus
from account.storage.mock import MockAccountsStorage

from app import AccountManager


def test_main():
    realisations = [MockAccountsStorage]
    for r in realisations:
        am = AccountManager(r())
        am.register_10_accounts()
        am.work_with_2_and_4_accounts()
        am.block_last_account()
        accounts = am.accounts_storage.get_all_accounts()
        assert len(accounts) == 10
        assert accounts[0].status == AccountStatus.PENDING
        assert accounts[1].status == AccountStatus.PROCESSING
        assert accounts[2].status == AccountStatus.PENDING
        assert accounts[3].status == AccountStatus.PROCESSING
        assert accounts[4].status == AccountStatus.PENDING
        assert accounts[5].status == AccountStatus.PENDING
        assert accounts[6].status == AccountStatus.PENDING
        assert accounts[7].status == AccountStatus.PENDING
        assert accounts[8].status == AccountStatus.PENDING
        assert accounts[9].status == AccountStatus.BLOCKED
        print(f'With realisation {r} everything is OK')


if __name__ == '__main__':
    test_main()
