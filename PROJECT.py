from abc import ABC, abstractmethod
import random

class Transaction(ABC):
   
    def __init__(self, amount: float):
        self.amount = amount

    @abstractmethod
    def execute(self, account) -> bool:
        pass


class Deposit(Transaction):
    
    def execute(self, account) -> bool:
        if self.amount <= 0:
            print("Error: Deposit amount must be positive.")
            return False
        account.set_balance(account.get_balance() + self.amount)
        print(f"Successfully deposited ${self.amount:,.2f}")
        return True


class Withdrawal(Transaction):
    
    def execute(self, account) -> bool:
        if self.amount <= 0:
            print("Error: Withdrawal amount must be positive.")
            return False
        if account.get_balance() < self.amount:
            print("Error: Insufficient funds available.")
            return False
        
        account.set_balance(account.get_balance() - self.amount)
        print(f"Successfully withdrew ${self.amount:,.2f}")
        return True



class Account:
    
    def __init__(self, account_number: str, pin: str, initial_balance: float):
        self.__account_number = account_number  
        self.__pin = pin                        
        self.__balance = initial_balance        

    
    def get_account_number(self) -> str:
        return self.__account_number

    def validate_pin(self, input_pin: str) -> bool:
        return self.__pin == input_pin

    def get_balance(self) -> float:
        return self.__balance

    def set_balance(self, amount: float):
        if amount >= 0:
            self.__balance = amount


class Bank:
    
    def __init__(self):
        self.accounts = {}

    def create_account(self, pin: str, initial_balance: float) -> str:
        # Generates a random 6-digit account number string
        acc_num = str(random.randint(100000, 999999))
        while acc_num in self.accounts:
            acc_num = str(random.randint(100000, 999999))
            
        new_account = Account(acc_num, pin, initial_balance)
        self.accounts[acc_num] = new_account
        return acc_num

    def authenticate(self, account_number: str, pin: str) -> Account:
        account = self.accounts.get(account_number)
        if account and account.validate_pin(pin):
            return account
        return None


class ATM:
    
    def __init__(self, bank_system: Bank):
        self.bank = bank_system
        self.current_account = None

    def start(self):
        
        print("=== Welcome to the Bank ATM Stimulation by Bandna :)===")
        while True:
            if not self.current_account:
                self.__show_auth_menu()
            else:
                self.__show_transaction_menu()

    def __show_auth_menu(self):
        print("\n1. Log In\n2. Open New Account\n3. Exit Machine")
        choice = input("Select an option: ").strip()

        if choice == "1":
            acc_num = input("Enter Account Number: ").strip()
            pin = input("Enter 4-Digit PIN: ").strip()
            account = self.bank.authenticate(acc_num, pin)
            if account:
                self.current_account = account
                print(f"Authentication successful! Welcome back.")
            else:
                print("Invalid Account Number or PIN.")

        elif choice == "2":
            pin = input("Create a 4-Digit PIN: ").strip()
            if len(pin) != 4 or not pin.isdigit():
                print("Invalid PIN format. Must be exactly 4 digits.")
                return
            try:
                bal = float(input("Enter Initial Deposit Amount: $"))
                new_id = self.bank.create_account(pin, bal)
                print(f"Account created! Your Account Number is: {new_id}")
            except ValueError:
                print("Invalid monetary amount.")

        elif choice == "3":
            print("Thank you for using our ATM. Goodbye!")
            exit()
        else:
            print("Invalid selection.")

    def __show_transaction_menu(self):
        print(f"\n--- Active Session [{self.current_account.get_account_number()}] ---")
        print("1. Check Balance\n2. Deposit Cash\n3. Withdraw Cash\n4. Log Out")
        choice = input("Select an option: ").strip()

        if choice == "1":
            print(f"Current Balance: ${self.current_account.get_balance():,.2f}")

        elif choice == "2":
            try:
                amt = float(input("Enter deposit amount: $"))
                tx = Deposit(amt)
                tx.execute(self.current_account)
            except ValueError:
                print("Invalid input number format.")

        elif choice == "3":
            try:
                amt = float(input("Enter withdrawal amount: $"))
                tx = Withdrawal(amt)
                tx.execute(self.current_account)
            except ValueError:
                print("Invalid input number format.")

        elif choice == "4":
            print("Session safely closed. Logging out...")
            self.current_account = None
        else:
            print("Invalid selection.")


if __name__ == "__main__":
    central_bank = Bank()
    # Seeding a dummy account: Account number '123456', PIN '9999', balance $500.00
    central_bank.accounts["123456"] = Account("123456", "9999", 500.0)
    
    my_atm = ATM(central_bank)
    my_atm.start()
