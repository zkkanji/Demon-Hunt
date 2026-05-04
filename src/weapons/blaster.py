import pygame
import math
from .gun_base import GunBase
from src.entities.projectile import Projectile

class Blaster(GunBase):
    
    def __init__(self):
        super().__init__(name = "Blaster", damage = 10, weapon_type="gun", is_automatic=False, ammo_limit=15)
        self.projectile_velocity = 10
        self.projectiles = pygame.sprite.Group()  # Group to manage active projectiles

        # Blaster Sprite code
        self.original_image = pygame.image.load("assets/weapons/blaster.png") # Load the blaster sprite (original, unrotated)
        self.image = self.original_image  # Current image (will be rotated)
        self.rect = self.image.get_rect()  # Get the rect for positioning and collision
        self.projectile_image = pygame.image.load("assets/misc/blast-projectile.png")  # Load the projectile sprite
        
        # Orbiting parameters
        self.orbit_radius = 50  # Distance from player to blaster

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

    def update_position(self, player_pos, mouse_pos):
        # Call parent method to handle orbiting
        super().update_position(player_pos, mouse_pos)
        # Then rotate the blaster to point at the cursor
        self.rotate_to_angle(self.angle)

    def rotate_to_angle(self, angle):
        # Rotate blaster image to point at cursor
        rotation_degrees = -math.degrees(angle)
        self.image = pygame.transform.rotate(self.original_image, rotation_degrees)
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self):
        self.projectiles.update()  # Update all active projectiles
