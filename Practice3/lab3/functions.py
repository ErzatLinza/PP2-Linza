"""LAB 3 — Python Function tasks 1–13."""

import math
import random
from itertools import permutations


# Task 1
def grams_to_ounces(grams):
    return grams / 28.3495231


# Task 2
def fahrenheit_to_centigrade(fahrenheit):
    return (5 / 9) * (fahrenheit - 32)


# Task 3
def solve(numheads, numlegs):
    rabbits = (numlegs - 2 * numheads) // 2
    chickens = numheads - rabbits

    if chickens < 0 or rabbits < 0 or 2 * chickens + 4 * rabbits != numlegs:
        return None
    return chickens, rabbits


def is_prime(number):
    if number < 2:
        return False
    for divisor in range(2, int(number ** 0.5) + 1):
        if number % divisor == 0:
            return False
    return True


# Task 4
def filter_prime(numbers):
    return [number for number in numbers if is_prime(number)]


# Task 5
def print_permutations(text):
    for item in permutations(text):
        print("".join(item))


# Task 6
def reverse_sentence(sentence):
    return " ".join(sentence.split()[::-1])


# Task 7
def has_33(nums):
    return any(nums[index] == 3 and nums[index + 1] == 3
               for index in range(len(nums) - 1))


# Task 8
def spy_game(nums):
    needed = [0, 0, 7]
    position = 0

    for number in nums:
        if number == needed[position]:
            position += 1
            if position == len(needed):
                return True
    return False


# Task 9
def sphere_volume(radius):
    return (4 / 3) * math.pi * radius ** 3


# Task 10
def unique_elements(items):
    result = []
    for item in items:
        if item not in result:
            result.append(item)
    return result


# Task 11
def is_palindrome(text):
    cleaned = "".join(character.lower() for character in text
                      if character.isalnum())
    return cleaned == cleaned[::-1]


# Task 12
def histogram(numbers):
    for number in numbers:
        print("*" * number)


# Task 13
def guess_the_number():
    name = input("Hello! What is your name?\n")
    secret_number = random.randint(1, 20)
    guesses = 0

    print(f"\nWell, {name}, I am thinking of a number between 1 and 20.")

    while True:
        guess = int(input("Take a guess.\n"))
        guesses += 1

        if guess < secret_number:
            print("\nYour guess is too low.")
        elif guess > secret_number:
            print("\nYour guess is too high.")
        else:
            print(f"\nGood job, {name}! You guessed my number in {guesses} guesses!")
            break


if __name__ == "__main__":
    print("100 grams in ounces:", grams_to_ounces(100))
    print("68°F in centigrade:", fahrenheit_to_centigrade(68))
    print("Chickens and rabbits:", solve(35, 94))
    print("Primes:", filter_prime([1, 2, 3, 4, 5, 10, 11]))
    print(reverse_sentence("We are ready"))
    print(has_33([1, 3, 3]))
    print(spy_game([1, 0, 2, 4, 0, 5, 7]))
    print("Sphere volume:", sphere_volume(3))
    print(unique_elements([1, 2, 2, 3, 1, 4]))
    print(is_palindrome("A man, a plan, a canal: Panama"))
    histogram([4, 9, 7])

    # Uncomment either line to run an interactive task:
    # print_permutations(input("Enter a string: "))
    # guess_the_number()