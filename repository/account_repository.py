import json
from pathlib import Path

from models.account import Account


class AccountRepository:

    def __init__(self):
        self.file_path = Path("database/accounts.json")

        self.file_path.parent.mkdir(parents=True, exist_ok=True)

        if not self.file_path.exists():
            with open(self.file_path, "w", encoding="utf-8") as file:
                json.dump([], file, indent=4)

    def load(self) -> list[Account]:
        with open(self.file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        return [Account.from_dict(account) for account in data]

    def save(self, accounts: list[Account]) -> None:
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(
                [account.to_dict() for account in accounts],
                file,
                indent=4,
                ensure_ascii=False
            )

    def get_all(self) -> list[Account]:
        return self.load()

    def get_by_id(self, account_id: int) -> Account | None:
        accounts = self.load()

        for account in accounts:
            if account.id == account_id:
                return account

        return None

    def next_id(self) -> int:
        accounts = self.load()

        if not accounts:
            return 1

        return max(account.id for account in accounts) + 1

    def insert(self, account: Account) -> None:
        accounts = self.load()

        account.id = self.next_id()

        accounts.append(account)

        self.save(accounts)

    def update(self, updated_account: Account) -> bool:
        accounts = self.load()

        for index, account in enumerate(accounts):
            if account.id == updated_account.id:
                accounts[index] = updated_account
                self.save(accounts)
                return True

        return False

    def delete(self, account_id: int) -> bool:
        accounts = self.load()

        for account in accounts:
            if account.id == account_id:
                accounts.remove(account)
                self.save(accounts)
                return True

        return False