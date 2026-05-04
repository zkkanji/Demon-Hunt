import pygame
from .base_weapon import BaseWeapon
from src.entities.projectile import Projectile

class Pistol(BaseWeapon):
    
    def __init__(self):
        super().__init__(name = "Pistol", damage = 5, ammunition = 15, weapon_type="gun", is_automatic=False)
        self.projectile_velocity = 8
        self.projectiles = pygame.sprite.Group()  # Group to manage active projectiles

    def attack(self, player_pos, direction):

        if self.ammunition <= 0:
            return  # No ammo left, cannot fire
        self.ammunition -= 1  # Decrease ammunition by 1 each time the gun is fired

        #Unpacking position and direction tuples
        px, py = player_pos
        dx, dy = direction

        vx = dx * self.projectile_velocity
        vy = dy * self.projectile_velocity

        projectile = Projectile(px, py, vx, vy, self.damage)
        self.projectiles.add(projectile)

    def reload(self, player_ammo):
        if self.ammunition < 15 and player_ammo > 0:
            if player_ammo <= 15:
                self.ammunition = player_ammo
                return 0
            else:
                self.ammunition = 15
                return player_ammo - 15
        return player_ammo

    def update(self):
        self.projectiles.update()  # Update all active projectiles