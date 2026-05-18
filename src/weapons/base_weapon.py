import pygame
import math
from abc import ABC, abstractmethod

class BaseWeapon(ABC):

    def __init__(self, name, damage, is_automatic, weapon_type, orbital_radius):
        self.name = name
        self.damage = damage
        self.is_automatic = is_automatic
        self.weapon_type = weapon_type 
        self.image = pygame.Surface((25, 25))
        self.rect = self.image.get_rect()
        
        # Original unrotated image (subclasses should set this)
        self.original_image = None
        
        # Orbiting parameters
        self.orbit_radius = orbital_radius  # Distance from player to weapon
        self.angle = 0

    @abstractmethod
    def attack(self):
        "Subclasses must implement this method to define how the weapon attacks"
        pass

    def update_position(self, player_pos, mouse_pos):
        # Calculate angle from player to mouse and position weapon in orbit
        player_x, player_y = player_pos
        mouse_x, mouse_y = mouse_pos
        
        # Fallback: if mouse hasn't moved yet (at 0,0), position weapon to the right
        if mouse_x == 0 and mouse_y == 0:
            mouse_x = player_x + 100  # Default to right of player
            mouse_y = player_y
        
        # Calculate angle to cursor
        self.angle = math.atan2(mouse_y - player_y, mouse_x - player_x)
        
        # Calculate orbital position around player
        weapon_x = player_x + self.orbit_radius * math.cos(self.angle)
        weapon_y = player_y + self.orbit_radius * math.sin(self.angle)
        
        # Update weapon position - centered at the calculated orbit position
        self.rect.center = (int(weapon_x), int(weapon_y))
        
        # Rotate weapon to point at cursor
        self.rotate_to_angle()

    def rotate_to_angle(self):
        # Rotate weapon image to point at cursor angle
        if self.original_image is None:
            return  # Skip if weapon doesn't have original_image set
        
        rotation_degrees = -math.degrees(self.angle)
        self.image = pygame.transform.rotate(self.original_image, rotation_degrees)
        self.rect = self.image.get_rect(center=self.rect.center)
