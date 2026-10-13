from functools import reduce

#map() applies a function to every item in a list.
numbers = [1, 2, 3, 4, 5, 6]
squared_numbers = list(map(lambda number: number ** 2, numbers))

#filter()
even_numbers = list(filter(lambda number: number%2 == 0, numbers))

#reduce() combines all item into one result
total = reduce(lambda result, number: result + number, numbers)
product = reduce(lambda result, number: result * number, numbers)

print("Original numbers:", numbers)
print("Squared numbers:", squared_numbers)
print("Even numbers:", even_numbers)
print("Sum:", total)
print("Product:", product)
print("Type of numbers:", type(numbers))
print("Is total an integer?", isinstance(total, int))

# Type conversions.
number_text = "25"
converted_integer = int(number_text)
converted_float = float(number_text)

print("String converted to integer:", converted_integer)
print("String converted to float:", converted_float)


