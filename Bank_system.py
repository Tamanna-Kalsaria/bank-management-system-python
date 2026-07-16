import json
import random
import string
from pathlib import Path

class Bank:
    database = "data.json"
    data = []

    try:
        if Path(database).exists():
            with open(database, "r") as fs:
                content = fs.read().strip()
                data = json.loads(content) if content else []
        else:
            with open(database, "w") as fs:
                json.dump([], fs)

    except Exception as err:
        print(f"An exception occurred: {err}")
        data = []

    @classmethod
    def __update(cls):
        with open(cls.database, "w") as fs:
            json.dump(cls.data, fs, indent=4)

    @classmethod
    def __accountgenerate(cls):
        alpha = random.choices(string.ascii_uppercase, k=3)
        num = random.choices(string.digits, k=3)
        spchar = random.choices("89")

        acc_id = alpha + num + spchar
        random.shuffle(acc_id)

        return "".join(acc_id)

    def Createaccount(self):
        info = {
            "name": input("Tell your name: "),
            "age": int(input("Tell your age: ")),
            "email": input("Tell your email: "),
            "pin": int(input("Tell your 4-digit PIN: ")),
            "accountNo.": Bank.__accountgenerate(),
            "balance": 0
        }

        if info["age"] < 18 or len(str(info["pin"])) != 4:
            print("Sorry, you cannot create an account.")
            return

        Bank.data.append(info)
        Bank.__update()

        print("\nAccount created successfully!")
        for key, value in info.items():
            print(f"{key}: {value}")

    def _authenticate(self):
        accountNo = input("Enter account number: ")
        pin = int(input("Enter PIN: "))

        userdata = [
            i for i in Bank.data
            if i["accountNo."] == accountNo and i["pin"] == pin
        ]

        return userdata[0] if userdata else None

    def depositmoney(self):
        user = self._authenticate()

        if not user:
            print("No user found.")
            return

        amount = int(input("Enter deposit amount: "))

        if amount <= 0 or amount > 10000:
            print("Amount must be between 1 and 10000.")
            return

        user["balance"] += amount
        Bank.__update()

        print("Amount deposited successfully.")
        print("Current Balance:", user["balance"])

    def withdrawmoney(self):
        user = self._authenticate()

        if not user:
            print("No user found.")
            return

        amount = int(input("Enter withdrawal amount: "))

        if amount <= 0:
            print("Invalid amount.")
            return

        if user["balance"] < amount:
            print("Insufficient balance.")
            return

        user["balance"] -= amount
        Bank.__update()

        print("Amount withdrawn successfully.")
        print("Current Balance:", user["balance"])

    def showdetails(self):
        user = self._authenticate()

        if not user:
            print("No user found.")
            return

        print("\nYOUR DETAILS\n")
        for key, value in user.items():
            print(f"{key}: {value}")

    def updatedetails(self):
        user = self._authenticate()

        if not user:
            print("No such user found.")
            return

        print("\nLeave blank to keep old value.\n")

        name = input("New Name: ")
        email = input("New Email: ")
        pin = input("New PIN: ")

        if name:
            user["name"] = name

        if email:
            user["email"] = email

        if pin:
            if len(pin) != 4 or not pin.isdigit():
                print("PIN must be 4 digits.")
                return
            user["pin"] = int(pin)

        Bank.__update()
        print("Details updated successfully.")

    def Delete(self):
        user = self._authenticate()

        if not user:
            print("No such account found.")
            return

        confirm = input("Press Y to delete account: ")

        if confirm.lower() == "y":
            Bank.data.remove(user)
            Bank.__update()
            print("Account deleted successfully.")
        else:
            print("Deletion cancelled.")


user = Bank()

while True:
    print("1. Create Account")
    print("2. Deposit Money")
    print("3. Withdraw Money")
    print("4. Show Details")
    print("5. Update Details")
    print("6. Delete Account")
    print("7. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        user.Createaccount()
    elif choice == "2":
        user.depositmoney()
    elif choice == "3":
        user.withdrawmoney()
    elif choice == "4":
        user.showdetails()
    elif choice == "5":
        user.updatedetails()
    elif choice == "6":
        user.Delete()
    elif choice == "7":
        print("Thank you for using the Bank System")
        break
    else:
        print("Invalid choice.")