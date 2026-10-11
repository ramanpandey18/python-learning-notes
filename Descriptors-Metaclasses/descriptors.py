class PositiveInteger:
    def __set_name__(self, owner, name):
        # Python calls this automatically when the class is created
        # name = "balance" → self.name = "_balance"
        self.name = "_" + name

    def __get__(self, instance, owner):
        if instance is None:
            return self  # accessing on the class itself (Account.balance)
        return getattr(instance, self.name)

    def __set__(self, instance, value):
        if not isinstance(value, int) or value <= 0:
            raise ValueError(f"{self.name[1:]} must be a positive int, got {value}")
        setattr(instance, self.name, value)


class Account:
    balance = PositiveInteger()

    def __init__(self, balance):
        self.balance = balance


# Test
acc = Account(100)
print(acc.balance)    # 100

acc.balance = 50
print(acc.balance)    # 50

acc.balance = -10     # ValueError: balance must be a positive int, got -10
