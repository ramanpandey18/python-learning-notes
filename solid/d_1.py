
from abc import ABC, abstractmethod


class OrderRepository(ABC):
    @abstractmethod
    def save(self, order):
        pass


class PostgreSQLRepository(OrderRepository):
    def save(self, order):
        print(f"Saving {order} to PostgreSQL")


class MongoRepository(OrderRepository):
    def save(self, order):
        print(f"Saving {order} to MongoDB")


class InMemoryRepository(OrderRepository):
    def __init__(self):
        self.orders = []

    def save(self, order):
        self.orders.append(order)



class OrderService:
    def __init__(self, repository: OrderRepository):
        self.repository = repository

    def create_order(self, order):
        self.repository.save(order)



order = {"id": 101, "total": 500}

service = OrderService(PostgreSQLRepository())
service.create_order(order)

service = OrderService(MongoRepository())
service.create_order(order)

memory_repository = InMemoryRepository()
service = OrderService(memory_repository)
service.create_order(order)

print(memory_repository.orders)
