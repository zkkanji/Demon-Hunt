import pygame
from .gun_base import GunBase
from src.entities.projectile import Projectile

class Pistol(GunBase):
    
    def __init__(self):
        super().__init__(name = "Pistol", damage = 5, weapon_type="gun", is_automatic=False, ammo_limit=15)
        self.projectile_velocity = 8
        self.projectiles = pygame.sprite.Group()  # Group to manage active projectiles

    def attack(self, player_pos, direction):

        if self.ammo <= 0:
            return  # No ammo left, cannot fire
        self.ammo -= 1  # Decrease ammunition by 1 each time the gun is fired

        #Unpacking position and direction tuples
        px, py = player_pos
        dx, dy = direction

        vx = dx * self.projectile_velocity
        vy = dy * self.projectile_velocity

        projectile = Projectile(px, py, vx, vy, self.damage)
        self.projectiles.add(projectile)

    def update(self):
        self.projectiles.update()  # Update all active projectiles