"""
PILLAR / FOUNDATION: CLASSES AND OBJECTS

Definition:
- A class is a blueprint describing data (attributes) and behavior (methods).
- An object is a concrete instance created from a class.
- __init__ initializes a newly created object.
- self refers to the particular instance on which an instance method is called.

Execution flow:
1. Python defines the Student class.
2. Student("Asha", 90) creates an object and calls __init__.
3. self.name and self.score store state on that specific object.
4. Calling describe() passes that object as self automatically.
"""


class Student:
    def __init__(self, name: str, score: int):
        # Instance attributes: each object gets its own values.
        self.name = name
        self.score = score

    def describe(self) -> str:
        # Instance method: behavior that uses this object's state.
        return f"{self.name} scored {self.score}"


# Step 1: create two different objects from the same class.
student_one = Student("Asha", 90)
student_two = Student("Ravi", 82)

# Step 2: call methods on the objects.
print(student_one.describe())
print(student_two.describe())

# Step 3: show that instance state is independent.
student_one.score = 95
print(f"Asha's updated score: {student_one.score}")
print(f"Ravi's score remains: {student_two.score}")


# Expected output:
# Asha scored 90
# Ravi scored 82
# Asha's updated score: 95
# Ravi's score remains: 82
