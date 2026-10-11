
class CheckoutService:
    def __init__(self, calculator, repository, notifier):
        self.calculator = calculator
        self.repository = repository
        self.notifier = notifier

    def checkout(self, items):
        total = self.calculator.calculate_total(items)

        order = {
            "items": items,
            "total": total,
        }

        self.repository.save(order)
        self.notifier.send_confirmation(order)

        return order


class OrderCalculator:
    def calculate_total(self, items):
        return sum(
            item["price"] * item["quantity"]
            for item in items
        )


class OrderRepository:
    def save(self, order):
        print("Saving order to database")


class EmailNotifier:
    def send_confirmation(self, order):
        print("Sending order confirmation email")


calculator = OrderCalculator()
repository = OrderRepository()
notifier = EmailNotifier()

checkout = CheckoutService(
    calculator,
    repository,
    notifier,
)

items = [
    {"price": 100, "quantity": 2},
    {"price": 50, "quantity": 1},
]

order = checkout.checkout(items)
print(order["total"])
