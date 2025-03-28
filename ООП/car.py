import datetime

class Car:
    def __init__(self,mark,model,year):
        self.mark = mark
        self.model = model
        self.year = year

    def display_info(self):
        print(f"Car: {self.year}, {self.mark}, {self.model}")


#my_car = Car("Toyota", "Corola", 2020)

#my_car.display_info()

class Employee:
    def __init__(self, name):
        self.name = name

    def work(self):
        raise NotImplementedError("Subclass must implement abstract method")

class Developer(Employee):
    def work(self):
        print(f"{self.name} codes")

class Tech_sup(Employee):
    def work(self):
        print(f"{self.name} provides technical support")

Bob = Tech_sup("Bob")
Candy = Developer("Candy")
Bob.work()
Candy.work()
