import pygame
from .base_weapon import BaseWeapon

class GunBase(BaseWeapon):

    def __init__(self, name, damage, weapon_type, is_automatic, ammo_limit):
        super().__init__(name, damage, weapon_type, is_automatic)

        self.ammo_limit = ammo_limit
        self.ammo = ammo_limit  # Start with a full magazine

    def reload(self, player_ammo):
        if self.ammo < self.ammo_limit and player_ammo > 0:
            ammo_needed = self.ammo_limit - self.ammo
            if player_ammo <= ammo_needed:
                self.ammo += player_ammo
                return 0
            else:
                self.ammo += ammo_needed
                return player_ammo - ammo_needed
        return player_ammo