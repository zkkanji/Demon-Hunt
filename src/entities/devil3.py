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
            pygame.image.load(f"assets/enemies/devil3/withWeapon/right/idle/f{i}.png").convert_alpha()
            for i in range(1, 6)
        ]
        idle_frames_left = [
            pygame.image.load(f"assets/enemies/devil3/withWeapon/left/idle/f{i}.png").convert_alpha()
            for i in range(1, 6)
        ]
        move_frames_right = [
            pygame.image.load(f"assets/enemies/devil3/withWeapon/right/movement/f{i}.png").convert_alpha()
            for i in range(1, 6)
        ]
        move_frames_left = [
            pygame.image.load(f"assets/enemies/devil3/withWeapon/left/movement/f{i}.png").convert_alpha()
            for i in range(1, 6)
        ]
        hit_frames_right = [
            pygame.image.load(f"assets/enemies/devil3/withWeapon/right/hit/f{i}.png").convert_alpha()
            for i in range(1, 8)
        ]
        hit_frames_left = [
            pygame.image.load(f"assets/enemies/devil3/withWeapon/left/hit/f{i}.png").convert_alpha()
            for i in range(1, 8)
        ]

        #No Weapon Frames
        idle_frames_right_no_weapon = [
            pygame.image.load(f"assets/enemies/devil3/noWeapon/right/idle/f{i}.png").convert_alpha()
            for i in range(1, 6)
        ]
        idle_frames_left_no_weapon = [
            pygame.image.load(f"assets/enemies/devil3/noWeapon/left/idle/f{i}.png").convert_alpha()
            for i in range(1, 6)
        ]
        move_frames_right_no_weapon = [
            pygame.image.load(f"assets/enemies/devil3/noWeapon/right/movement/f{i}.png").convert_alpha()
            for i in range(1, 6)
        ]
        move_frames_left_no_weapon = [
            pygame.image.load(f"assets/enemies/devil3/noWeapon/left/movement/f{i}.png").convert_alpha()
            for i in range(1, 6)
        ]
        hit_frames_right_no_weapon = [
            pygame.image.load(f"assets/enemies/devil3/noWeapon/right/hit/f{i}.png").convert_alpha()
            for i in range(1, 8)
        ]
        hit_frames_left_no_weapon = [
            pygame.image.load(f"assets/enemies/devil3/noWeapon/left/hit/f{i}.png").convert_alpha()
            for i in range(1, 8)
        ]

        #Death Frames
        death_frames_raw = [
            pygame.image.load(f"assets/enemies/devil3/death/f{i}.png").convert_alpha()
            for i in range(1, 14)
        ]

        #All Scaled Frames
        self.idle_frames_right = [pygame.transform.scale(frame.convert_alpha(), (frame.get_width() * self.scale_factor, frame.get_height() * self.scale_factor)) for frame in idle_frames_right]
        self.idle_frames_left = [pygame.transform.scale(frame.convert_alpha(), (frame.get_width() * self.scale_factor, frame.get_height() * self.scale_factor)) for frame in idle_frames_left]
        self.move_frames_right = [pygame.transform.scale(frame.convert_alpha(), (frame.get_width() * self.scale_factor, frame.get_height() * self.scale_factor)) for frame in move_frames_right]
        self.move_frames_left = [pygame.transform.scale(frame.convert_alpha(), (frame.get_width() * self.scale_factor, frame.get_height() * self.scale_factor)) for frame in move_frames_left]
        self.hit_frames_right = [pygame.transform.scale(frame.convert_alpha(), (frame.get_width() * self.scale_factor, frame.get_height() * self.scale_factor)) for frame in hit_frames_right]
        self.hit_frames_left = [pygame.transform.scale(frame.convert_alpha(), (frame.get_width() * self.scale_factor, frame.get_height() * self.scale_factor)) for frame in hit_frames_left]
        self.idle_frames_right_no_weapon = [pygame.transform.scale(frame.convert_alpha(), (frame.get_width() * self.scale_factor, frame.get_height() * self.scale_factor)) for frame in idle_frames_right_no_weapon]
        self.idle_frames_left_no_weapon = [pygame.transform.scale(frame.convert_alpha(), (frame.get_width() * self.scale_factor, frame.get_height() * self.scale_factor)) for frame in idle_frames_left_no_weapon]
        self.move_frames_right_no_weapon = [pygame.transform.scale(frame.convert_alpha(), (frame.get_width() * self.scale_factor, frame.get_height() * self.scale_factor)) for frame in move_frames_right_no_weapon]
        self.move_frames_left_no_weapon = [pygame.transform.scale(frame.convert_alpha(), (frame.get_width() * self.scale_factor, frame.get_height() * self.scale_factor)) for frame in move_frames_left_no_weapon]
        self.hit_frames_right_no_weapon = [pygame.transform.scale(frame.convert_alpha(), (frame.get_width() * self.scale_factor, frame.get_height() * self.scale_factor)) for frame in hit_frames_right_no_weapon]
        self.hit_frames_left_no_weapon = [pygame.transform.scale(frame.convert_alpha(), (frame.get_width() * self.scale_factor, frame.get_height() * self.scale_factor)) for frame in hit_frames_left_no_weapon]
        self.death_frames = [pygame.transform.scale(frame.convert_alpha(), (frame.get_width() * self.scale_factor, frame.get_height() * self.scale_factor)) for frame in death_frames_raw]

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
        

        self.color = (67, 64, 64)

    def primary_attack(self, player):
        pass

    def wave_update(self):
        pass

    def update(self, player):
        pass