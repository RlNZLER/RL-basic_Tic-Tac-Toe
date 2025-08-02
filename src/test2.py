from collections import Counter

with open("state_values.txt", "r") as f:
    lines = f.readlines()

# Extract just the state keys (before the colon)
keys = [line.split(":")[0].strip() for line in lines]

# Count frequency of each state
counter = Counter(keys)

# Print any state that appears more than once
duplicates = [k for k, v in counter.items() if v > 1]

if duplicates:
    print("Duplicate states found:")
    for d in duplicates:
        print(d)
else:
    print("✅ No duplicate state keys found.")