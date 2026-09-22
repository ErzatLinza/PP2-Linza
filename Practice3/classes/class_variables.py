class Student:
    school = "Central School"  # Class variable

    def __init__(self, name, age):
        self.name = name       # Instance variable
        self.age = age         # Instance variable


student1 = Student("Linza", 19)
student2 = Student("Emil", 21)

print(student1.name)    # Linza
print(student2.age)     # 21
print(Student.school)   # Central School