import pygame 
from .base_entity import BaseEntity
from src.utils.sprite_utils import get_sprite_bounds

class Player(BaseEntity):

    def __init__(self, x, y, color=(0, 0, 255), direction=None, health=100, scale_factor=3):
        super().__init__(x, y, color, health)

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

        #Player Design/Animation frames
        # Load and scale walk frames (unarmed)
        walk_frames_raw = [
            pygame.image.load("assets/player/movement/player-move1.png"),
            pygame.image.load("assets/player/movement/player-move2.png"),
            pygame.image.load("assets/player/movement/player-move3.png"),
            pygame.image.load("assets/player/movement/player-move4.png"),
            pygame.image.load("assets/player/movement/player-move5.png"),
        ]
        
        # Load and scale idle frames (unarmed)
        idle_frames_raw = [
            pygame.image.load("assets/player/idle/player-idle1.png"),
            pygame.image.load("assets/player/idle/player-idle2.png"),
            pygame.image.load("assets/player/idle/player-idle3.png"),
            pygame.image.load("assets/player/idle/player-idle4.png"),
            pygame.image.load("assets/player/idle/player-idle5.png"),
        ]
        
        # Scale frames based on scale_factor
        self.walk_frames = [
            pygame.transform.scale(frame, (int(frame.get_width() * scale_factor), int(frame.get_height() * scale_factor)))
            for frame in walk_frames_raw
        ]
        self.idle_frames = [
            pygame.transform.scale(frame, (int(frame.get_width() * scale_factor), int(frame.get_height() * scale_factor)))
            for frame in idle_frames_raw
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

        # Set initial image to first idle frame BEFORE creating rect
        self.image = self.idle_frames[0]
        
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


    def update(self):
        self.handle_input()  # Handle player input to update velocity
        super().update()  # Call the base class update to move the player
        
        # Keep collision rect synced with player position
        self.collision_rect.center = self.rect.center

        # Update weapon position if equipped (gun only)
        if self.weapon_equipped and hasattr(self.weapon_equipped, 'update_position'):
            mouse_pos = pygame.mouse.get_pos()
            # Pass the player's center explicitly
            self.weapon_equipped.update_position((self.rect.centerx, self.rect.centery), mouse_pos)

        # Update cursor side based on mouse position for sword frames
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
            # Choose frame set based on equipped weapon
            if self.weapon_equipped and self.weapon_equipped.weapon_type == "melee":
                if self.cursor_side == "left":
                    idle_frames = self.sword_idle_left
                    walk_frames = self.sword_walk_left
                else:
                    idle_frames = self.sword_idle_right
                    walk_frames = self.sword_walk_right
            else:
                idle_frames = self.idle_frames
                walk_frames = self.walk_frames

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