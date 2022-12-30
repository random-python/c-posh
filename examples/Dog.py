import posh

class Dog(object):
  def __init__(self, owner=None, race=None, weight=None):
    self.owner = owner or "Unknown"
    self.race = race or "Unknown"
    self.weight = weight or 50

  def bark(self):
    if self.weight > 100:
      print "BARK"
    else:
      print "bark"

posh.allow_sharing(Dog, posh.generic_init)

d = Dog("Steffen", "Golden Retriever", 120)
d.bark()
e = posh.share(d)
e.bark()
e.weight /= 3
e.bark()

