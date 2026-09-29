#1
def generate_squares(n):
    for number in range(n + 1):
        yield number ** 2


n = int(input("Enter N: "))

for square in generate_squares(n):
    print(square)

#2
def even_numbers(n):
    for number in range(n + 1):
        if number % 2 == 0:
            yield number


n = int(input("Enter n: "))

print(",".join(map(str, even_numbers(n))))

#3
def divisible_by_3_and_4(n):
    for number in range(n + 1):
        if number % 3 == 0 and number % 4 == 0:
            yield number


n = int(input("Enter n: "))

for number in divisible_by_3_and_4(n):
    print(number)

#4
def squares(a, b):
    for number in range(a, b + 1):
        yield number ** 2


a = int(input("Enter a: "))
b = int(input("Enter b: "))

for square in squares(a, b):
    print(square)

#5
def countdown(n):
    while n >= 0:
        yield n
        n -= 1


n = int(input("Enter n: "))

for number in countdown(n):
    print(number)