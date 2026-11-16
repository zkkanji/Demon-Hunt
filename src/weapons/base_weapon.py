import random
from abc import ABC, abstractmethod
from src.utils.assets import load_image, scale_surface

class BaseWeapon(ABC):

    def __init__(self, name, damage, is_automatic, crit_mult=1.0, weapon_type=None):
        self.name = name
        self.damage = damage
        self.is_automatic = is_automatic
        self.weapon_type = weapon_type 
        self.crit_chance = 10 #supposed to be 10
        self.crit_multiplier = crit_mult
        idle_weapon_card = load_image(f"assets/weapons/{self.name}/{self.name}1.png")
        hover_weapon_card = load_image(f"assets/weapons/{self.name}/{self.name}2.png")
        card_scale = 170
        self.weapon_cards = (scale_surface(idle_weapon_card, card_scale, card_scale), 
                            scale_surface(hover_weapon_card, card_scale, card_scale)
                            )

    def roll_critical_hit(self):
        return random.random() < self.crit_chance / 100
        
    @abstractmethod
    def attack(self):
        "Subclasses must implement this method to define how the weapon attacks"
        pass

