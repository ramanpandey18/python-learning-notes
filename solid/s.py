class OrderService:
    def calculate_total(self, items):
        return sum(item["price"] * item["quantity"]
                   for item in items)

    def save_to_database(self, order):
        print("Saving order to database")

    def send_email(self, order):
        print("Sending order confirmation email")
