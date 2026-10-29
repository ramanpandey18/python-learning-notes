import logging
from concurrent.futures import ThreadPoolExecutor
import threading
import time

logging.basicConfig(
    level= logging.DEBUG,
    fotmat="%(asctime)s | %(levelname)s | %(processName)s | %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger(__name__)


class CheckoutService:
    def __init__(self, calculator, repository, notifier):
        self.calculator = calculator
        self.repository = repository
        self.notifier = notifier
        self.pool = ThreadPoolExecutor(max_workers=4)

    def _send_notification(self, order):
        print(f"[{threading.current_thread().name}] Notification task started")

        try:
            self.notifier.send(order)
            print(f"[{threading.current_thread().name}] Notification task completed")
        except Exception:
            logger.exception("Notification failed for order")
            print(f"[{threading.current_thread().name}] Notification task failed")

    def checkout(self, items):
        print("[Main] Checkout started")

        print("[Main] Calculating order total")
        total = self.calculator.calculate_total(items)
        print(f"[Main] Total calculated: {total}")

        order = {
            "items": items,
            "total": total,
            "status": "pending",
        }
        print("[Main] Order created with pending status")

        print("[Main] Saving order to database")
        self.repository.save(order)
        print("[Main] Order saved successfully")

        order["status"] = "success"
        print("[Main] Order status updated to success")

        print("[Main] Submitting notification to background thread")
        self.pool.submit(
            self._send_notification,
            order.copy(),
        )

        print("[Main] Checkout returning response")
        return order


class OrderCalculator:
    def calculate_total(self, items):
        print("[Calculator] Calculating total")
        return sum(
            item["price"] * item["quantity"]
            for item in items
        )


class OrderRepository:
    def save(self, order):
        print(f"[Repository] Saving order: total={order['total']}")


class EmailNotifier:
    def send(self, order):
        print("[Notifier] Preparing to send email")

        # Simulate a slow email operation.
        time.sleep(2)

        print(f"[Notifier] Email sent: status={order['status']}")


checkout = CheckoutService(
    OrderCalculator(),
    OrderRepository(),
    EmailNotifier(),
)

items = [
    {"price": 100, "quantity": 2},
    {"price": 50, "quantity": 1},
]

order = checkout.checkout(items)
print(f"[Main] Final order total: {order['total']}")

# Demonstration only: wait for background tasks before exiting.
checkout.pool.shutdown(wait=True)
print("[Main] Application finished")
