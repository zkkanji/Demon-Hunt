import pygame
from .melee_base import MeleeBase
import math

class Sword(MeleeBase):
    
    def __init__(self):
        super().__init__(name = "Sword", damage = 20, is_automatic = False, melee_range = 50, orbit_radius = 55, attack_cooldown = 400)

        # Sword Sprite code
        sword_scale_factor = 2
        self.original_image = pygame.image.load("assets/weapons/sword.png") # Load the sword sprite (original, unrotated)
        self.original_image = pygame.transform.scale(self.original_image, (int(self.original_image.get_width() * sword_scale_factor), int(self.original_image.get_height() * sword_scale_factor)))
        self.image = self.original_image.copy()  # Current image (will be rotated)
        self.rect = self.image.get_rect()  # Get the rect for positioning and collision

        #Sword Attack Animation Frames
        self.sword_attack_frames = [
            pygame.transform.scale(pygame.image.load(f"assets/weapons/sword_attack/sword-attack{i}.png"), (int(pygame.image.load(f"assets/weapons/sword_attack/sword-attack{i}.png").get_width() * sword_scale_factor), int(pygame.image.load(f"assets/weapons/sword_attack/sword-attack{i}.png").get_height() * sword_scale_factor))) 
            for i in range(1, 7)]
        self.attack_frame_index = 0

    def attack(self, player_pos, direction):
        if not self.check_attack_ready():
            return
        self.is_attacking = True  # Start the attack animation
        self.attack_frame_index = 0  # Reset animation frame index
        self.enemies_hit_this_swing = []
        self.time_from_last_attack = pygame.time.get_ticks()  # Reset the attack cooldown timer

    def update(self):
        if self.is_attacking:
            current_frame = self.sword_attack_frames[self.attack_frame_index]
            
            # Rotate the animation frame to point at cursor
            rotation_degrees = -math.degrees(self.angle)
            self.image = pygame.transform.rotate(current_frame, rotation_degrees)
            self.rect = self.image.get_rect(center=self.rect.center)
            
            self.attack_frame_index += 1
            if self.attack_frame_index >= len(self.sword_attack_frames):
                self.is_attacking = False  # End the attack animation
                self.attack_frame_index = 0

    def get_sweep_triangle(self):
        weapon_pos = self.rect.center
        attack_angle = self.angle

        sweep_distance = self.melee_range
        tip = weapon_pos

        left_angle = attack_angle + math.radians(30)
        right_angle = attack_angle - math.radians(30)

        left_point = (
            weapon_pos[0] + sweep_distance * math.cos(left_angle),
            weapon_pos[1] + sweep_distance * math.sin(left_angle)
        )
        right_point = (
            weapon_pos[0] + sweep_distance * math.cos(right_angle),
            weapon_pos[1] + sweep_distance * math.sin(right_angle)
        )
        return (tip, left_point, right_point)