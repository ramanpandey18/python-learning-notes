
class PostgreSQLRepository:
    def save(self, order):
        print(f"Saving {order} to PostgreSQL")


class OrderService:
    def __init__(self):
        self.repository = PostgreSQLRepository()

    def create_order(self, order):
        self.repository.save(order)

