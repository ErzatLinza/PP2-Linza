
class person:
    def __init__(self,name, age):
        self.name = name
        self.age = age

    def greet(self):
        print("Hello my name is " + self.name)

p1 = person("John", 24)
p1.greet()