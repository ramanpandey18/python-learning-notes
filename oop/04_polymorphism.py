"""
PILLAR 3: POLYMORPHISM

Definition:
Polymorphism means "many forms": the same operation can work with different object
types, while each object provides its own behavior.

This example uses duck typing:
Python does not require EmailNotifier and SMSNotifier to inherit from the same
parent. If an object provides send(message), it can be used by notify_user().

Execution flow:
1. notify_user(email, message) calls email.send(message).
2. EmailNotifier.send prints an email-specific message.
3. notify_user(sms, message) calls sms.send(message).
4. SMSNotifier.send prints an SMS-specific message.
5. The caller uses the same function without checking the concrete class.
"""


class EmailNotifier:
    def send(self, message: str) -> None:
        print(f"EMAIL: {message}")


class SMSNotifier:
    def send(self, message: str) -> None:
        print(f"SMS: {message}")


def notify_user(notifier, message: str) -> None:
    # Polymorphic call: behavior depends on the actual object's send() method.
    notifier.send(message)


email = EmailNotifier()
sms = SMSNotifier()

notify_user(email, "Your order has shipped")
notify_user(sms, "Your verification code is 123456")


# Expected output:
# EMAIL: Your order has shipped
# SMS: Your verification code is 123456
