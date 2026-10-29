import pygame
import math
from .gun_base import GunBase
from src.entities.projectile import Projectile
from src.utils.assets import load_image, scale_surface

class Shotgun(GunBase):

    def __init__(self):
        super().__init__(name = "shotgun", damage = 15, is_automatic = False, ammo_limit=15, reload_time=1200, attack_cooldown=800, crit_mult=1.5)
        self.projectile_velocity = 12
        projectile_scale = 1.5
        self.projectile_spread_angle = 7.5  # degrees
        self.num_projectiles_per_shot = 3
        self.projectiles = pygame.sprite.Group()  # Group to manage active projectiles
        projectile_image_raw = load_image("assets/misc/shotgun-projectile.png")
        self.projectile_image = scale_surface(projectile_image_raw, int(projectile_image_raw.get_width() * projectile_scale), int(projectile_image_raw.get_height() * projectile_scale))
    
    def attack(self, player_pos, direction):
        if self.is_reloading:
            return False
        if self.ammo < self.num_projectiles_per_shot:
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
            is_critical = self.roll_critical_hit()
            projectile_damage = round(self.damage * self.crit_multiplier) if is_critical else self.damage
            projectile = Projectile(
                px+(2*rotated_vx),
                py+(2*rotated_vy),
                rotated_vx,
                rotated_vy,
                projectile_damage,
                sprite_image=self.projectile_image,
                is_critical=is_critical,
            )
            self.projectiles.add(projectile)
        return True  # Attack succeeded

    def update(self):
        self.projectiles.update()  # Update all active projectiles

    def reload(self, player_ammo):
        if self.ammo < self.ammo_limit and player_ammo > 0:
            current_time = pygame.time.get_ticks()

            if self.time_of_last_reload == 0:
                ammo_needed = self.ammo_limit - self.ammo
                raw_transfer = min(player_ammo, ammo_needed)
                self.ammo_to_transfer = (raw_transfer // self.num_projectiles_per_shot) * self.num_projectiles_per_shot

                if self.ammo_to_transfer == 0:
                    return player_ammo  # Not enough reserve for even one shot's worth

                self.time_of_last_reload = current_time
                self.is_reloading = True
                return player_ammo - self.ammo_to_transfer

        if self.ammo >= self.ammo_limit:
            self.is_reloading = False

        return player_ammo