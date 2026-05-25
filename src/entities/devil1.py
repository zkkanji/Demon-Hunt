import pygame
import math
from .enemy_base import Enemy
from src.utils.progressbar import ProgressBar
from .sword_sweep import SwordSweep
from src.utils.sprite_utils import get_sprite_bounds
from src.constants import FPS

class Devil(Enemy):
    
    def __init__(self, x, y):
        super().__init__(x, y, attack_duration=400, max_health=50, attack_damage=7, knockback_damage=4, movement_speed=1.5, scale_factor=2.5, attack_cooldown=900)

        self.attack_radius = 175
        self.melee_sweeps = pygame.sprite.Group()  # Group to manage active melee sweeps
        #idle frames
        left_idle_raw_frames = [
            pygame.image.load(f"assets/enemies/enemy1/left/idle/idle{i}.png")
            for i in range(1, 6)
        ]
        right_idle_raw_frames = [
            pygame.image.load(f"assets/enemies/enemy1/right/idle/idle{i}.png")
            for i in range(1, 6)
        ]
        self.left_idle_frames = [
            pygame.transform.scale(frame, (int(frame.get_width() * self.scale_factor), int(frame.get_height() * self.scale_factor)))
            for frame in left_idle_raw_frames
        ]
        self.right_idle_frames = [
            pygame.transform.scale(frame, (int(frame.get_width() * self.scale_factor), int(frame.get_height() * self.scale_factor)))
            for frame in right_idle_raw_frames
        ]

        #hit frames
        left_hit_raw_frames = [
            pygame.image.load(f"assets/enemies/enemy1/left/hit/hit{i}.png")
            for i in range(1, 8)
        ]
        right_hit_raw_frames = [
            pygame.image.load(f"assets/enemies/enemy1/right/hit/hit{i}.png")
            for i in range(1, 8)
        ]
        self.left_hit_frames = [
            pygame.transform.scale(frame, (int(frame.get_width() * self.scale_factor), int(frame.get_height() * self.scale_factor)))
            for frame in left_hit_raw_frames
        ]
        self.right_hit_frames = [
            pygame.transform.scale(frame, (int(frame.get_width() * self.scale_factor), int(frame.get_height() * self.scale_factor)))
            for frame in right_hit_raw_frames
        ]

        #movement frames
        left_movement_raw_frames = [
            pygame.image.load(f"assets/enemies/enemy1/left/movement/move{i}.png")
            for i in range(1, 6)
        ]
        right_movement_raw_frames = [
            pygame.image.load(f"assets/enemies/enemy1/right/movement/move{i}.png")
            for i in range(1, 6)
        ]
        self.left_movement_frames = [
            pygame.transform.scale(frame, (int(frame.get_width() * self.scale_factor), int(frame.get_height() * self.scale_factor)))
            for frame in left_movement_raw_frames
        ]
        self.right_movement_frames = [
            pygame.transform.scale(frame, (int(frame.get_width() * self.scale_factor), int(frame.get_height() * self.scale_factor)))
            for frame in right_movement_raw_frames
        ]

        #attack frames
        left_attack_raw_frames = [
            pygame.image.load(f"assets/enemies/enemy1/left/attack/attack{i}.png")
            for i in range(1, 10)
        ]
        right_attack_raw_frames = [
            pygame.image.load(f"assets/enemies/enemy1/right/attack/attack{i}.png")
            for i in range(1, 10)
        ]
        self.left_attack_frames = [
            pygame.transform.scale(frame, (int(frame.get_width() * self.scale_factor), int(frame.get_height() * self.scale_factor)))
            for frame in left_attack_raw_frames
        ]
        self.right_attack_frames = [
            pygame.transform.scale(frame, (int(frame.get_width() * self.scale_factor), int(frame.get_height() * self.scale_factor)))
            for frame in right_attack_raw_frames
        ]

        #death frames
        death_frames_raw = [
            pygame.image.load(f"assets/enemies/enemy1/death/death{i}.png")
            for i in range(1, 13)
        ]
        self.death_frames = [
            pygame.transform.scale(frame, (int(frame.get_width() * self.scale_factor), int(frame.get_height() * self.scale_factor)))
            for frame in death_frames_raw
        ]

        #Attack melee sweep frames
        attack_sweep_scale = 4
        raw_sweep_frames = [
            pygame.image.load(f"assets/misc/enemy1-melee-sweep/sweep{i}.png")
            for i in range(1, 14)
        ]
        self.sweep_frames = [
            pygame.transform.scale(frame, (int(frame.get_width() * attack_sweep_scale), int(frame.get_height() * attack_sweep_scale)))
            for frame in raw_sweep_frames
        ]

        # Animation sequences (back and forth)
        self.idle_sequence = [0, 1, 2, 3, 4, 3, 2, 1]
        self.hit_sequence = [0, 1, 2, 3, 4, 5, 6, 5, 4, 3, 2, 1]
        self.movement_sequence = [0, 1, 2, 1, 0, 3, 4, 3]
        self.attack_sequence = [0, 1, 2, 3, 4, 5, 6, 7, 8]  # 9 attack frames, played once

        self.idle_frame_index = 0
        self.hit_frame_index = 0
        self.movement_frame_index = 0
        self.attack_frame_index = 0
        self.death_frame_index = 0

        # Set initial image BEFORE creating rect (use right_idle_frames since default direction is "right")
        self.image = self.right_idle_frames[0]
        
        # Create collision rect from actual sprite bounds (crop transparent padding)
        bounds = get_sprite_bounds(self.image)
        self.collision_rect = pygame.Rect(0, 0, bounds.width, bounds.height)
        self.collision_rect.center = (int(x), int(y))
        
        # Display rect centered on position
        self.rect = self.image.get_rect(center=(x, y))
        
        # Animation timing
        self.frame_counter = 0
        self.frame_speed = 5  # Match player frame speed
        self.death_frame_speed = 2  # Faster death animation
        self.attack_frame_speed = 2 # Faster attack animation
        self.hit_timer = 0
        self.hit_duration = 200  # milliseconds

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
        """Attack the player with a melee sweep if in range and cooldown is ready."""
        dx = player.x - self.x
        dy = player.y - self.y
        distance = (dx ** 2 + dy ** 2) ** 0.5

        # Check if player is in attack radius and cooldown is ready
        current_time = pygame.time.get_ticks()
        elapsed_since_last_attack = current_time - self.time_from_last_attack
        
        if distance <= self.attack_radius and elapsed_since_last_attack >= self.attack_cooldown:
            # Calculate angle toward player
            angle = math.atan2(self.direction[1], self.direction[0])
            spawn_offset = 15
            # Spawn sweep at offset from enemy center
            spawn_x = self.x + self.direction[0] * spawn_offset
            spawn_y = self.y + self.direction[1] * spawn_offset

            # Calculate velocity so sweep travels attack_radius distance in attack_duration
            velocity = (self.attack_radius * 1000) / (self.attack_duration * FPS)  # pixels per frame
            vx = self.direction[0] * velocity
            vy = self.direction[1] * velocity

            # Create sweep projectile
            sweep = SwordSweep(spawn_x, spawn_y, vx, vy, self.attack_damage, self.attack_duration, self.sweep_frames, angle=angle)
            self.melee_sweeps.add(sweep)

            # Set attack state
            self.is_attacking = True
            self.attack_timer = current_time
            self.time_from_last_attack = current_time  # Reset cooldown timer

    def update(self, player):
        # Check if knockback should end
        if self.is_knockback:
            elapsed = pygame.time.get_ticks() - self.knockback_timer
            if elapsed >= self.knockback_duration:
                self.is_knockback = False
                self.velocity_x = 0
                self.velocity_y = 0
        
        # Only perform AI actions (movement/attack) if player is still alive
        if not player.is_dying:
            # Only perform regular movement if not in knockback state
            if not self.is_knockback:
                self.movement(player)  # Update movement towards player
            
            # Call attack logic
            self.primary_attack(player)
        
        # Update melee sweeps
        self.melee_sweeps.update()
        
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
                self.idle_frame_index = 0  # Reset to start of idle
        
        # Check if attack animation should end
        if self.is_attacking:
            elapsed = pygame.time.get_ticks() - self.attack_timer
            if elapsed >= self.attack_duration:
                self.is_attacking = False
                self.attack_frame_index = 0  # Reset for next attack
        
        # Update animation frame with adaptive speed
        current_speed = 0
        if self.is_dying:
            current_speed = self.death_frame_speed
        elif self.is_attacking:
            current_speed = self.attack_frame_speed
        else:
            current_speed = self.frame_speed
        self.frame_counter += 1
        if self.frame_counter >= current_speed:
            self.frame_counter = 0
            
            # Select directional frames based on facing direction
            if self.direction_facing == "left":
                idle_frames = self.left_idle_frames
                hit_frames = self.left_hit_frames
                movement_frames = self.left_movement_frames
                attack_frames = self.left_attack_frames
            else:
                idle_frames = self.right_idle_frames
                hit_frames = self.right_hit_frames
                movement_frames = self.right_movement_frames
                attack_frames = self.right_attack_frames
            
            if self.is_dying:
                if self.death_frame_index < len(self.death_frames):
                    self.image = self.death_frames[self.death_frame_index]
                    self.death_frame_index += 1
                else:
                    self.kill()  
            elif self.is_hit:
                # Play hit animation (back and forth)
                self.hit_frame_index = (self.hit_frame_index + 1) % len(self.hit_sequence)
                frame_to_show = self.hit_sequence[self.hit_frame_index]
                self.image = hit_frames[frame_to_show]
            elif self.is_attacking:
                # Play attack animation once through
                if self.attack_frame_index < len(self.attack_sequence):
                    frame_to_show = self.attack_sequence[self.attack_frame_index]
                    self.image = attack_frames[frame_to_show]
                    self.attack_frame_index += 1
            elif self.is_moving:
                # Play movement animation
                self.movement_frame_index = (self.movement_frame_index + 1) % len(self.movement_sequence)
                frame_to_show = self.movement_sequence[self.movement_frame_index]
                self.image = movement_frames[frame_to_show]
            else:
                # Play idle animation (back and forth, looping)
                self.idle_frame_index = (self.idle_frame_index + 1) % len(self.idle_sequence)
                frame_to_show = self.idle_sequence[self.idle_frame_index]
                self.image = idle_frames[frame_to_show]
        
