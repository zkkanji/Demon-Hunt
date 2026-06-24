import pygame
import math
from .gun_base import GunBase
from src.entities.projectile import Projectile

class Shotgun(GunBase):

    def __init__(self):
        super().__init__(name = "Shotgun", damage = 15, is_automatic = False, ammo_limit=15, reload_time=1200, attack_cooldown=800)
        self.projectile_velocity = 12
        projectile_scale = 1.5
        self.projectile_spread_angle = 7.5  # degrees
        self.num_projectiles_per_shot = 3
        self.projectiles = pygame.sprite.Group()  # Group to manage active projectiles
        projectile_image_raw = pygame.image.load("assets/misc/shotgun-projectile.png")  
        self.projectile_image = pygame.transform.scale(projectile_image_raw, (projectile_image_raw.get_width() * projectile_scale, projectile_image_raw.get_height() * projectile_scale))
    
    def attack(self, player_pos, direction):
        if self.is_reloading:
            return False
        if self.ammo <= 0:
            return False
        if not self.check_shot_ready():
            return False
        self.ammo -= self.num_projectiles_per_shot 

        #Unpacking position and direction tuples
        px, py = player_pos
        dx, dy = direction

        vx = dx * self.projectile_velocity
        vy = dy * self.projectile_velocity

        self.is_shooting = True
        self.time_since_last_shot = pygame.time.get_ticks()
        for i in range(self.num_projectiles_per_shot):
            angle_offset = (i - self.num_projectiles_per_shot // 2) * self.projectile_spread_angle
            rad_angle = math.radians(angle_offset)
            rotated_vx = vx * math.cos(rad_angle) - vy * math.sin(rad_angle)
            rotated_vy = vx * math.sin(rad_angle) + vy * math.cos(rad_angle)
            projectile = Projectile(px+(2*rotated_vx), py+(2*rotated_vy), rotated_vx, rotated_vy, self.damage, sprite_image = self.projectile_image)
            self.projectiles.add(projectile)
        return True  # Attack succeeded

    def update(self):
        self.projectiles.update()  # Update all active projectiles