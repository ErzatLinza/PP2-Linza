def myfunc():
    global x
    x = 200
    def myinnerfunc():
        print(x)
    myinnerfunc()

myfunc()
print(x)

#LEGB rule
x = "global"
def outer():
    x = "enclosing"
    def inner():
        x = "local"
        print("Inner:" , x)
    inner()
    print("Outer:", x)

outer()
print("Global", x)