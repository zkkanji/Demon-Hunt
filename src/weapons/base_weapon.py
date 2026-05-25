import pygame
import math
from abc import ABC, abstractmethod

class BaseWeapon(ABC):

    def __init__(self, name, damage, is_automatic, weapon_type):
        self.name = name
        self.damage = damage
        self.is_automatic = is_automatic
        self.weapon_type = weapon_type 
        
    @abstractmethod
    def attack(self):
        "Subclasses must implement this method to define how the weapon attacks"
        pass

