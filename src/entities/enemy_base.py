import pygame
from .base_entity import BaseEntity
from abc import ABC, abstractmethod

class Enemy(BaseEntity, ABC):

    def __init__(self, x, y, color=(255, 0, 0), health=20, movement_speed=6, scale_factor=3):
        super().__init__(x, y, color, health)
        self.movement_speed = movement_speed
        self.direction = (0, 0)  # Default direction (not moving)
        self.scale_factor = scale_factor
        self.is_hit = False
        self.hit_timer = 0
        
    @abstractmethod
    def primary_attack(self, player):
        pass

    def take_damage(self, damage_amount):
        self.health -= damage_amount
        if self.health <= 0:
            self.kill()  
        else:
            self.is_hit = True  # Set hit state to trigger hit animation
            self.hit_timer = pygame.time.get_ticks()  # Record when hit occurred