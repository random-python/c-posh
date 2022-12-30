class Zoo(object):
    def __init__(self):
        self.animals = []

    def add(self, animal):
        self.animals.append(animal)

class Animal(object):
    def __init__(self):
        pass

    def meet(self, other):
        abstract

class Lion(Animal):
    def meet(self, other):
        other.meetLion(self)

    def meetLion(self, other):
        print "Lions growl at each other"
