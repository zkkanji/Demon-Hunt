import pygame
import src.game as game
from .enemy_base import Enemy
from src.utils.progressbar import ProgressBar
from src.entities.projectile import BoomerangProjectile
from src.utils.sprite_utils import get_sprite_bounds, make_shadow
from src.utils.assets import load_image, scale_surface

class Devil3(Enemy):

    def __init__(self, x, y):
        super().__init__(x, 
                        y,
                        attack_duration=200, 
                        max_health=50, 
                        attack_damage=10,
                        knockback_damage=6,
                        movement_speed=1.5,
                        scale_factor=2.5,
                        attack_cooldown=1100,
                        enemy_type="scythe devil")
        self.shoot_radius = 325
        self.projectile_speed = 4.5
        self.projectiles = pygame.sprite.Group()
        
        #With Weapon Frames
        idle_frames_right = [
            load_image(f"assets/enemies/enemy3/withWeapon/right/idle/f{i}.png")
            for i in range(1, 6)
        ]
        idle_frames_left = [
            load_image(f"assets/enemies/enemy3/withWeapon/left/idle/f{i}.png")
            for i in range(1, 6)
        ]
        move_frames_right = [
            load_image(f"assets/enemies/enemy3/withWeapon/right/movement/f{i}.png")
            for i in range(1, 6)
        ]
        move_frames_left = [
            load_image(f"assets/enemies/enemy3/withWeapon/left/movement/f{i}.png")
            for i in range(1, 6)
        ]
        hit_frames_right = [
            load_image(f"assets/enemies/enemy3/withWeapon/right/hit/f{i}.png")
            for i in range(1, 8)
        ]
        hit_frames_left = [
            load_image(f"assets/enemies/enemy3/withWeapon/left/hit/f{i}.png")
            for i in range(1, 8)
        ]

        #No Weapon Frames
        idle_frames_no_weapon = [
            load_image(f"assets/enemies/enemy3/noWeapon/idle/f{i}.png")
            for i in range(1, 6)
        ]

        move_frames_no_weapon = [
            load_image(f"assets/enemies/enemy3/noWeapon/movement/f{i}.png")
            for i in range(1, 6)
        ]
        hit_frames_no_weapon = [
            load_image(f"assets/enemies/enemy3/noWeapon/hit/f{i}.png")
            for i in range(1, 8)
        ]

        #Death Frames
        death_frames_raw = [
            load_image(f"assets/enemies/enemy3/death/f{i}.png")
            for i in range(1, 14)
        ]

        #All Scaled Frames
        self.idle_frames_right = [
            scale_surface(frame, int(frame.get_width() * self.scale_factor), int(frame.get_height() * self.scale_factor)) 
            for frame in idle_frames_right
            ]
        self.idle_frames_left = [
            scale_surface(frame, int(frame.get_width() * self.scale_factor), int(frame.get_height() * self.scale_factor)) 
            for frame in idle_frames_left
            ]
        self.move_frames_right = [
            scale_surface(frame, int(frame.get_width() * self.scale_factor), int(frame.get_height() * self.scale_factor)) 
            for frame in move_frames_right
            ]
        self.move_frames_left = [
            scale_surface(frame, int(frame.get_width() * self.scale_factor), int(frame.get_height() * self.scale_factor)) 
            for frame in move_frames_left
            ]
        self.hit_frames_right = [
            scale_surface(frame, int(frame.get_width() * self.scale_factor), int(frame.get_height() * self.scale_factor)) 
            for frame in hit_frames_right
            ]
        self.hit_frames_left = [
            scale_surface(frame, int(frame.get_width() * self.scale_factor), int(frame.get_height() * self.scale_factor)) 
            for frame in hit_frames_left
            ]
        self.idle_frames_no_weapon = [
            scale_surface(frame, int(frame.get_width() * self.scale_factor), int(frame.get_height() * self.scale_factor)) 
            for frame in idle_frames_no_weapon
            ]
        self.move_frames_no_weapon = [
            scale_surface(frame, int(frame.get_width() * self.scale_factor), int(frame.get_height() * self.scale_factor)) 
            for frame in move_frames_no_weapon
            ]
        self.hit_frames_no_weapon = [
            scale_surface(frame, int(frame.get_width() * self.scale_factor), int(frame.get_height() * self.scale_factor)) 
            for frame in hit_frames_no_weapon
            ]
        self.death_frames = [
            scale_surface(frame, int(frame.get_width() * self.scale_factor), int(frame.get_height() * self.scale_factor)) 
            for frame in death_frames_raw
            ]

        #Animation Sequences
        self.idle_sequence = [0, 1, 2, 3, 4, 3, 2, 1]
        self.hit_sequence = [0, 1, 2, 3, 4, 5, 6, 5, 4, 3, 2, 1, 0]
        self.movement_sequence = [0, 1, 2, 1, 0, 3, 4, 3]
        
        self.idle_frame_index = 0
        self.hit_frame_index = 0
        self.movement_frame_index = 0
        self.death_frame_index = 0

        #Initial Sprite Frame
        self.image = self.idle_frames_right[0]

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
        self.hit_timer = 0
        self.hit_duration = 200
        
        #Shadow Frame Code
        self.shadow_image_raw = load_image("assets/misc/entity-shadow.png")
        self.shadow = make_shadow(self.shadow_image_raw, self.idle_frames_right[0].get_width())
        
        #Scythe Frame Code
        scythe_scale = 2.8
        scythe_projectile_image = load_image("assets/misc/scythe-projectile.png")
        self.scythe_image = scale_surface(scythe_projectile_image, int(scythe_projectile_image.get_width() * scythe_scale), int(scythe_projectile_image.get_height() * scythe_scale))

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
        

        self.color = (67, 64, 64)

    def primary_attack(self, player):
        dx = player.x - self.x
        dy = player.y - self.y
        distance = (dx ** 2 + dy ** 2) ** 0.5

        current_time = pygame.time.get_ticks()
        elapsed_since_last_attack = current_time - self.time_from_last_attack

        if (
            distance <= self.shoot_radius
            and elapsed_since_last_attack >= self.attack_cooldown
            and not self.projectiles
        ):
            direction = pygame.Vector2(dx, dy)
            if direction.length_squared() == 0:
                return
            direction = direction.normalize()

            projectile = BoomerangProjectile(
                self.x,
                self.y,
                direction.x * self.projectile_speed,
                direction.y * self.projectile_speed,
                self.attack_damage,
                self,
                self.shoot_radius,
                sprite_image=self.scythe_image,
            )
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
        if self.is_knockback:
            elapsed = pygame.time.get_ticks() - self.knockback_timer
            if elapsed >= self.knockback_duration:
                self.is_knockback = False
                self.velocity_x = 0
                self.velocity_y = 0

        if self.is_dying:
            for projectile in self.projectiles:
                projectile.kill()
        elif not player.is_dying:
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
                    self.calculate_direction(player)

            self.primary_attack(player)

        self.projectiles.update()

        super().update()

        self.collision_rect.center = self.rect.center

        self.healthbar.x = self.rect.centerx - (self.healthbar.container_width // 2)
        self.healthbar.y = self.rect.top - 25
        self.healthbar.update(self.current_health)

        if self.is_hit:
            elapsed = pygame.time.get_ticks() - self.hit_timer
            if elapsed >= self.hit_duration:
                self.is_hit = False
                self.idle_frame_index = 0

        if self.is_attacking:
            elapsed = pygame.time.get_ticks() - self.attack_timer
            if elapsed >= self.attack_duration:
                self.is_attacking = False

        current_speed = self.death_frame_speed if self.is_dying else self.frame_speed
        self.frame_counter += 1
        if self.frame_counter >= current_speed:
            self.frame_counter = 0

            if self.direction_facing == "left":
                idle_frames = self.idle_frames_left
                hit_frames = self.hit_frames_left
                movement_frames = self.move_frames_left
            else:
                idle_frames = self.idle_frames_right
                hit_frames = self.hit_frames_right
                movement_frames = self.move_frames_right

            no_weapon = bool(self.projectiles)
            if no_weapon:
                idle_frames = self.idle_frames_no_weapon
                hit_frames = self.hit_frames_no_weapon
                movement_frames = self.move_frames_no_weapon

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
            elif self.is_moving:
                self.movement_frame_index = (self.movement_frame_index + 1) % len(self.movement_sequence)
                frame_to_show = self.movement_sequence[self.movement_frame_index]
                self.image = movement_frames[frame_to_show]
            else:
                self.idle_frame_index = (self.idle_frame_index + 1) % len(self.idle_sequence)
                frame_to_show = self.idle_sequence[self.idle_frame_index]
                self.image = idle_frames[frame_to_show]

        self.shadow = make_shadow(self.shadow_image_raw, self.image.get_width())