import pygame
from .melee_base import MeleeBase
from src.entities.projectile import BoomerangProjectile
from src.constants import FPS
from src.utils.assets import load_image, scale_surface

class Boomerang(MeleeBase):
    def __init__(self, player=None):
        super().__init__(name = "boomerang", damage = 30, is_automatic = False, melee_range = 310, attack_cooldown = 500, crit_mult = 1.7)
        self.boomerang_scale = 2
        projectile_image = load_image("assets/misc/boomerang-projectile.png")
        self.boomerang_image = scale_surface(projectile_image, int(projectile_image.get_width() * self.boomerang_scale), int(projectile_image.get_height() * self.boomerang_scale))
        self.player = player
        self.projectiles = pygame.sprite.Group()

    def attack(self, player_pos, direction):
        if self.player is None or not self.check_attack_ready() or self.projectiles:
            return False

        direction_vector = pygame.Vector2(direction)
        if direction_vector.length_squared() == 0:
            return False
        direction_vector = direction_vector.normalize()
        speed = (self.melee_range * 2) / (self.attack_cooldown * FPS / 1000)
        is_critical = self.roll_critical_hit()
        damage = round(self.damage * self.crit_multiplier) if is_critical else self.damage
        projectile = BoomerangProjectile(
            player_pos[0],
            player_pos[1],
            direction_vector.x * speed,
            direction_vector.y * speed,
            damage,
            self.player,
            self.melee_range,
            sprite_image=self.boomerang_image,
            is_critical=is_critical,
        )
        self.projectiles.add(projectile)
        self.time_from_last_attack = pygame.time.get_ticks()
        self.is_attacking = True
        if self.player is not None:
            self.player.weapon_in_hand = False
        return True

    def update(self):
        self.projectiles.update()
        if not self.projectiles:
            self.is_attacking = False
            if self.player is not None:
                self.player.weapon_in_hand = True