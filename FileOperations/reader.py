import csv
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, "..", "employees.csv")
csv_path = os.path.join(script_dir, "employees.csv")
employees = {}
data = {}
columns = {}

with open(csv_path, "r") as file:
    reader = csv.DictReader(file)

    # for row in reader:
    #     print(row)

    # for row in reader:
    #     print(row["name"], row["department"])
    
    # for row in reader:
    #     employees[row["id"]] = row
    
    # for index, row in enumerate(reader, start=1):
    #     data[index] = row
    
    for row in reader:
        for key, value in row.items():
            columns.setdefault(key, []).append(value)

# print(employees)
# print(data)
print(columns)