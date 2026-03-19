#1
class Animal:
    def speak(self):
        return "sound"

class Dog(Animal):
    def speak(self):
        return "bark"


#2
class Vehicle:
    def move(self):
        return "moving"

class Car(Vehicle):
    def move(self):
        return "driving"


#3
class Shape:
    def area(self):
        return 0

class Rectangle(Shape):
    def area(self):
        return 10 * 5


#4
class User:
    def role(self):
        return "user"

class Admin(User):
    def role(self):
        return super().role() + ":admin"


#5
from abc import ABC, abstractmethod

class Payment(ABC):
    @abstractmethod
    def pay(self):
        pass

class CreditCardPayment(Payment):
    def pay(self):
        return "paid with credit card"
