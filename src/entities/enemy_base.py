import pygame
from .base_entity import BaseEntity
from abc import ABC, abstractmethod

class Enemy(BaseEntity, ABC):

    def __init__(self, x, y, attack_duration, max_health, attack_damage, knockback_damage, movement_speed, scale_factor=2.5, attack_cooldown=400):
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
        
    @abstractmethod
    def primary_attack(self, player):
        pass

    def take_damage(self, damage_amount):
        self.current_health -= damage_amount
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
        