import pygame
import math
from .gun_base import GunBase
from src.entities.projectile import Projectile

class Blaster(GunBase):
    
    def __init__(self):
        super().__init__(name = "Blaster", damage = 10, is_automatic = False, ammo_limit=15, orbit_radius = 65)
        self.projectile_velocity = 10
        self.projectiles = pygame.sprite.Group()  # Group to manage active projectiles

        # Blaster Sprite code
        blaster_scale_factor = 1.7
        self.original_image = pygame.image.load("assets/weapons/blaster.png") # Load the blaster sprite (original, unrotated)
        self.original_image = pygame.transform.scale(self.original_image, (int(self.original_image.get_width() * blaster_scale_factor), int(self.original_image.get_height() * blaster_scale_factor)))
        self.image = self.original_image.copy()  # Current image (will be rotated)
        self.rect = self.image.get_rect()  # Get the rect for positioning and collision
        self.projectile_image = pygame.image.load("assets/misc/blast-projectile.png")  # Load the projectile sprite
    

    def attack(self, player_pos, direction):

        if self.ammo <= 0:
            return  # No ammo left, cannot fire
        self.ammo -= 1  # Decrease ammunition by 1 each time the gun is fired

        #Unpacking position and direction tuples
        px, py = player_pos
        dx, dy = direction

        vx = dx * self.projectile_velocity
        vy = dy * self.projectile_velocity

        projectile = Projectile(px, py, vx, vy, self.damage, sprite_image = self.projectile_image)
        self.projectiles.add(projectile)

    def update(self):
        self.projectiles.update()  # Update all active projectiles
