"""
PILLAR 2: INHERITANCE

Definition:
Inheritance lets a child/subclass reuse or specialize behavior from a parent/base
class. Use it when the child genuinely "is a" kind of the parent.

In this example:
- Employee is the base class.
- Developer and Designer are subclasses.
- super().__init__(...) reuses Employee's initialization.

Execution flow:
1. Developer(...) calls Developer.__init__.
2. super().__init__(name) initializes the inherited name attribute.
3. describe() is inherited from Employee.
4. work() is overridden so each subclass provides specialized behavior.
"""


class Employee:
    def __init__(self, name: str):
        self.name = name

    def describe(self) -> str:
        # Shared behavior inherited by subclasses.
        return f"Employee: {self.name}"

    def work(self) -> str:
        # General default behavior; subclasses may specialize it.
        return f"{self.name} is working"


class Developer(Employee):
    def work(self) -> str:
        # Method overriding: specialized behavior for developers.
        return f"{self.name} is writing code"


class Designer(Employee):
    def work(self) -> str:
        return f"{self.name} is designing a user interface"


developer = Developer("Asha")
designer = Designer("Ravi")

print(developer.describe())
print(developer.work())
print(designer.describe())
print(designer.work())


# Expected output:
# Employee: Asha
# Asha is writing code
# Employee: Ravi
# Ravi is designing a user interface
