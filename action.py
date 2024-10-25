# Machines will have a list of state:action pairs.
class Action:
  def __init__(self, colour, animal, tree):
    self.next_colour = colour
    self.next_animal = animal
    self.tree = tree

  def __str__(self):
    return f"{self.next_colour},{self.next_animal},{self.tree}"