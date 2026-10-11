
class PaymentService:
    def pay(self, payment_method, amount):
        if payment_method == "card":
            print(f"Paying {amount} using credit card")

        elif payment_method == "upi":
            print(f"Paying {amount} using UPI")

        elif payment_method == "paypal":
            print(f"Paying {amount} using PayPal")

        else:
            raise ValueError("Unsupported payment method")
