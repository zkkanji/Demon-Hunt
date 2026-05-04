import pygame
import math
from abc import ABC, abstractmethod

class BaseWeapon(ABC):

    def __init__(self, name, damage, weapon_type, is_automatic):
        self.name = name
        self.damage = damage
        self.weapon_type = weapon_type
        self.is_automatic = is_automatic
        self.image = pygame.Surface((25, 25))
        self.rect = self.image.get_rect()
        
        # Orbiting parameters
        self.orbit_radius = 80
        self.angle = 0

    @abstractmethod
    def attack(self):
        "Subclasses must implement this method to define how the weapon attacks"
        pass

    def update_position(self, player_pos, mouse_pos):
        # Calculate angle from player to mouse and position weapon in orbit
        player_x, player_y = player_pos
        mouse_x, mouse_y = mouse_pos
        
        # Calculate angle to cursor
        self.angle = math.atan2(mouse_y - player_y, mouse_x - player_x)
        
        # Calculate orbital position around player
        weapon_x = player_x + self.orbit_radius * math.cos(self.angle)
        weapon_y = player_y + self.orbit_radius * math.sin(self.angle)
        
        # Update weapon position
        self.rect.center = (int(weapon_x), int(weapon_y))
