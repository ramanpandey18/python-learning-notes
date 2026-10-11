
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Protocol
from uuid import uuid4


# ---------- Domain model ----------

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


# ---------- SRP: calculate totals ----------

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


# ---------- DIP / OCP: payment abstraction ----------

class PaymentGateway(ABC):
    @abstractmethod
    def charge(self, amount: float) -> bool:
        """Return True if payment succeeds."""
        pass


class StripeGateway(PaymentGateway):
    def charge(self, amount: float) -> bool:
        print(f"Stripe charged {amount:.2f}")
        return True


class RazorpayGateway(PaymentGateway):
    def charge(self, amount: float) -> bool:
        print(f"Razorpay charged {amount:.2f}")
        return True


# ---------- DIP / OCP: persistence abstraction ----------

class OrderRepository(Protocol):
    def save(self, order: Order) -> None:
        ...


class InMemoryOrderRepository:
    def __init__(self):
        self.orders: dict[str, Order] = {}

    def save(self, order: Order) -> None:
        self.orders[order.order_id] = order


# ---------- ISP: focused notification capability ----------

class OrderNotifier(Protocol):
    def send_confirmation(self, order: Order) -> None:
        ...


class EmailNotifier:
    def send_confirmation(self, order: Order) -> None:
        print(f"Email sent for order {order.order_id}")


# ---------- Workflow orchestration ----------

class CheckoutService:
    def __init__(
        self,
        calculator: OrderCalculator,
        gateway: PaymentGateway,
        repository: OrderRepository,
        notifier: OrderNotifier,
    ):
        self.calculator = calculator
        self.gateway = gateway
        self.repository = repository
        self.notifier = notifier

    def checkout(self, items: tuple[Item, ...]) -> Order:
        total = self.calculator.calculate(items)

        if not self.gateway.charge(total):
            raise RuntimeError("Payment failed")

        order = Order(
            order_id=str(uuid4()),
            items=items,
            total=total,
        )

        self.repository.save(order)
        self.notifier.send_confirmation(order)

        return order


# ---------- Composition: wire dependencies ----------

repository = InMemoryOrderRepository()

checkout_service = CheckoutService(
    calculator=OrderCalculator(),
    gateway=StripeGateway(),
    repository=repository,
    notifier=EmailNotifier(),
)

items = (
    Item("Keyboard", 1000.00, 1),
    Item("Mouse", 500.00, 2),
)

order = checkout_service.checkout(items)

print(f"Order total: {order.total:.2f}")
print(f"Orders saved: {len(repository.orders)}")
