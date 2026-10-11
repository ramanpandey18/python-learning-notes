# Practice Exercises

Try these in order. Change the code and run it again before checking your reasoning.

## 1. Classes and objects
In `01_classes_objects.py`:
- Create a third Student object.
- Add a `passed()` method that returns `True` when score >= 40.
- Explain why changing one student's score doesn't change the other student's score.

## 2. Encapsulation
In `02_encapsulation.py`:
- Add a `withdraw(amount)` method.
- Reject non-positive withdrawal amounts.
- Reject withdrawals larger than the current balance.
- Keep the balance unchanged when a withdrawal is rejected.

## 3. Inheritance
In `03_inheritance.py`:
- Add a `Tester(Employee)` class.
- Override `work()` to return `"<name> is testing software"`.
- Use `super()` if the subclass needs the base class initialization.

## 4. Polymorphism
In `04_polymorphism.py`:
- Add `PushNotifier` with a `send(message)` method.
- Call `notify_user()` with all three notifier objects.
- Did you need to change `notify_user()`?

## 5. Abstraction
In `05_abstraction.py`:
- Add `RazorpayGateway(PaymentGateway)`.
- Implement `charge()` with the same return contract.
- Pass it to `run_payment()` without changing that function.

## 6. Combined backend example
In `06_combined_checkout.py`:
- Run once with a successful fake payment.
- Set `should_succeed=False` and observe what happens.
- Explain why the order is not saved after a failed payment.
- Add a second repository implementation while keeping `CheckoutService` unchanged.

## Self-check questions
1. What is the difference between a class and an object?
2. How does `@property` help encapsulation?
3. Why should inheritance represent a valid "is-a" relationship?
4. How does duck typing provide polymorphism?
5. Why might a caller depend on an abstract contract rather than a concrete provider?
6. When is composition preferable to inheritance?
