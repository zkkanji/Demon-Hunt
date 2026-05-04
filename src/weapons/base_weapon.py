import pygame
from abc import ABC, abstractmethod

class BaseWeapon(ABC):

    def __init__(self, name, damage, weapon_type, is_automatic):
        self.name = name
        self.damage = damage
        self.weapon_type = weapon_type
        self.is_automatic = is_automatic

    @abstractmethod
    def attack(self):
        "Subclasses must implement this method to define how the weapon attacks"
        pass