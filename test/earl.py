import re

words = input("Say something!\n")
p = re.compile("my name is (\w*)", re.IGNORECASE)
matches = p.search(words)
if matches:
    print(f"Hey, {matches[1]}.")
else:
    print("Hey, you.")