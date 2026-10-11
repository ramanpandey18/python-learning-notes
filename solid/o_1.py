
from abc import ABC, abstractmethod
#using polymorphism

class PaymentMethod(ABC):
    @abstractmethod
    def pay(self, amount):
        pass

class CreditCardPayment(PaymentMethod):
    def pay(self, amount):
        print(f"Paying {amount} using credit card")


class UPIPayment(PaymentMethod):
    def pay(self, amount):
        print(f"Paying {amount} using UPI")


class PayPalPayment(PaymentMethod):
    def pay(self, amount):
        print(f"Paying {amount} using PayPal")


class PaymentService:
    def __init__(self, payment_method: PaymentMethod):
        self.payment_method = payment_method

    def checkout(self, amount):
        self.payment_method.pay(amount)
