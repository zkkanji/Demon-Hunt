import pygame
from .enemy_base import Enemy
from src.utils.progressbar import ProgressBar
from src.utils.sprite_utils import get_sprite_bounds

class Devil(Enemy):
    
    def __init__(self, x, y):
        super().__init__(x, y, color=(255, 0, 0), max_health=15, movement_speed=6)

        idle_frames_raw = [
            pygame.image.load(f"assets/enemies/enemy1/enemy1idle/enemy1idle{i}.png")
            for i in range(1, 6)
        ]
        hit_frames_raw = [
            pygame.image.load(f"assets/enemies/enemy1/enemy1hit/enemy1hit{i}.png")
            for i in range(1, 8)
        ]
        movement_frames = [
            pygame.image.load(f"assets/enemies/enemy1/enemy1movement/enemy1-move{i}.png")
            for i in range(1, 6)
        ]
        death_frames = [
            pygame.image.load(f"assets/enemies/enemy1/enemy1death/death{i}.png")
            for i in range(1, 13)
        ]

        self.idle_frames = [pygame.transform.scale(frame, (frame.get_width() * self.scale_factor, frame.get_height() * self.scale_factor)) for frame in idle_frames_raw]
        self.hit_frames = [pygame.transform.scale(frame, (frame.get_width() * self.scale_factor, frame.get_height() * self.scale_factor)) for frame in hit_frames_raw]
        self.movement_frames = [pygame.transform.scale(frame, (frame.get_width() * self.scale_factor, frame.get_height() * self.scale_factor)) for frame in movement_frames]
        self.death_frames = [pygame.transform.scale(frame, (frame.get_width() * self.scale_factor, frame.get_height() * self.scale_factor)) for frame in death_frames]

        # Animation sequences (back and forth)
        self.idle_sequence = list(range(len(self.idle_frames))) + list(range(len(self.idle_frames) - 2, 0, -1))
        self.hit_sequence = list(range(len(self.hit_frames))) + list(range(len(self.hit_frames) - 2, 0, -1))
        self.movement_sequence = [0, 1, 2, 1, 0, 3, 4, 4]

        self.idle_frame_index = 0
        self.hit_frame_index = 0
        self.death_frame_index = 0

        # Set initial image BEFORE creating rect
        self.image = self.idle_frames[0]
        
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
                                    ymargin=1.5
                                    )

    def primary_attack(self, player):
        # Implement the logic for the primary attack (e.g., shoot a projectile)
        pass

    def update(self):
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
        
        # Update animation frame with adaptive speed
        current_speed = self.death_frame_speed if self.is_dying else self.frame_speed
        self.frame_counter += 1
        if self.frame_counter >= current_speed:
            self.frame_counter = 0
            
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
                self.image = self.hit_frames[frame_to_show]
            else:
                # Play idle animation (back and forth, looping)
                self.idle_frame_index = (self.idle_frame_index + 1) % len(self.idle_sequence)
                frame_to_show = self.idle_sequence[self.idle_frame_index]
                self.image = self.idle_frames[frame_to_show]
        
