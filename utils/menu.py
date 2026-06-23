from models.account import Account
from services.account_service import AccountService


class Menu:

    def __init__(self):
        self.service = AccountService()

    def run(self):
        while True:
            self.show_menu()

            option = input("Escolha uma opção: ")

            match option:
                case "1":
                    self.create_account()

                case "2":
                    self.list_accounts()

                case "3":
                    self.update_account()

                case "4":
                    self.delete_account()

                case "0":
                    print("\nAté logo!")
                    break

                case _:
                    print("\nOpção inválida!")

            input("\nPressione ENTER para continuar...")

    def show_menu(self):
        print("\n" + "=" * 40)
        print("      ACCOUNT MANAGER")
        print("=" * 40)
        print("1 - Cadastrar conta")
        print("2 - Listar contas")
        print("3 - Editar conta")
        print("4 - Excluir conta")
        print("0 - Sair")
        print("=" * 40)

    def create_account(self):
        print("\n=== Nova Conta ===")

        email = input("Email: ")
        login_method = input( "Método de login (EMAIL_PASSWORD, GOOGLE, MICROSOFT, STEAM...): ").upper()
        password = ""
        if login_method == "EMAIL_PASSWORD":
            password = input("Senha: ")
        site = input("Site: ")
        account_type = input("Tipo: ")
        items = []

        while True:
            item = input("Item (ENTER para finalizar): ")

            if item == "":
                break

            items.append(item)

        notes = input("Observações: ")

        self.service.create_account(
            email=email,
            password=password,
            site=site,
            account_type=account_type,
            login_method=login_method,
            items=items,
            notes=notes
        )
        print("\nConta cadastrada com sucesso!")

    def list_accounts(self):
        accounts = self.service.get_all_accounts()

        if not accounts:
            print("\nNenhuma conta cadastrada.")
            return

        print()

        for account in accounts:
            print("-" * 40)
            print(f"ID: {account.id}")
            print(f"Site: {account.site}")
            print(f"Email: {account.email}")
            print(f"Senha: {account.password}")
            print(f"Tipo: {account.account_type}")
            print(f"Método de Login: {account.login_method}")

            if account.items:
                print("Itens:")

                for item in account.items:
                    print(f"  - {item}")

            if account.notes:
                print(f"Observações: {account.notes}")

        print("-" * 40)

    def update_account(self):
        account_id = int(input("\nID da conta: "))

        account = self.service.get_account_by_id(account_id)

        if account is None:
            print("\nConta não encontrada.")
            return

        print("\nDeixe vazio para manter o valor atual.")

        email = input(f"Email ({account.email}): ") or account.email
        password = input(f"Senha ({account.password}): ") or account.password
        site = input(f"Site ({account.site}): ") or account.site
        account_type = input(f"Tipo ({account.account_type}): ") or account.account_type
        notes = input(f"Observações ({account.notes}): ") or account.notes

        account.email = email
        account.password = password
        account.site = site
        account.account_type = account_type
        account.notes = notes

        self.service.update_account(account)

        print("\nConta atualizada com sucesso!")

    def delete_account(self):
        account_id = int(input("\nID da conta: "))

        if self.service.delete_account(account_id):
            print("\nConta removida com sucesso!")
        else:
            print("\nConta não encontrada.")