import time


USER_DB = {
    "user123": {
        "name": "Priyanshu Tiwari",
        "balance": 1500.50,
        "transactions": [
            {"date": "2024-05-01", "description": "Salary Credit", "amount": 2000.00},
            {"date": "2024-05-03", "description": "Grocery Store", "amount": -150.75},
            {"date": "2024-05-05", "description": "Electricity Bill", "amount": -85.00},
        ],
    }
}


class BankOperations:
    def __init__(self):
        self.users = USER_DB

    def get_balance(self, user_id):
        return self.users.get(user_id, {}).get("balance", 0)

    def transfer_funds(self, from_user, to_user, amount):
        if from_user in self.users and self.users[from_user]["balance"] >= amount:
            self.users[from_user]["balance"] -= amount
            transaction = {
                "date": time.strftime("%Y-%m-%d"),
                "description": f"Transfer to {to_user}",
                "amount": -amount,
            }
            self.users[from_user]["transactions"].append(transaction)
            return True, "Transfer successful"
        return False, "Insufficient funds"
