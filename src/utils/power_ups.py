import pygame
from pygame.sprite import Sprite
from src.utils.sprite_utils import make_shadow
from abc import ABC, abstractmethod

#Stores all power up classes in file
class PowerUp(ABC):
    def __init__(self, player, duration, name):
        self.player = player
        self.duration = duration  # milliseconds
        self.text = None
        self.name = name
        self.is_active = False
        self.start_time = 0
        self.has_time_limit = None
        self.UI_logo = None

    @abstractmethod
    def use_powerup(self):
        """Activate the power-up's effect on the player."""
        pass

    @abstractmethod
    def end_powerup(self):
        """Revert the power-up's effect once its duration has elapsed."""
        pass

    def is_expired(self):
        return pygame.time.get_ticks() - self.start_time >= self.duration

    def update(self):
        if self.is_active and self.is_expired():
            self.end_powerup()

class Bomb_PowerUp(PowerUp):

    class Bomb(Sprite):
        def __init__(self, pos, damage, radius):
            super().__init__()
            self.x, self.y = pos
            self.damage = damage
            self.radius = radius

            bomb_frames_raw = [
                pygame.image.load(f"assets/misc/bomb-frames/f{i}.png")
                for i in range(1, 14)
            ]
            explosion_frames_raw = [
                pygame.image.load(f"assets/misc/explosion/f{i}.png")
                for i in range(1, 8)
            ]
            blast_radius_raw = pygame.image.load("assets/misc/blast-radius.png").convert_alpha()

            image_scale = 2
            self.bomb_frames = [
                pygame.transform.scale(frame, (int(frame.get_width() * image_scale), int(frame.get_height() * image_scale)))
                for frame in bomb_frames_raw
            ]

            # Explosion frames and the blast radius decal are scaled together off
            # the actual damage radius, so they stay visually in sync if radius changes.
            blast_diameter = int(self.radius * 2)
            self.explosion_frames = [
                pygame.transform.scale(frame, (blast_diameter, blast_diameter))
                for frame in explosion_frames_raw
            ]
            self.blast_radius_image = pygame.transform.scale(blast_radius_raw, (blast_diameter, blast_diameter))
            self.blast_radius_image.set_alpha(60)  # Make the blast radius semi-transparent
            shadow_image_raw = pygame.image.load("assets/misc/entity-shadow.png").convert_alpha()
            self.shadow = make_shadow(shadow_image_raw, self.bomb_frames[0].get_width())

            self.image = self.bomb_frames[0]
            self.rect = self.image.get_rect(center=(self.x, self.y))

            self.state = "ticking"  # "ticking" -> "exploding" -> killed
            self.fuse_time = 1500  # ms before detonation
            self.spawn_time = pygame.time.get_ticks()
            self.damaged_entities = set()  # entities already hit by this explosion

            self.frame_index = 0
            self.frame_counter = 0
            self.frame_speed = 5
            self.explosion_frame_speed = 2

        def update(self):
            self.frame_counter += 1
            if self.state == "ticking":
                if self.frame_counter >= self.frame_speed:
                    self.frame_counter = 0
                    self.frame_index = (self.frame_index + 1) % len(self.bomb_frames)
                    self.image = self.bomb_frames[self.frame_index]
                if pygame.time.get_ticks() - self.spawn_time >= self.fuse_time:
                    self.state = "exploding"
                    self.frame_index = 0
                    self.frame_counter = 0
                    self.image = self.explosion_frames[0]
                    self.rect = self.image.get_rect(center=(self.x, self.y))
            elif self.state == "exploding":
                if self.frame_counter >= self.explosion_frame_speed:
                    self.frame_counter = 0
                    if self.frame_index < len(self.explosion_frames):
                        self.image = self.explosion_frames[self.frame_index]
                        self.rect = self.image.get_rect(center=(self.x, self.y))
                        self.frame_index += 1
                    else:
                        self.kill()

        def draw(self, screen):
            blast_rect = self.blast_radius_image.get_rect(center=(self.x, self.y))
            screen.blit(self.blast_radius_image, blast_rect)
            if self.state == "ticking":
                shadow_rect = self.shadow.get_rect(midbottom=(self.rect.centerx, self.rect.bottom))
                screen.blit(self.shadow, shadow_rect)
            screen.blit(self.image, self.rect)


    def __init__(self, player, duration):
        super().__init__(player, duration, "Bomb")
        self.text = "Power Up: A bomb that can be dropped and explodes after a short delay"
        self.damage = 120
        self.radius = 200
        self.pending_bombs = []  # newly-dropped bombs, harvested into a sprite group by main.py
        self.UI_logo = pygame.image.load("assets/upgrade-cards/powerup-cards/bomb/card.png").convert_alpha()

    def use_powerup(self):
        bomb = self.Bomb((self.player.x, self.player.y), self.damage, self.radius)
        self.pending_bombs.append(bomb)

    def end_powerup(self):
        pass  # one-shot effect; nothing to revert

class Invincibility(PowerUp):
    def __init__(self, player, duration):
        super().__init__(player, duration, "Invincibility")
        self.text = "Power Up: Gain invincibility for 10 seconds"
        self.has_time_limit = True
        self.UI_logo = pygame.image.load("assets/upgrade-cards/powerup-cards/invincibility/card.png").convert_alpha()

    def use_powerup(self):
        self.player.is_invincible = True
        self.is_active = True
        self.start_time = pygame.time.get_ticks()

    def end_powerup(self):
        self.player.is_invincible = False
        self.is_active = False

class SpeedBoost(PowerUp):
    def __init__(self, player, duration):
        super().__init__(player, duration, "Speed Boost")
        self.text = "Power Up: Increase movement speed for 10 seconds"
        self.speed_multiplier = 2
        self.has_time_limit = True
        self.original_speed = None
        self.UI_logo = pygame.image.load("assets/upgrade-cards/powerup-cards/speed-boost/card.png").convert_alpha()
        
    def use_powerup(self):
        if not self.is_active:
            self.original_speed = self.player.movement_speed
            self.player.movement_speed *= self.speed_multiplier
            self.is_active = True
        self.start_time = pygame.time.get_ticks()  # (re)start the duration timer

    def end_powerup(self):
        self.player.movement_speed = self.original_speed
        self.is_active = False
