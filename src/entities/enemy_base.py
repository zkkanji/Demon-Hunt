import pygame
from .base_entity import BaseEntity
from abc import ABC, abstractmethod

class Enemy(BaseEntity, ABC):

    def __init__(self, x, y, width=50, height=50, color=(255, 0, 0), health=20, movement_speed=2):
        super().__init__(x, y, width, height, color, health)
        self.movement_speed = movement_speed
        self.direction = (0, 0)  # Default direction (not moving)
    
    @abstractmethod
    def primary_attack(self, player):
        pass

    @abstractmethod
    def secondary_attack(self, player):
        pass