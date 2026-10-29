import pygame
from .gun_base import GunBase
from src.entities.projectile import Projectile
from src.utils.assets import load_image, scale_surface

class Blaster(GunBase):
    
    def __init__(self):
        super().__init__(name = "blaster", damage = 10, is_automatic = False, ammo_limit=15, reload_time=800, attack_cooldown=225, crit_mult=1.5)
        self.projectile_velocity = 10
        projectile_scale = 1.5
        self.projectiles = pygame.sprite.Group()  # Group to manage active projectiles
        projectile_image_raw = load_image("assets/misc/blast-projectile.png")
        self.projectile_image = scale_surface(projectile_image_raw, int(projectile_image_raw.get_width() * projectile_scale), int(projectile_image_raw.get_height() * projectile_scale))
    

    def attack(self, player_pos, direction):
        if self.is_reloading:
            return False
        if self.ammo <= 0:
            return False
        if not self.check_shot_ready():
            return False
        self.ammo -= 1

        #Unpacking position and direction tuples
        px, py = player_pos
        dx, dy = direction

        vx = dx * self.projectile_velocity
        vy = dy * self.projectile_velocity

        self.is_shooting = True
        self.time_since_last_shot = pygame.time.get_ticks()
        is_critical = self.roll_critical_hit()
        projectile_damage = round(self.damage * self.crit_multiplier) if is_critical else self.damage
        projectile = Projectile(
            px+(2*vx), 
            py+(2*vy), 
            vx, 
            vy, 
            projectile_damage, 
            sprite_image = self.projectile_image, 
            is_critical=is_critical)
        self.projectiles.add(projectile)
        return True  # Attack succeeded

    def update(self):
        self.projectiles.update()  # Update all active projectiles
