import pygame 
from .base_entity import BaseEntity
from src.utils.sprite_utils import get_sprite_bounds

class Player(BaseEntity):

    def __init__(self, x, y, color=(0, 0, 255), direction=None, max_health=100, scale_factor=3):
        super().__init__(x, y, color, max_health)

        self.direction = direction  # Track the player's facing direction
        self.weapons_inventory = {
            "gun": None,  # Placeholder for the player's gun
            "melee": None  # Placeholder for the player's melee weapon
        }  
        self.misc_inventory = {
            "ammo" : 1000
        }
        self.weapon_equipped = None  # Track which weapon is currently equipped
        self.previous_space_pressed = False
        self.movement_speed = 5

        #Player Design/Animation frames (Blaster or Sword)
        #Blaster Raw Frames (Left and Right)
        blaster_idle_right_raw =[
            pygame.image.load(f"assets/player/blaster/blaster-right/idle/blaster-idle-right{i}.png")
            for i in range(1, 6)
        ]
        blaster_idle_left_raw = [
            pygame.image.load(f"assets/player/blaster/blaster-left/idle/blaster-idle-left{i}.png")
            for i in range(1, 6)
        ]
        blaster_move_right_raw = [
            pygame.image.load(f"assets/player/blaster/blaster-right/movement/blaster-move-right{i}.png")
            for i in range(1, 6)
        ]
        blaster_move_left_raw = [
            pygame.image.load(f"assets/player/blaster/blaster-left/movement/blaster-move-left{i}.png")
            for i in range(1, 6)
        ]

        # Scale blaster frames
        self.blaster_idle_right = [
            pygame.transform.scale(frame, (int(frame.get_width() * scale_factor), int(frame.get_height() * scale_factor)))
            for frame in blaster_idle_right_raw
        ]
        self.blaster_idle_left = [
            pygame.transform.scale(frame, (int(frame.get_width() * scale_factor), int(frame.get_height() * scale_factor)))
            for frame in blaster_idle_left_raw
        ]
        self.blaster_move_right = [
            pygame.transform.scale(frame, (int(frame.get_width() * scale_factor), int(frame.get_height() * scale_factor)))
            for frame in blaster_move_right_raw
        ]
        self.blaster_move_left = [
            pygame.transform.scale(frame, (int(frame.get_width() * scale_factor), int(frame.get_height() * scale_factor)))
            for frame in blaster_move_left_raw
        ]

        # Load sword frame sets (left and right)
        sword_idle_left_raw = [
            pygame.image.load(f"assets/player/sword/sword-left/idle-left/sword-idle-left{i}.png")
            for i in range(1, 6)
        ]
        sword_idle_right_raw = [
            pygame.image.load(f"assets/player/sword/sword-right/idle-right/sword-idle-right{i}.png")
            for i in range(1, 6)
        ]
        sword_walk_left_raw = [
            pygame.image.load(f"assets/player/sword/sword-left/movement-left/sword-move-left{i}.png")
            for i in range(1, 6)
        ]
        sword_walk_right_raw = [
            pygame.image.load(f"assets/player/sword/sword-right/movement-right/sword-move-right{i}.png")
            for i in range(1, 6)
        ]
        
        # Scale sword frames
        self.sword_idle_left = [
            pygame.transform.scale(frame, (int(frame.get_width() * scale_factor), int(frame.get_height() * scale_factor)))
            for frame in sword_idle_left_raw
        ]
        self.sword_idle_right = [
            pygame.transform.scale(frame, (int(frame.get_width() * scale_factor), int(frame.get_height() * scale_factor)))
            for frame in sword_idle_right_raw
        ]
        self.sword_walk_left = [
            pygame.transform.scale(frame, (int(frame.get_width() * scale_factor), int(frame.get_height() * scale_factor)))
            for frame in sword_walk_left_raw
        ]
        self.sword_walk_right = [
            pygame.transform.scale(frame, (int(frame.get_width() * scale_factor), int(frame.get_height() * scale_factor)))
            for frame in sword_walk_right_raw
        ]

        # Load sword attack frames (left and right)
        sword_attack_left_raw = [
            pygame.image.load(f"assets/player/sword/sword-left/attack-left/sword-attack-left{i}.png")
            for i in range(1, 10)  # 9 attack frames
        ]
        sword_attack_right_raw = [
            pygame.image.load(f"assets/player/sword/sword-right/attack-right/sword-attack-right{i}.png")
            for i in range(1, 10)  # 9 attack frames
        ]

        # Scale sword attack frames
        self.sword_attack_left = [
            pygame.transform.scale(frame, (int(frame.get_width() * scale_factor), int(frame.get_height() * scale_factor)))
            for frame in sword_attack_left_raw
        ]
        self.sword_attack_right = [
            pygame.transform.scale(frame, (int(frame.get_width() * scale_factor), int(frame.get_height() * scale_factor)))
            for frame in sword_attack_right_raw
        ]

        self.frame_counter = 0
        self.frame_speed = 5
        self.attack_frame_speed = 2  # Faster animation for attacks
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

        # Set initial image to first sword idle right frame BEFORE creating rect
        # Player starts with sword equipped visually (even if no weapon assigned)
        self.image = self.sword_idle_right[0]
        
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
                self.misc_inventory["ammo"] = self.weapon_equipped.reload(self.misc_inventory["ammo"])
        if keys[pygame.K_1]:
            if self.weapons_inventory["gun"] is not None:
                self.equip_weapon(self.weapons_inventory["gun"])
        if keys[pygame.K_2]:
            if self.weapons_inventory["melee"] is not None:
                self.equip_weapon(self.weapons_inventory["melee"])
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
        if self.weapon_equipped and self.weapon_equipped.weapon_type == "gun":
            return self.blaster_idle_left if self.cursor_side == "left" else self.blaster_idle_right
        else:
            # Default to sword (melee)
            return self.sword_idle_left if self.cursor_side == "left" else self.sword_idle_right

    def get_walk_frames(self):
        """Get walk frame set based on equipped weapon and cursor side."""
        if self.weapon_equipped and self.weapon_equipped.weapon_type == "gun":
            return self.blaster_move_left if self.cursor_side == "left" else self.blaster_move_right
        else:
            # Default to sword (melee)
            return self.sword_walk_left if self.cursor_side == "left" else self.sword_walk_right


    def update(self):
        self.handle_input()  # Handle player input to update velocity
        super().update()  # Call the base class update to move the player
        
        # Keep collision rect synced with player position
        self.collision_rect.center = self.rect.center

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

        # Handle attack animation
        if self.is_attacking and self.weapon_equipped and self.weapon_equipped.weapon_type == "melee":
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
                    if self.weapon_equipped and self.weapon_equipped.weapon_type == "melee":
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
    
    def calculate_angle_to_mouse(self, mouse_pos):
        import math
        dx = mouse_pos[0] - self.rect.centerx
        dy = mouse_pos[1] - self.rect.centery
        return math.atan2(dy, dx)
        

    def equip_weapon(self, weapon):
        if weapon.weapon_type in self.weapons_inventory:
            self.weapon_equipped = weapon
            # Position the weapon immediately if it has update_position method
            if hasattr(weapon, 'update_position'):
                mouse_pos = pygame.mouse.get_pos()
                # Pass the player's center explicitly
                weapon.update_position((self.rect.centerx, self.rect.centery), mouse_pos)

    def use_weapon(self):
        if self.weapon_equipped:
            attack_succeeded = self.weapon_equipped.attack(self.rect.center, self.direction)
            # Trigger attack animation for melee weapons ONLY if attack succeeded
            if attack_succeeded and self.weapon_equipped.weapon_type == "melee":
                self.is_attacking = True
                self.weapon_equipped.is_attacking = True  # Sync weapon state
                self.attack_start_time = pygame.time.get_ticks()
                self.attack_frame_index = 0
        else:
            print("No weapon equipped")