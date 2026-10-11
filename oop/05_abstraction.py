"""
PILLAR 4: ABSTRACTION

Definition:
Abstraction exposes the essential operations a caller needs while hiding the
implementation details. An abstract base class can define a contract that concrete
subclasses must implement.

In this example:
- PaymentGateway defines the operation charge().
- StripeGateway and FakePaymentGateway implement that contract differently.
- Checkout code can call charge() without knowing the provider's internal details.

Execution flow:
1. Python prevents direct instantiation of PaymentGateway because charge() is abstract.
2. StripeGateway implements charge().
3. FakePaymentGateway implements charge() for testing.
4. run_payment() uses the abstraction and works with either implementation.
"""

from abc import ABC, abstractmethod


class PaymentGateway(ABC):
    @abstractmethod
    def charge(self, amount: float) -> bool:
        """Return True if the payment succeeds."""
        pass


class StripeGateway(PaymentGateway):
    def charge(self, amount: float) -> bool:
        # A real integration would call the provider's SDK/API here.
        print(f"Stripe processing {amount:.2f}")
        return True


class FakePaymentGateway(PaymentGateway):
    def charge(self, amount: float) -> bool:
        # A deterministic fake is useful in tests; no real money is moved.
        print(f"FAKE gateway processing {amount:.2f}")
        return True


def run_payment(gateway: PaymentGateway, amount: float) -> None:
    # The function depends on the abstract contract, not a concrete provider.
    succeeded = gateway.charge(amount)
    print(f"Payment succeeded: {succeeded}")


run_payment(StripeGateway(), 250.00)
run_payment(FakePaymentGateway(), 75.00)


# Expected output:
# Stripe processing 250.00
# Payment succeeded: True
# FAKE gateway processing 75.00
# Payment succeeded: True
