class Student:
    def __init__(self, university):
        self.university = university

    def study(self):
        print(f"I study at {self.university}")

class Athlete:
    def __init__(self, sport):
        self.sport = sport

    def exercise(self):
        print(f"I train in {self.sport}.")

class Person(Student, Athlete):
    def __init__(self, name, age, university, sport):
        Student.__init__(self,university)
        Athlete.__init__(self, sport)

        self.name = name
        self._age = age

        @property
        def age(self):
            return self.age
        
        @age.setter
        def age(self, new_age):
            if new_age >= 0:
                self._age = new_age
            else:
                print("Age cannot be negative.")

    def introduce(self):
            print(f"My name is {self.name}, and I am {self._age} years old")

person1 = Person("Linza", 19, "KBTU", "Football")

person1.introduce()
person1.study()
person1.exercise()

print(person1._age)

person1.age = 20
print(person1.age)

