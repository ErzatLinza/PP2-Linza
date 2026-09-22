from math import sqrt


# Task 1
class StringHandler:
    def __init__(self):
        self.text = ""

    def getString(self):
        self.text = input("Enter a string: ")

    def printString(self):
        print(self.text.upper())


# Tasks 2 and 3
class Shape:
    def area(self):
        return 0


class Square(Shape):
    def __init__(self, length):
        self.length = length

    def area(self):
        return self.length ** 2


class Rectangle(Shape):
    def __init__(self, length, width):
        self.length = length
        self.width = width

    def area(self):
        return self.length * self.width


# Task 4
class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def show(self):
        print(f"({self.x}, {self.y})")

    def move(self, x, y):
        self.x = x
        self.y = y

    def dist(self, other):
        return sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)


# Task 5
class Account:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        if amount <= 0:
            print("Deposit amount must be positive.")
            return False

        self.balance += amount
        print(f"Deposited: {amount}. Balance: {self.balance}")
        return True

    def withdraw(self, amount):
        if amount <= 0:
            print("Withdrawal amount must be positive.")
            return False
        if amount > self.balance:
            print("Withdrawal denied: insufficient balance.")
            return False

        self.balance -= amount
        print(f"Withdrawn: {amount}. Balance: {self.balance}")
        return True


# Task 6
def filter_primes_with_lambda(numbers):
    def is_prime(number):
        return number >= 2 and all(
            number % divisor != 0
            for divisor in range(2, int(number ** 0.5) + 1)
        )

    return list(filter(lambda number: is_prime(number), numbers))


if __name__ == "__main__":
    print("Square area:", Square(5).area())
    print("Rectangle area:", Rectangle(4, 6).area())

    first = Point(1, 2)
    second = Point(4, 6)
    first.show()
    print("Distance:", first.dist(second))
    first.move(10, 20)
    first.show()

    account = Account("KBTU Student", 100)
    account.deposit(50)
    account.withdraw(70)
    account.withdraw(100)  # This withdrawal is rejected.

    print("Prime numbers:", filter_primes_with_lambda([1, 2, 3, 4, 5, 10, 11]))