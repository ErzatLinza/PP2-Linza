class person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __lt__(self, other):
        return self.age < other.age
    
p1= person("Emil", 22)
p2 = person("Tobias", 19)
p3 = person("Linus", 25)

x = sorted([p1, p2, p3])

print(x[1].age)