from models.account import Account
from repository.account_repository import AccountRepository


class AccountService:

    def __init__(self):
        self.repository = AccountRepository()
    def create_account(
        self,
        email: str,
        password: str,
        site: str,
        account_type: str,
        login_method: str,
        items: list[str],
        notes: str = ""
    ) -> Account:

        account = Account(
            id=0,
            email=email,
            password=password,
            site=site,
            account_type=account_type,
            login_method=login_method,
            items=items,
            notes=notes
        )

        self.repository.insert(account)

        return account

    def get_all_accounts(self) -> list[Account]:
        return self.repository.get_all()

    def get_account_by_id(self, account_id: int) -> Account | None:
        return self.repository.get_by_id(account_id)

    def update_account(self, account: Account) -> bool:
        return self.repository.update(account)
    def delete_account(self, account_id: int) -> bool:
        return self.repository.delete(account_id)
