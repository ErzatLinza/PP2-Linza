"""Task 14 — importing and using functions from another Python file."""

from functions import (
    filter_prime,
    grams_to_ounces,
    has_33,
    reverse_sentence,
    sphere_volume,
)


print(grams_to_ounces(250))
print(filter_prime([1, 2, 3, 4, 5, 6, 7]))
print(reverse_sentence("We are ready"))
print(has_33([1, 3, 3]))
print(sphere_volume(5))
