from dataclasses import dataclass, field


@dataclass
class Account:
    id: int
    email: str
    password: str
    site: str
    account_type: str
    login_method: str
    items: list[str] = field(default_factory=list)
    notes: str = ""

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "email": self.email,
            "password": self.password,
            "site": self.site,
            "account_type": self.account_type,
            "items": self.items,
            "notes": self.notes,
            "login_method": self.login_method
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data["id"],
            email=data["email"],
            password=data["password"],
            site=data["site"],
            account_type=data["account_type"],
            items=data.get("items", []),
            notes=data.get("notes", ""),
            login_method=data.get("login_method", "")
        )