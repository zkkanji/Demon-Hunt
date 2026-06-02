import pygame
from .base_entity import BaseEntity
from abc import ABC, abstractmethod
import src.game as game
from src.game import decrement_wave_enemies
from src.utils.enemy_utils import DamageNumber, EnemyDrops
import random

class Enemy(BaseEntity, ABC):

    def __init__(self, x, y, attack_duration, max_health, attack_damage, knockback_damage, movement_speed, scale_factor=2.5, attack_cooldown=400, enemy_type=None):
        super().__init__(x, y, max_health)
        self.movement_speed = movement_speed
        self.direction = (0, 0)  # Default direction (not moving)
        self.is_moving = False
        self.scale_factor = scale_factor
        self.is_hit = False
        self.hit_timer = 0
        self.is_dying = False
        self.direction_facing = "right"  # Default facing direction
        self.is_attacking = False
        self.attack_timer = 0
        self.attack_duration = attack_duration  # milliseconds
        self.attack_damage = attack_damage
        self.knockback_damage = knockback_damage
        self.knockback_velocity = 3
        self.knockback_duration = 300  # milliseconds
        self.is_knockback = False
        self.knockback_timer = 0
        self.time_from_last_attack = 0
        self.attack_cooldown = attack_cooldown  # milliseconds
        self.last_wave_processed = 0
        self.enemy_type = enemy_type
        self.shadow = None  # set by subclass after frames are loaded
        self.damage_numbers = []
        self.pending_drops = []  

    @abstractmethod
    def primary_attack(self, player):
        pass

    def take_damage(self, damage_amount):
        self.current_health -= damage_amount
        dnx, dny = self.rect.topright
        dnx += 10
        dny += 10
        self.damage_numbers.append(DamageNumber((dnx, dny), damage_amount))
        if self.current_health <= 0:
            self.is_dying = True
        else:
            self.is_hit = True  # Set hit state to trigger hit animation
            self.hit_timer = pygame.time.get_ticks()  # Record when hit occurred

    def calculate_direction(self, player):
        dx = player.x - self.x
        dy = player.y - self.y
        distance = (dx ** 2 + dy ** 2) ** 0.5
        if distance != 0:
            self.direction = (dx / distance, dy / distance)
            # Update facing direction based on horizontal movement
            if dx < 0:
                self.direction_facing = "left"
            else:
                self.direction_facing = "right"

    def movement(self, player):
        self.calculate_direction(player)
        self.velocity_x = self.direction[0] * self.movement_speed
        self.velocity_y = self.direction[1] * self.movement_speed
        self.is_moving = True if (self.velocity_x != 0 or self.velocity_y != 0) else False

    def wave_update(self):
        if game.wave_number > self.last_wave_processed and game.wave_number > 1:
            self.last_wave_processed = game.wave_number
            health_increment = (game.wave_number-1) * 17
            attack_increment = (game.wave_number-1) * 5
            knockback_increment = (game.wave_number-1) * 5 
            self.max_health += health_increment
            self.current_health = self.max_health       
            self.attack_damage += attack_increment
            self.knockback_damage += knockback_increment

    def die(self):
        decrement_wave_enemies()  # Decrement the count of enemies left in the wave when this enemy dies
    
    def death_drops_generation(self, player):
        random_index = random.randint(0, 4)
        if random_index == 0:
            drop = EnemyDrops((self.x, self.y), 15, player, "current_health")
            self.pending_drops.append(drop)
        elif random_index == 1 or random_index == 2:  # Increase chance for ammo drops
            drop = EnemyDrops((self.x, self.y), 15, player, "ammo")
            self.pending_drops.append(drop)

    def update(self):
        super().update()  # Update position based on velocity and handle border control
        self.wave_update()  # Check for wave events and update stats if needed
        for dn in self.damage_numbers:
            dn.update()
        self.damage_numbers = [dn for dn in self.damage_numbers if not dn.is_expired()]