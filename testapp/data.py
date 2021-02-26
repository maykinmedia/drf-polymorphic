from dataclasses import dataclass


@dataclass
class Pet:
    name: str


@dataclass
class Cat(Pet):
    hunting_skill: str
    pet_type: str = "cat"


@dataclass
class Dog(Pet):
    bark: str
    pet_type: str = "dog"


@dataclass
class Lizard(Pet):
    loves_rocks: bool
    pet_type: str = "lizard"


cat = Cat(name="Snowball", hunting_skill="lazy")
dog = Dog(name="Lady", bark="soft")
lizard = Lizard(name="John", loves_rocks=True)

pets = [cat, dog, lizard]
