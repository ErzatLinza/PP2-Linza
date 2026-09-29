import math


# 1. Convert degrees to radians

degree = float(input("Input degree: "))
radian = degree * math.pi / 180

print("Output radian:", round(radian, 6))


# 2. Calculate the area of a trapezoid

height = float(input("\nHeight: "))
base1 = float(input("Base, first value: "))
base2 = float(input("Base, second value: "))

trapezoid_area = (base1 + base2) * height / 2

print("Area of the trapezoid:", trapezoid_area)


# 3. Calculate the area of a regular polygon

number_of_sides = int(input("\nInput number of sides: "))
side_length = float(input("Input the length of a side: "))

polygon_area = (
    number_of_sides * side_length ** 2
    / (4 * math.tan(math.pi / number_of_sides))
)

print("The area of the polygon is:", round(polygon_area))


# 4. Calculate the area of a parallelogram

base = float(input("\nLength of base: "))
parallelogram_height = float(input("Height of parallelogram: "))

parallelogram_area = base * parallelogram_height

print("Area of the parallelogram:", parallelogram_area)