"""
PILLAR 1: ENCAPSULATION

Definition:
Encapsulation bundles data and the methods that operate on it, while controlling
how that data is accessed or changed.

Python convention:
- _balance means "internal; do not access directly from outside".
- @property exposes a controlled, attribute-like interface.
Python does not make a single underscore truly private; it communicates intent.

Why it matters:
If callers can set an account balance to any value, invalid states can be introduced.
A property lets the class validate changes in one place.

Execution flow:
1. BankAccount(100) initializes _balance to 100.
2. Reading account.balance invokes the getter.
3. Setting account.balance = 150 invokes the setter and validates the value.
4. Setting a negative balance raises ValueError.
"""


class BankAccount:
    def __init__(self, opening_balance: float):
        if opening_balance < 0:
            raise ValueError("Opening balance cannot be negative")
        self._balance = opening_balance

    @property
    def balance(self) -> float:
        # Getter: callers can read the balance through a controlled interface.
        return self._balance

    @balance.setter
    def balance(self, new_balance: float) -> None:
        # Setter: validate before updating the internal state.
        if new_balance < 0:
            raise ValueError("Balance cannot be negative")
        self._balance = new_balance

    def deposit(self, amount: float) -> None:
        # Business operation: validate the operation as well.
        if amount <= 0:
            raise ValueError("Deposit must be positive")
        self._balance += amount


account = BankAccount(100)

print(f"Opening balance: {account.balance:.2f}")
account.deposit(25)
print(f"After deposit: {account.balance:.2f}")

# This assignment is routed through the property setter.
account.balance = 150
print(f"After controlled update: {account.balance:.2f}")

# Uncomment to see validation fail:
# account.balance = -10


# Expected output:
# Opening balance: 100.00
# After deposit: 125.00
# After controlled update: 150.00
