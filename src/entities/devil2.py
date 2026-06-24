import pygame
import math
import src.game as game
from .enemy_base import Enemy
from src.utils.progressbar import ProgressBar
from src.entities.projectile import AnimatedProjectile
from src.utils.sprite_utils import get_sprite_bounds, make_shadow
from src.constants import FPS

class Devil2(Enemy):

    def __init__(self, x, y):
        super().__init__(x,
                        y,
                        attack_duration=100,
                        max_health=40,
                        attack_damage=8,
                        knockback_damage=5,
                        movement_speed=1.5,
                        scale_factor=2.5,
                        attack_cooldown=700,
                        enemy_type="ranged devil")

        self.shoot_radius = 250
        self.projectile_speed = 4
        self.projectiles = pygame.sprite.Group()

        #Idle Frames (Right)
        idle_frames_right_raw = [
            pygame.image.load(f"assets/enemies/enemy2/right/idle/f{i}.png")
            for i in range(1, 6)
        ]
        self.right_idle_frames = [
            pygame.transform.scale(frame, (int(frame.get_width() * self.scale_factor), int(frame.get_height() * self.scale_factor)))
            for frame in idle_frames_right_raw
        ]
        #Idle Frames (Left)
        idle_frames_left_raw = [
            pygame.image.load(f"assets/enemies/enemy2/left/idle/f{i}.png")
            for i in range(1, 6)
        ]
        self.left_idle_frames = [
            pygame.transform.scale(frame, (int(frame.get_width() * self.scale_factor), int(frame.get_height() * self.scale_factor)))
            for frame in idle_frames_left_raw
        ]

        #Right Movement Frames
        right_movement_frames_raw = [
            pygame.image.load(f"assets/enemies/enemy2/right/movement/f{i}.png")
            for i in range(1, 6)
        ]
        self.right_movement_frames = [
            pygame.transform.scale(frame, (int(frame.get_width() * self.scale_factor), int(frame.get_height() * self.scale_factor)))
            for frame in right_movement_frames_raw
        ]
        #Left Movement Frames
        left_movement_frames_raw = [
            pygame.image.load(f"assets/enemies/enemy2/left/movement/f{i}.png")
            for i in range(1, 6)
        ]
        self.left_movement_frames = [
            pygame.transform.scale(frame, (int(frame.get_width() * self.scale_factor), int(frame.get_height() * self.scale_factor)))
            for frame in left_movement_frames_raw
        ]

        #Right Hit Frames
        right_hit_frames_raw = [
            pygame.image.load(f"assets/enemies/enemy2/right/hit/f{i}.png")
            for i in range(1, 8)
        ]
        self.right_hit_frames = [
            pygame.transform.scale(frame, (int(frame.get_width() * self.scale_factor), int(frame.get_height() * self.scale_factor)))
            for frame in right_hit_frames_raw
        ]
        #Left Hit Frames
        left_hit_frames_raw = [
            pygame.image.load(f"assets/enemies/enemy2/left/hit/f{i}.png")
            for i in range(1, 8)
        ]
        self.left_hit_frames = [
            pygame.transform.scale(frame, (int(frame.get_width() * self.scale_factor), int(frame.get_height() * self.scale_factor)))
            for frame in left_hit_frames_raw
        ]

        #Death Frames (f1-f11; f12 asset is missing)
        death_frames_raw = [
            pygame.image.load(f"assets/enemies/enemy2/death/f{i}.png")
            for i in range(1, 13)
        ]
        self.death_frames = [
            pygame.transform.scale(frame, (int(frame.get_width() * self.scale_factor), int(frame.get_height() * self.scale_factor)))
            for frame in death_frames_raw
        ]

        #Attack Frames (direction-agnostic)
        attack_frames_raw = [
            pygame.image.load(f"assets/enemies/enemy2/attack/f{i}.png")
            for i in range(1, 5)
        ]
        self.attack_frames = [
            pygame.transform.scale(frame, (int(frame.get_width() * self.scale_factor), int(frame.get_height() * self.scale_factor)))
            for frame in attack_frames_raw
        ]

        #Projectile Frames
        projectile_scale = 2.5
        projectile_frames_raw = [
            pygame.image.load(f"assets/misc/enemy2-projectile/f{i}.png")
            for i in range(1, 4)
        ]
        self.projectile_frames = [
            pygame.transform.scale(frame, (int(frame.get_width() * projectile_scale), int(frame.get_height() * projectile_scale)))
            for frame in projectile_frames_raw
        ]

        # Animation sequences (back and forth)
        self.idle_sequence = [0, 1, 2, 3, 4, 3, 2, 1]
        self.hit_sequence = [0, 1, 2, 3, 4, 5, 6, 5, 4, 3, 2, 1]
        self.movement_sequence = [0, 1, 2, 1, 0, 3, 4, 3]
        self.attack_sequence = [0, 1, 2, 3]
        self.projectile_sequence = [0, 1, 2, 1]

        self.idle_frame_index = 0
        self.hit_frame_index = 0
        self.movement_frame_index = 0
        self.attack_frame_index = 0
        self.death_frame_index = 0

        # Set initial image BEFORE creating rect
        self.image = self.right_idle_frames[0]

        # Create collision rect from actual sprite bounds
        bounds = get_sprite_bounds(self.image)
        self.collision_rect = pygame.Rect(0, 0, bounds.width, bounds.height)
        self.collision_rect.center = (int(x), int(y))

        # Display rect centered on position
        self.rect = self.image.get_rect(center=(x, y))

        # Animation timing
        self.frame_counter = 0
        self.frame_speed = 5
        self.death_frame_speed = 2
        self.attack_frame_speed = 2
        self.hit_timer = 0
        self.hit_duration = 200

        #Shadow Frame Code
        self.shadow_image_raw = pygame.image.load("assets/misc/entity-shadow.png").convert_alpha()
        self.shadow = make_shadow(self.shadow_image_raw, self.right_idle_frames[0].get_width())

        #Enemy Health Bar Code
        self.healthbar = ProgressBar(self.rect.centerx,
                                    self.rect.top - 25,
                                    self.max_health,
                                    f"assets/misc/enemy-healthbar.png",
                                    self.scale_factor * 0.5,
                                    self.scale_factor * 0.5,
                                    xmargin=0.5,
                                    ymargin=1
                                    )

    def primary_attack(self, player):
        dx = player.x - self.x
        dy = player.y - self.y
        distance = (dx ** 2 + dy ** 2) ** 0.5

        current_time = pygame.time.get_ticks()
        elapsed_since_last_attack = current_time - self.time_from_last_attack

        if distance <= self.shoot_radius and elapsed_since_last_attack >= self.attack_cooldown:
            dir_x = dx / distance if distance != 0 else 0
            dir_y = dy / distance if distance != 0 else 0

            vx = dir_x * self.projectile_speed
            vy = dir_y * self.projectile_speed

            projectile = AnimatedProjectile(self.x, self.y, vx, vy, self.attack_damage, frames=self.projectile_frames, sequence=self.projectile_sequence)
            self.projectiles.add(projectile)

            self.is_attacking = True
            self.attack_timer = current_time
            self.time_from_last_attack = current_time

    def wave_update(self):
        if game.wave_number > self.last_wave_processed and game.wave_number > 1:
            super().wave_update()
            self.shoot_radius += 20
            self.healthbar.max_value = self.max_health

    def update(self, player):
        # Check if knockback should end
        if self.is_knockback:
            elapsed = pygame.time.get_ticks() - self.knockback_timer
            if elapsed >= self.knockback_duration:
                self.is_knockback = False
                self.velocity_x = 0
                self.velocity_y = 0

        if not player.is_dying:
            if not self.is_knockback:
                dx = player.x - self.x
                dy = player.y - self.y
                distance = (dx ** 2 + dy ** 2) ** 0.5
                if distance > self.shoot_radius:
                    self.movement(player)
                else:
                    self.velocity_x = 0
                    self.velocity_y = 0
                    self.is_moving = False
                    self.calculate_direction(player)  # Keep facing the player while stationary

            self.primary_attack(player)

        self.projectiles.update()

        super().update()

        # Keep collision rect synced with entity position
        self.collision_rect.center = self.rect.center

        self.healthbar.x = self.rect.centerx - (self.healthbar.container_width // 2)
        self.healthbar.y = self.rect.top - 25
        self.healthbar.update(self.current_health)

        # Check if hit animation should end
        if self.is_hit:
            elapsed = pygame.time.get_ticks() - self.hit_timer
            if elapsed >= self.hit_duration:
                self.is_hit = False
                self.idle_frame_index = 0

        # Check if attack animation should end
        if self.is_attacking:
            elapsed = pygame.time.get_ticks() - self.attack_timer
            if elapsed >= self.attack_duration:
                self.is_attacking = False
                self.attack_frame_index = 0

        # Update animation frame
        current_speed = self.death_frame_speed if self.is_dying else (self.attack_frame_speed if self.is_attacking else self.frame_speed)
        self.frame_counter += 1
        if self.frame_counter >= current_speed:
            self.frame_counter = 0

            if self.direction_facing == "left":
                idle_frames = self.left_idle_frames
                hit_frames = self.left_hit_frames
                movement_frames = self.left_movement_frames
            else:
                idle_frames = self.right_idle_frames
                hit_frames = self.right_hit_frames
                movement_frames = self.right_movement_frames

            if self.is_dying:
                if self.death_frame_index < len(self.death_frames):
                    self.image = self.death_frames[self.death_frame_index]
                    self.death_frame_index += 1
                else:
                    self.die()
                    self.death_drops_generation(player)
                    self.kill()
            elif self.is_hit:
                self.hit_frame_index = (self.hit_frame_index + 1) % len(self.hit_sequence)
                frame_to_show = self.hit_sequence[self.hit_frame_index]
                self.image = hit_frames[frame_to_show]
            elif self.is_attacking:
                if self.attack_frame_index < len(self.attack_sequence):
                    frame_to_show = self.attack_sequence[self.attack_frame_index]
                    self.image = self.attack_frames[frame_to_show]
                    self.attack_frame_index += 1
            elif self.is_moving:
                self.movement_frame_index = (self.movement_frame_index + 1) % len(self.movement_sequence)
                frame_to_show = self.movement_sequence[self.movement_frame_index]
                self.image = movement_frames[frame_to_show]
            else:
                self.idle_frame_index = (self.idle_frame_index + 1) % len(self.idle_sequence)
                frame_to_show = self.idle_sequence[self.idle_frame_index]
                self.image = idle_frames[frame_to_show]

        self.shadow = make_shadow(self.shadow_image_raw, self.image.get_width())