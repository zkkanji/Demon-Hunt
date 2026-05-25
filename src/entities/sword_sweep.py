import pygame
import math
from .projectile import Projectile
from src.constants import FPS
from src.utils.sprite_utils import get_sprite_bounds

class SwordSweep(Projectile):

    def __init__(self, x, y, velocity_x, velocity_y, damage, attack_duration, attack_frames, angle=0):
        super().__init__(x, y, velocity_x, velocity_y, damage)

        self.attack_duration = attack_duration  # Total duration of the attack in milliseconds
        self.attack_frames_original = attack_frames  # List of frames for the sword sweep animation (unrotated)
        self.angle = angle  # Angle towards cursor (in radians)

        self.current_frame_index = 0
        self.frame_counter = 0
        # Calculate frames per animation frame: (duration_ms * FPS / 1000) / num_frames
        self.frame_speed = max(1, (attack_duration * FPS) // (1000 * len(attack_frames)))

        self.spawn_time = pygame.time.get_ticks()  # Record when the attack was initiated
        
        # Store actual sprite bounds (crop transparent padding) for collision
        first_frame_bounds = get_sprite_bounds(attack_frames[0])
        self.collision_width = first_frame_bounds.width
        self.collision_height = first_frame_bounds.height
        
        # Rotate frames based on angle and display first frame
        self._update_frame()

    def _update_frame(self):
        if self.current_frame_index < len(self.attack_frames_original):
            unrotated_frame = self.attack_frames_original[self.current_frame_index]
            # Rotate frame to aim towards cursor
            rotation_degrees = -math.degrees(self.angle)
            self.image = pygame.transform.rotate(unrotated_frame, rotation_degrees)
            # Display rect from rotated image (includes padding from rotation)
            self.rect = self.image.get_rect(center=(int(self.x), int(self.y)))
            # Collision rect from unrotated frame size (avoids rotation padding)
            self.collision_rect = pygame.Rect(0, 0, self.collision_width, self.collision_height)
            self.collision_rect.center = (int(self.x), int(self.y))
        
    def update(self):
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.rect.center = (int(self.x), int(self.y))
        # Keep collision rect synced with position
        self.collision_rect.center = (int(self.x), int(self.y))

        # Update animation frame
        self.frame_counter += 1
        if self.frame_counter >= self.frame_speed:
            self.frame_counter = 0
            self.current_frame_index += 1
            if self.current_frame_index < len(self.attack_frames_original):
                self._update_frame()
            else:
                self.kill()  # End the attack after the animation finishes

        # Ensure the attack ends after the specified duration
        elapsed = pygame.time.get_ticks() - self.spawn_time
        if elapsed >= self.attack_duration:
            self.kill()