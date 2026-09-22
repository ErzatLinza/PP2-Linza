def changecase(func):
    def myinner(*x, **kwargs):
        return func(*x, **kwargs).upper()
    return myinner

@changecase
def myfunc(nam):
    return "Hello" + nam

print(myfunc(" John"))
