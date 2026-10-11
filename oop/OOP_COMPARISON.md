# OOP Concepts: Quick Comparison

| Concept | Definition | Key question | Example in this pack |
|---|---|---|---|
| Class | Blueprint for attributes and methods | What structure/behavior do objects share? | `Student` |
| Object | Instance of a class | What concrete instance are we using? | `Student("Asha", 90)` |
| Encapsulation | Bundle state and behavior; control changes to state | How do we protect valid state? | `BankAccount.balance` property |
| Inheritance | Reuse/specialize a base class | Is this truly an "is-a" relationship? | `Developer(Employee)` |
| Polymorphism | Same operation, different implementation behavior | Can the caller use different objects the same way? | `notifier.send(...)` |
| Abstraction | Expose a contract and hide implementation details | What does the caller need to know? | `PaymentGateway.charge()` |
| Composition | Build an object using other objects | Does this object "have-a" component? | `CheckoutService` has a calculator, gateway, and repository |

## Common interview distinctions

### Encapsulation vs abstraction
- Encapsulation is about bundling state/behavior and controlling access to state.
- Abstraction is about exposing essential capabilities while hiding implementation details.

### Inheritance vs polymorphism
- Inheritance is a relationship/mechanism for deriving a class from another.
- Polymorphism is the ability to use different implementations through a common operation.
- Polymorphism can also work through duck typing in Python, without inheritance.

### Abstraction vs abstract class
- Abstraction is the design idea.
- An abstract base class (`ABC`) is one Python tool for expressing a contract.
- `typing.Protocol` is another option for structural typing.

### Inheritance vs composition
- Inheritance: `Developer` is an `Employee`.
- Composition: `CheckoutService` has a `PaymentGateway`.
- Prefer composition when the relationship is "has-a" or when behavior should be swappable.

## Python notes
- `self` refers to the current instance in an instance method.
- `__init__` initializes an instance; it is not technically the method that creates the object.
- `@property` enables controlled attribute-style access.
- `@abstractmethod` marks a method that concrete subclasses must implement.
- Python's type hints are not automatically enforced at runtime.
