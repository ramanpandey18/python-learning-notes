import os
from typing import Counter

def read_lines(filepath):
    with open(filepath) as f:
        for line in f:
            yield line

def filter_errors(lines):
    for line in lines:
        if "ERROR" in line:
            yield line

def extract_hour(lines):
    for line in lines:
        # line: "2026-07-30 14:23:01 ERROR Something failed"
        parts = line.split()
        timestamp = parts[1]       # "14:23:01"
        hour = timestamp.split(":")[0]  # "14"
        yield hour

script_dir = os.path.dirname(os.path.abspath(__file__))
log_path = os.path.join(script_dir, "app.log")

# Chaining them together:
lines = read_lines(log_path)
errors = filter_errors(lines)
hours = extract_hour(errors)

# for hour in hours:
#     print(hour)

hour_counts = Counter(hours)
for hour, count in sorted(hour_counts.items()):
    print(f"Hour {hour}: {count} errors")