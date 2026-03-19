#1
class Flyer:
    def move(self):
        return "flying"

class Walker:
    def move(self):
        return "walking"

class Bird(Flyer, Walker):
    pass


#2
class Engine:
    def start(self):
        return "engine started"

class Wheels:
    def roll(self):
        return "wheels rolling"

class Car(Engine, Wheels):
    pass


#3
class A:
    def who(self):
        return "A"

class B:
    def who(self):
        return "B"

class C(A, B):
    pass


#4
class Reader:
    def read(self):
        return "reading"

class Writer:
    def write(self):
        return "writing"

class Author(Reader, Writer):
    pass


#5
class Logger:
    def log(self):
        return "logging"

class Saver:
    def save(self):
        return "saving"

class Service(Logger, Saver):
    pass
