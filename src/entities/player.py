import pygame 
from .base_entity import BaseEntity
from src.utils.sprite_utils import get_sprite_bounds, make_shadow
from src.utils.assets import lazy_scaled_frames, load_image

class Player(BaseEntity):

    def __init__(self, x, y, direction=None, max_health=100, scale_factor=3):
        super().__init__(x, y, max_health)

        self.mana = 100
        self.direction = direction  # Track the player's facing direction
        self.weapons_inventory = {
            "gun": None,  # Placeholder for the player's gun
            "melee": None  # Placeholder for the player's melee weapon
        }  
        self.gun_inventory = []
        self.melee_inventory = []
        self.ammo = 70
        self.power_up = None  # currently held, unused power-up
        self.active_power_ups = []  # power-ups currently in effect
        self.is_invincible = False
        self.weapon_equipped = None  # Track which weapon is currently equipped
        self.previous_space_pressed = False
        self.movement_speed = 3.7 #3.7 is standard
        self.is_hit = False
        self.hit_timer = 0
        self.is_alive = True
        self.is_dying = False
        self.death_timer = 0
        self.color = (29, 116, 205)
        self.weapon_in_hand = True  # True if the player has a weapon in hand, False if unarmed

        #Player Design/Animation frames (Blaster or Sword)

        self.blank_idle_right = lazy_scaled_frames("assets/player/noWeapon/right/idle/f{i}.png", range(1, 6), scale_factor)
        self.blank_idle_left = lazy_scaled_frames("assets/player/noWeapon/left/idle/f{i}.png", range(1, 6), scale_factor)
        self.blank_movement = lazy_scaled_frames("assets/player/noWeapon/movement/f{i}.png", range(1, 6), scale_factor)

        self.blaster_idle_right = lazy_scaled_frames("assets/player/blaster/blaster-right/idle/f{i}.png", range(1, 6), scale_factor)
        self.blaster_idle_left = lazy_scaled_frames("assets/player/blaster/blaster-left/idle/f{i}.png", range(1, 6), scale_factor)
        self.blaster_move_right = lazy_scaled_frames("assets/player/blaster/blaster-right/movement/f{i}.png", range(1, 6), scale_factor)
        self.blaster_move_left = lazy_scaled_frames("assets/player/blaster/blaster-left/movement/f{i}.png", range(1, 6), scale_factor)

        self.sword_idle_left = lazy_scaled_frames("assets/player/sword/sword-left/idle-left/f{i}.png", range(1, 6), scale_factor)
        self.sword_idle_right = lazy_scaled_frames("assets/player/sword/sword-right/idle-right/f{i}.png", range(1, 6), scale_factor)
        self.sword_walk_left = lazy_scaled_frames("assets/player/sword/sword-left/movement-left/f{i}.png", range(1, 6), scale_factor)
        self.sword_walk_right = lazy_scaled_frames("assets/player/sword/sword-right/movement-right/f{i}.png", range(1, 6), scale_factor)

        self.shotgun_idle_right = lazy_scaled_frames("assets/player/shotgun/shotgun-right/idle/f{i}.png", range(1, 6), scale_factor)
        self.shotgun_idle_left = lazy_scaled_frames("assets/player/shotgun/shotgun-left/idle/f{i}.png", range(1, 6), scale_factor)
        self.shotgun_walk_right = lazy_scaled_frames("assets/player/shotgun/shotgun-right/movement/f{i}.png", range(1, 6), scale_factor)
        self.shotgun_walk_left = lazy_scaled_frames("assets/player/shotgun/shotgun-left/movement/f{i}.png", range(1, 6), scale_factor)

        self.sword_attack_left = lazy_scaled_frames("assets/player/sword/sword-left/attack-left/f{i}.png", range(1, 10), scale_factor)
        self.sword_attack_right = lazy_scaled_frames("assets/player/sword/sword-right/attack-right/f{i}.png", range(1, 10), scale_factor)

        self.boomerang_idle_left = lazy_scaled_frames("assets/player/boomerang/left/idle/f{i}.png", range(1, 6), scale_factor)
        self.boomerang_idle_right = lazy_scaled_frames("assets/player/boomerang/right/idle/f{i}.png", range(1, 6), scale_factor)
        self.boomerang_move_left = lazy_scaled_frames("assets/player/boomerang/left/movement/f{i}.png", range(1, 6), scale_factor)
        self.boomerang_move_right = lazy_scaled_frames("assets/player/boomerang/right/movement/f{i}.png", range(1, 6), scale_factor)



        self.death_frames = lazy_scaled_frames("assets/player/death/f{i}.png", range(1, 14), scale_factor)

        self.sword_hit_right = lazy_scaled_frames("assets/player/sword/sword-right/hit-right/f{i}.png", range(1, 6), scale_factor)
        self.blaster_hit_right = lazy_scaled_frames("assets/player/blaster/blaster-right/hit/f{i}.png", range(1, 6), scale_factor)
        self.shotgun_hit_right = lazy_scaled_frames("assets/player/shotgun/shotgun-right/hit/f{i}.png", range(1, 6), scale_factor)
        self.boomerang_hit_right = lazy_scaled_frames("assets/player/boomerang/right/hit/f{i}.png", range(1, 8), scale_factor)
        self.blank_hit_right = lazy_scaled_frames("assets/player/noWeapon/right/hit/f{i}.png", range(1, 8), scale_factor)

        self.sword_hit_left = lazy_scaled_frames("assets/player/sword/sword-left/hit-left/f{i}.png", range(1, 6), scale_factor)
        self.blaster_hit_left = lazy_scaled_frames("assets/player/blaster/blaster-left/hit/f{i}.png", range(1, 6), scale_factor)
        self.shotgun_hit_left = lazy_scaled_frames("assets/player/shotgun/shotgun-left/hit/f{i}.png", range(1, 6), scale_factor)
        self.boomerang_hit_left = lazy_scaled_frames("assets/player/boomerang/left/hit/f{i}.png", range(1, 8), scale_factor)
        self.blank_hit_left = lazy_scaled_frames("assets/player/noWeapon/left/hit/f{i}.png", range(1, 8), scale_factor)

        self.blaster_shoot = lazy_scaled_frames("assets/player/blaster/blaster-right/shoot/f{i}.png", range(1, 4), scale_factor)
        self.blaster_shoot_left = lazy_scaled_frames("assets/player/blaster/blaster-left/shoot/f{i}.png", range(1, 4), scale_factor)
        self.shotgun_shoot_right = lazy_scaled_frames("assets/player/shotgun/shotgun-right/shoot/f{i}.png", range(1, 4), scale_factor)
        self.shotgun_shoot_left = lazy_scaled_frames("assets/player/shotgun/shotgun-left/shoot/f{i}.png", range(1, 4), scale_factor)

        self.shadow_image_raw = load_image("assets/misc/entity-shadow.png")
        self.shadow = make_shadow(self.shadow_image_raw, self.blank_idle_right[0].get_width()*0.7)

        self.frame_counter = 0
        self.hit_frame_counter = 0
        self.death_frame_counter = 0
        self.frame_speed = 5
        self.attack_frame_speed = 2  # Faster animation for attacks
        self.death_frame_speed = 1  # Faster death animation
        self.is_moving = False
        self.cursor_side = "right"  # Track which side cursor is on
        self.is_attacking = False  # Track if player is in attack animation
        self.attack_start_time = 0  # When the attack started

        # Animation sequences
        self.idle_sequence = [0, 1, 2, 3, 4, 3, 2, 1]  # Breathe effect: 1-5 then 5-1
        self.walk_sequence = [0, 1, 2, 1, 0, 3, 4, 3, 0]  # Custom walk pattern
        self.idle_frame_index = 0
        self.walk_frame_index = 0
        self.attack_frame_index = 0  # For attack animation
        self.hit_frame_index = 0  # For hit animation
        self.death_frame_index = 0  # For death animation
        
        # Hit animation sequence (5 frames: play forward, then backward for recovery effect)
        self.hit_sequence = [0, 1, 2, 3, 4, 3, 2, 1, 0]
        self.hit_animation_speed = 1  # Frame speed for hit animation

        # Use a neutral frame until the first equipped weapon is updated.
        self.image = self.blank_idle_right[0]
        
        # Create collision rect from actual sprite bounds (crop transparent padding)
        bounds = get_sprite_bounds(self.image)
        self.collision_rect = pygame.Rect(0, 0, bounds.width, bounds.height)
        self.collision_rect.center = (int(x), int(y))
        
        # Display rect centered on position
        self.rect = self.image.get_rect(center=(x, y))
        # Create a smaller collision rect (about 60% of image size, centered on player)
        self.collision_rect = pygame.Rect(0, 0, int(self.rect.width * 0.6), int(self.rect.height * 0.6))
        self.collision_rect.center = (x, y)
        self.width = self.rect.width
        self.height = self.rect.height

    def handle_input(self):
        keys = pygame.key.get_pressed()
        self.velocity_x = 0
        self.velocity_y = 0

        if keys[pygame.K_a] or keys[pygame.K_d] or keys[pygame.K_w] or keys[pygame.K_s]:
            self.is_moving = True
        else:
            self.is_moving = False

        if keys[pygame.K_a]:
            self.velocity_x = self.movement_speed * -1
        if keys[pygame.K_d]:
            self.velocity_x = self.movement_speed
        if keys[pygame.K_w]:
            self.velocity_y = self.movement_speed * -1
        if keys[pygame.K_s]:
            self.velocity_y = self.movement_speed
        if self.weapon_equipped and self.weapon_equipped.is_automatic:
            if keys[pygame.K_SPACE]:
                self.use_weapon()
        elif self.weapon_equipped and not self.weapon_equipped.is_automatic:
            if keys[pygame.K_SPACE] and not self.previous_space_pressed:
                self.use_weapon()
            self.previous_space_pressed = keys[pygame.K_SPACE]
        if keys[pygame.K_r]:
            if self.weapon_equipped and self.weapon_equipped.weapon_type == "gun":
                self.ammo = self.weapon_equipped.reload(self.ammo)
        if keys[pygame.K_1]:
            if self.weapons_inventory["gun"] is not None:
                self.equip_weapon(self.weapons_inventory["gun"])
        if keys[pygame.K_2]:
            if self.weapons_inventory["melee"] is not None:
                self.equip_weapon(self.weapons_inventory["melee"])
        if self.power_up is not None:
            if keys[pygame.K_e]:
                self.power_up.use_powerup()
                if self.power_up.has_time_limit:
                    self.active_power_ups.append(self.power_up)
                self.power_up = None
        mouse_pos = pygame.mouse.get_pos()
        self.direction = self.calculate_direction(mouse_pos)

    def calculate_direction(self, target_pos):
        dx = target_pos[0] - self.rect.centerx
        dy = target_pos[1] - self.rect.centery
        distance = (dx**2 + dy**2) ** 0.5

        if distance == 0:
            return (0, 0)
        return (dx / distance, dy / distance)

    def get_idle_frames(self):
        """Get idle frame set based on equipped weapon and cursor side."""
        if self.weapon_equipped:
            if self.weapon_equipped.name == "Boomerang" and not self.weapon_in_hand:
                return self.blank_idle_left if self.cursor_side == "left" else self.blank_idle_right
            elif self.weapon_equipped.name == "blaster":
                return self.blaster_idle_left if self.cursor_side == "left" else self.blaster_idle_right
            elif self.weapon_equipped.name == "shotgun":
                return self.shotgun_idle_left if self.cursor_side == "left" else self.shotgun_idle_right
            elif self.weapon_equipped.name == "sword":
                return self.sword_idle_left if self.cursor_side == "left" else self.sword_idle_right
            elif self.weapon_equipped.name == "boomerang":
                return self.boomerang_idle_left if self.cursor_side == "left" else self.boomerang_idle_right

    def get_walk_frames(self):
        """Get walk frame set based on equipped weapon and cursor side."""
        if self.weapon_equipped:
            if self.weapon_equipped.name == "boomerang" and not self.weapon_in_hand:
                return self.blank_movement
            elif self.weapon_equipped.name == "blaster":
                return self.blaster_move_left if self.cursor_side == "left" else self.blaster_move_right
            elif self.weapon_equipped.name == "shotgun":
                return self.shotgun_walk_left if self.cursor_side == "left" else self.shotgun_walk_right
            elif self.weapon_equipped.name == "sword":
                return self.sword_walk_left if self.cursor_side == "left" else self.sword_walk_right
            elif self.weapon_equipped.name == "boomerang":
                return self.boomerang_move_left if self.cursor_side == "left" else self.boomerang_move_right


    def update(self):
        self.handle_input()  # Handle player input to update velocity
        super().update()  # Call the base class update to move the player

        # Update active power-ups and revert any that have expired
        for power_up in self.active_power_ups:
            power_up.update()
        self.active_power_ups = [p for p in self.active_power_ups if p.is_active]

        if self.weapon_equipped and self.weapon_equipped.weapon_type == "gun" and self.weapon_equipped.ammo == 0 and self.ammo > 0:
            self.ammo = self.weapon_equipped.reload(self.ammo)
        
        # Keep collision rect synced with player position
        self.collision_rect.center = self.rect.center

        # Check if player should die
        if not self.is_dying and self.current_health <= 0:
            self.is_dying = True
            self.death_timer = pygame.time.get_ticks()
            self.death_frame_index = 0

        # Update weapon angle for aiming (gun only) - for hit detection purposes
        if self.weapon_equipped and self.weapon_equipped.weapon_type == "gun":
            mouse_pos = pygame.mouse.get_pos()
            # Still calculate angle for aiming/projectile direction, but don't rotate sprite
            self.weapon_equipped.angle = self.calculate_angle_to_mouse(mouse_pos)

        # Update cursor side based on mouse position
        mouse_pos = pygame.mouse.get_pos()
        if mouse_pos[0] > self.rect.centerx:
            self.cursor_side = "right"
        else:
            self.cursor_side = "left"

        # Play death animation (takes highest priority)
        if self.is_dying:
            self.death_frame_counter += 1
            if self.death_frame_counter >= self.death_frame_speed:
                self.death_frame_counter = 0
                if self.death_frame_index < len(self.death_frames):
                    self.image = self.death_frames[self.death_frame_index]
                    self.death_frame_index += 1
                else:
                    # Leave the final frame visible until the main loop switches screens.
                    self.is_alive = False
        # Play hit animation when taking damage (takes priority over other animations)
        elif self.is_hit:
            # Select hit frames based on equipped weapon and cursor side
            if self.weapon_equipped and self.weapon_equipped.name == "blaster":
                hit_frames = self.blaster_hit_left if self.cursor_side == "left" else self.blaster_hit_right
            elif self.weapon_equipped and self.weapon_equipped.name == "shotgun":
                hit_frames = self.shotgun_hit_left if self.cursor_side == "left" else self.shotgun_hit_right
            elif self.weapon_equipped and self.weapon_equipped.name == "boomerang" and not self.weapon_in_hand:
                hit_frames = self.blank_hit_left if self.cursor_side == "left" else self.blank_hit_right
            elif self.weapon_equipped and self.weapon_equipped.name == "boomerang":
                hit_frames = self.boomerang_hit_left if self.cursor_side == "left" else self.boomerang_hit_right
            else:
                hit_frames = self.sword_hit_left if self.cursor_side == "left" else self.sword_hit_right
            
            # Update hit animation frame with separate counter
            self.hit_frame_counter += 1
            if self.hit_frame_counter >= self.hit_animation_speed:
                self.hit_frame_counter = 0
                # Play animation once, then end hit state
                if self.hit_frame_index < len(self.hit_sequence):
                    frame_to_show = self.hit_sequence[self.hit_frame_index]
                    self.image = hit_frames[frame_to_show]
                    self.hit_frame_index += 1
                else:
                    self.is_hit = False
                    self.hit_frame_index = 0
        # Handle gun shoot animation
        elif self.is_attacking and self.weapon_equipped and self.weapon_equipped.name == "blaster":
            shoot_frames = self.blaster_shoot_left if self.cursor_side == "left" else self.blaster_shoot
            self.frame_counter += 1
            if self.frame_counter >= self.attack_frame_speed:
                self.frame_counter = 0
                if self.attack_frame_index < len(shoot_frames):
                    self.image = shoot_frames[self.attack_frame_index]
                    self.attack_frame_index += 1
                else:
                    self.is_attacking = False
                    self.weapon_equipped.is_shooting = False
                    self.attack_frame_index = 0
        elif self.is_attacking and self.weapon_equipped and self.weapon_equipped.name == "shotgun":
            shoot_frames = self.shotgun_shoot_left if self.cursor_side == "left" else self.shotgun_shoot_right
            self.frame_counter += 1
            if self.frame_counter >= self.attack_frame_speed:
                self.frame_counter = 0
                if self.attack_frame_index < len(shoot_frames):
                    self.image = shoot_frames[self.attack_frame_index]
                    self.attack_frame_index += 1
                else:
                    self.is_attacking = False
                    self.weapon_equipped.is_shooting = False
                    self.attack_frame_index = 0
        # Handle melee attack animation
        elif self.is_attacking and self.weapon_equipped and self.weapon_equipped.name == "sword":
            # Show attack animation
            if self.cursor_side == "left":
                attack_frames = self.sword_attack_left
            else:
                attack_frames = self.sword_attack_right
            
            # Play attack animation at faster speed
            self.frame_counter += 1
            if self.frame_counter >= self.attack_frame_speed:
                self.frame_counter = 0
                if self.attack_frame_index < len(attack_frames):
                    self.image = attack_frames[self.attack_frame_index]
                    self.attack_frame_index += 1
                else:
                    # Animation finished, end attack state and sync weapon
                    self.is_attacking = False
                    if self.weapon_equipped and self.weapon_equipped.name == "sword":
                        self.weapon_equipped.is_attacking = False
                    self.attack_frame_index = 0
        else:
            # Get appropriate frame sets based on equipped weapon
            idle_frames = self.get_idle_frames()
            walk_frames = self.get_walk_frames()

            # Update animation based on movement state
            self.frame_counter += 1
            if self.frame_counter >= self.frame_speed:
                self.frame_counter = 0
                
                if self.is_moving:
                    # Use walk sequence
                    self.walk_frame_index = (self.walk_frame_index + 1) % len(self.walk_sequence)
                    frame_to_show = self.walk_sequence[self.walk_frame_index]
                    self.image = walk_frames[frame_to_show]
                else:
                    # Use idle sequence
                    self.idle_frame_index = (self.idle_frame_index + 1) % len(self.idle_sequence)
                    frame_to_show = self.idle_sequence[self.idle_frame_index]
                    self.image = idle_frames[frame_to_show]

        #Shadow Update
        self.shadow = make_shadow(self.shadow_image_raw, self.image.get_width()*0.7)

    
    def calculate_angle_to_mouse(self, mouse_pos):
        import math
        dx = mouse_pos[0] - self.rect.centerx
        dy = mouse_pos[1] - self.rect.centery
        return math.atan2(dy, dx)
        
    def weapon_swap(self, new_weapon):
        new_weapon_type = getattr(new_weapon, 'weapon_type', None)
        if new_weapon_type == "gun": 
            for i in range(len(self.gun_inventory)):
                if self.gun_inventory[i] == new_weapon:
                    self.weapons_inventory["gun"] = self.gun_inventory[i]
        elif new_weapon_type == "melee":
            for i in range(len(self.melee_inventory)):
                if self.melee_inventory[i] == new_weapon:
                    self.weapons_inventory["melee"] = self.melee_inventory[i]
        else:
            print("Invalid weapon type for swapping")

    def equip_weapon(self, weapon):
        if weapon.weapon_type in self.weapons_inventory:
            # Clear attack state on the outgoing weapon before switching
            if self.weapon_equipped:
                if hasattr(self.weapon_equipped, 'is_attacking'):
                    self.weapon_equipped.is_attacking = False
                if hasattr(self.weapon_equipped, 'is_shooting'):
                    self.weapon_equipped.is_shooting = False
            self.is_attacking = False
            self.attack_frame_index = 0

            self.weapon_equipped = weapon
            if hasattr(weapon, 'update_position'):
                mouse_pos = pygame.mouse.get_pos()
                weapon.update_position((self.rect.centerx, self.rect.centery), mouse_pos)

    def use_weapon(self):
        if self.weapon_equipped:
            attack_succeeded = self.weapon_equipped.attack(self.rect.center, self.direction)
            # Trigger attack animation for melee weapons ONLY if attack succeeded
            if attack_succeeded:
                if self.weapon_equipped.weapon_type == "melee":
                    self.is_attacking = True
                    self.weapon_equipped.is_attacking = True  # Sync weapon state
                    self.attack_start_time = pygame.time.get_ticks()
                    self.attack_frame_index = 0
                elif self.weapon_equipped.weapon_type == "gun":
                    self.is_attacking = True
                    self.weapon_equipped.is_shooting = True
                    self.attack_start_time = pygame.time.get_ticks()
                    self.attack_frame_index = 0
        else:
            print("No weapon equipped")

    def take_damage(self, damage_amount):
        """Apply damage to the player and trigger hit animation."""
        if self.is_invincible:
            return
        self.current_health -= damage_amount
        if self.current_health < 0:
            self.current_health = 0
        self.is_hit = True
        self.hit_timer = pygame.time.get_ticks()
        self.hit_frame_index = 0  # Reset hit animation to start from first frame