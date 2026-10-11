"""
COMBINED EXAMPLE: OOP PILLARS IN A SMALL BACKEND WORKFLOW

Scenario:
A checkout flow calculates an order total, charges a payment gateway, and saves
the order.

Where the OOP concepts appear:
- Classes/objects: Item, Order, OrderCalculator, repositories and gateways.
- Encapsulation: OrderCalculator owns validation/calculation behavior; Order is
  represented as a dataclass.
- Inheritance: StripeGateway and FakePaymentGateway inherit PaymentGateway.
- Polymorphism: CheckoutService calls gateway.charge() without checking its type.
- Abstraction: PaymentGateway defines the charge() contract.

This example also previews SOLID:
- SRP: calculation, payment, persistence, and orchestration are separated.
- OCP: a new compatible gateway can be added without changing CheckoutService.
- LSP: each gateway must honor the charge() contract.
- ISP: PaymentGateway contains only payment-related behavior.
- DIP: CheckoutService receives the gateway and repository from outside.

Execution flow:
1. Build items.
2. CheckoutService asks OrderCalculator for the total.
3. CheckoutService calls the injected gateway.
4. If payment fails, raise an error and do not save the order.
5. If payment succeeds, create and save the order.
6. Return the order to the caller.

This is a teaching example, not a production-ready payment workflow.
Production systems need idempotency, durable transactions/reconciliation, and
careful handling of failures between charging and saving.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Protocol
from uuid import uuid4


@dataclass(frozen=True)
class Item:
    name: str
    price: float
    quantity: int


@dataclass(frozen=True)
class Order:
    order_id: str
    items: tuple[Item, ...]
    total: float


class OrderCalculator:
    def calculate(self, items: tuple[Item, ...]) -> float:
        if not items:
            raise ValueError("Order cannot be empty")

        for item in items:
            if item.price < 0 or item.quantity <= 0:
                raise ValueError("Invalid item")

        return round(
            sum(item.price * item.quantity for item in items),
            2,
        )


class PaymentGateway(ABC):
    @abstractmethod
    def charge(self, amount: float) -> bool:
        """True means success; False means declined/failed."""
        pass


class StripeGateway(PaymentGateway):
    def charge(self, amount: float) -> bool:
        print(f"Stripe charged {amount:.2f}")
        return True


class FakePaymentGateway(PaymentGateway):
    def __init__(self, should_succeed: bool = True):
        self.should_succeed = should_succeed

    def charge(self, amount: float) -> bool:
        print(f"Fake gateway received charge: {amount:.2f}")
        return self.should_succeed


class OrderRepository(Protocol):
    def save(self, order: Order) -> None:
        ...


class InMemoryOrderRepository:
    def __init__(self):
        self.orders: dict[str, Order] = {}

    def save(self, order: Order) -> None:
        self.orders[order.order_id] = order
        print(f"Saved order {order.order_id}")


class CheckoutService:
    def __init__(
        self,
        calculator: OrderCalculator,
        gateway: PaymentGateway,
        repository: OrderRepository,
    ):
        self.calculator = calculator
        self.gateway = gateway
        self.repository = repository

    def checkout(self, items: tuple[Item, ...]) -> Order:
        total = self.calculator.calculate(items)

        if not self.gateway.charge(total):
            raise RuntimeError("Payment failed; order was not saved")

        order = Order(
            order_id=str(uuid4()),
            items=items,
            total=total,
        )
        self.repository.save(order)
        return order


if __name__ == "__main__":
    items = (
        Item("Keyboard", 1000.00, 1),
        Item("Mouse", 500.00, 2),
    )

    repository = InMemoryOrderRepository()
    service = CheckoutService(
        calculator=OrderCalculator(),
        gateway=FakePaymentGateway(should_succeed=True),
        repository=repository,
    )

    order = service.checkout(items)
    print(f"Checkout complete; total = {order.total:.2f}")
    print(f"Saved order count = {len(repository.orders)}")

    # To practice the failure path, change should_succeed=True to False.
    # The RuntimeError will be raised and the order will not be saved.
