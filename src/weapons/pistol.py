import pygame
from .base_weapon import BaseWeapon
from src.entities.projectile import Projectile

class Pistol(BaseWeapon):
    
    def __init__(self):
        super().__init__(name = "Pistol", damage = 5, ammunition = 15, weapon_type="gun")
        self.projectile_velocity = 8
        self.projectiles = pygame.sprite.Group()  # Group to manage active projectiles

    def attack(self, player_pos, direction):
        self.ammunition -= 1  # Decrease ammunition by 1 each time the gun is fired

        #Unpacking position and direction tuples
        px, py = player_pos
        dx, dy = direction

        vx = dx * self.projectile_velocity
        vy = dy * self.projectile_velocity

        projectile = Projectile(px, py, vx, vy, self.damage)
        self.projectiles.add(projectile)

    def update(self):
        self.projectiles.update()  # Update all active projectiles