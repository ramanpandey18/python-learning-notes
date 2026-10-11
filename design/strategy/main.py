from abc import ABC, abstractmethod

# ============================================================
# Strategy Interface
# ============================================================

class ShippingStrategy(ABC):
    @abstractmethod
    def calculate(self, weight: float) -> float:
        pass

# ============================================================
# Concrete Strategies
# ============================================================

class StandardShipping(ShippingStrategy):
    def calculate(self, weight: float) -> float:
        return weight * 5

class ExpressShipping(ShippingStrategy):
    def calculate(self, weight: float) -> float:
        return weight * 10

class InternationalShipping(ShippingStrategy):
    def calculate(self, weight: float) -> float:
        return weight * 20

# ============================================================
# Context
# ============================================================

class ShippingService:
    def __init__(self, strategy: ShippingStrategy):
        self.strategy = strategy

    def calculate_shipping(self, weight: float) -> float:
        if weight <= 0:
            raise ValueError("Weight must be greater than 0")
        return self.strategy.calculate(weight)

def main():
    weight = 5
    standard_service = ShippingService(
        StandardShipping()
    )

    express_service = ShippingService(
        ExpressShipping()
    )

    international_service = ShippingService(
        InternationalShipping()
    )

    print(
        "standard:",
        standard_service.calculate_shipping(weight)
    )
    print(
        "express:",
        express_service.calculate_shipping(weight)
    )
    print(
        "international:",
        international_service.calculate_shipping(weight)
    )

if __name__ == "__main__":
    main()

