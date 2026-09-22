def my_function(name): # name is a parameter
  print("Hello", name)

my_function("Emil") # "Emil" is an argument

def my_function(country = "Norway"):
  print("I am from", country)

my_function("Sweden")
my_function()



def my_function(fruits):
  for fruit in fruits:
    print(fruit)

my_fruits = ["apple", "banana","cherry"]
my_function(my_fruits)
