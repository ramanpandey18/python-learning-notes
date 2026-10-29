
from abc import ABC, abstractmethod


class PaymentMethod(ABC):
    @abstractmethod
    def pay(self, amount: float) -> None:
        pass


class RefundablePaymentMethod(PaymentMethod):
    @abstractmethod
    def refund(self, amount: float) -> None:
        pass


class CreditCardPayment(RefundablePaymentMethod):
    def pay(self, amount: float) -> None:
        print(f"Charging {amount} to credit card")

    def refund(self, amount: float) -> None:
        print(f"Refunding {amount} to credit card")


class CashPayment(PaymentMethod):
    def pay(self, amount: float) -> None:
        print(f"Accepting {amount} in cash")


def process_refund(payment: RefundablePaymentMethod,amount: float,) -> None:
    payment.refund(amount)


process_refund(CreditCardPayment(), 100)
