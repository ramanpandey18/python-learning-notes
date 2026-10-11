# Python OOP Study Pack

A runnable, comment-rich introduction to Python Object-Oriented Programming (OOP).

## What is OOP?

Object-Oriented Programming organizes code around **objects**: values that combine
state (data/attributes) and behavior (methods).

A **class** defines the structure and behavior; an **object** is an instance of that
class.

## Recommended learning order

1. `01_classes_objects.py` — classes, objects, attributes, methods, `self`, `__init__`
2. `02_encapsulation.py` — controlling access to state, properties, validation
3. `03_inheritance.py` — reusing/extending behavior from a base class
4. `04_polymorphism.py` — the same operation behaving differently for different objects
5. `05_abstraction.py` — exposing a contract while hiding implementation details
6. `06_combined_checkout.py` — a small backend example connecting the concepts
7. `OOP_COMPARISON.md` — definitions and differences at a glance
8. `PRACTICE.md` — exercises to check understanding

## Run the examples

Use Python 3.10+ (the examples use only the Python standard library).

From this directory, run one file at a time:

```bash
python 01_classes_objects.py
python 02_encapsulation.py
python 03_inheritance.py
python 04_polymorphism.py
python 05_abstraction.py
python 06_combined_checkout.py
```

Each file includes:
- a specific definition,
- commented code,
- numbered execution-flow steps,
- expected output.

## Important notes

- Python does not enforce private attributes as strictly as some languages. A leading
  underscore (for example, `_balance`) means "internal use by convention".
- `@property` lets you expose an attribute-like interface while validating updates.
- Inheritance models an "is-a" relationship. Prefer composition when a component
  merely "has-a" another component.
- Polymorphism can be achieved through inheritance or duck typing (objects with the
  required method can be used even without a shared parent class).
- Abstraction is not just "using an abstract class"; it is designing around a clear
  contract and hiding unnecessary implementation details.
