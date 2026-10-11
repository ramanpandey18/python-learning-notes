
from abc import ABC, abstractmethod


class PaymentMethod(ABC):
    @abstractmethod
    def refund(self, amount):
        pass


class CreditCardPayment(PaymentMethod):
    def refund(self, amount):
        print(f"Refunding {amount} to credit card")


class CashPayment(PaymentMethod):
    def refund(self, amount):
        raise NotImplementedError(
            "Cash refunds are not supported"
        )


def process_refund(payment: PaymentMethod, amount: float):
    payment.refund(amount)


process_refund(CreditCardPayment(), 100)
process_refund(CashPayment(), 100)
