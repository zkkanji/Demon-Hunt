import pygame

from .gun_base import GunBase
from src.entities.projectile import Projectile

class Blaster(GunBase):
    
    def __init__(self):
        super().__init__(name = "Blaster", damage = 10, is_automatic = False, ammo_limit=15, reload_time=800)
        self.projectile_velocity = 10
        projectile_scale = 1.5
        self.projectiles = pygame.sprite.Group()  # Group to manage active projectiles
        projectile_image_raw = pygame.image.load("assets/misc/blast-projectile.png")  # Load the projectile sprite
        self.projectile_image = pygame.transform.scale(projectile_image_raw, (projectile_image_raw.get_width() * projectile_scale, projectile_image_raw.get_height() * projectile_scale))
    

    def attack(self, player_pos, direction):
        if self.is_reloading:
            return False  # Cannot attack while reloading
        if self.ammo <= 0:
            return False  # No ammo left, cannot fire
        self.ammo -= 1  # Decrease ammunition by 1 each time the gun is fired

        #Unpacking position and direction tuples
        px, py = player_pos
        dx, dy = direction

        vx = dx * self.projectile_velocity
        vy = dy * self.projectile_velocity

        projectile = Projectile(px+(2*vx), py+(2*vy), vx, vy, self.damage, sprite_image = self.projectile_image)
        self.projectiles.add(projectile)
        return True  # Attack succeeded

    def update(self):
        self.projectiles.update()  # Update all active projectiles
