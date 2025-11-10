#!/usr/bin/python3

language=["C++", "C", "Go", "Nim", "Rust"]

"""
Enumeate() functions adds a counter to an iterable, allowing access to both the index and the item during execution
"""

#gegt both index and element
for index, lang in enumerate(language):
    print(f"Index{index}: {lang}")

#can convert a list to a tuple
print(list(enumerate(language)))

