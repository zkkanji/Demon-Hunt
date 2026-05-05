import pygame
from .base_weapon import BaseWeapon

class MeleeBase(BaseWeapon):
    def __init__(self, name, 
                damage,  
                is_automatic, 
                melee_range, 
                attack_cooldown, 
                orbit_radius = 40,
                weapon_type = "melee"):
        
        super().__init__(name, damage, is_automatic, weapon_type, orbit_radius)
        self.melee_range = melee_range  # Range of the melee attack
        self.attack_cooldown = attack_cooldown  # Cooldown period between attacks
        self.time_from_last_attack = 0  # Time since the last attack was made
        self.is_attacking = False  # Whether the weapon is currently in an attack animation

    def check_attack_ready(self):
        if self.is_attacking:
            return False  # Currently in an attack animation, cannot attack again
        # Check if enough time has passed since the last attack to allow a new attack
        return (pygame.time.get_ticks() - self.time_from_last_attack) >= self.attack_cooldown