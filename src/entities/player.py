import pygame
from .base_entity import BaseEntity

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
        # Load and scale walk frames
        walk_frames_raw = [
            pygame.image.load("assets/player/movement/player-move1.png"),
            pygame.image.load("assets/player/movement/player-move2.png"),
            pygame.image.load("assets/player/movement/player-move3.png"),
            pygame.image.load("assets/player/movement/player-move4.png"),
            pygame.image.load("assets/player/movement/player-move5.png"),
        ]
        
        # Load and scale idle frames
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

        self.current_frame = 0
        self.frame_counter = 0
        self.frame_speed = 5
        self.is_moving = False

        # Animation sequences
        self.idle_sequence = [0, 1, 2, 3, 4, 3, 2, 1]  # Breathe effect: 1-5 then 5-1
        self.walk_sequence = [0, 1, 2, 1, 0, 3, 4, 3, 0]  # Custom walk pattern
        self.idle_frame_index = 0
        self.walk_frame_index = 0

        self.current_frames = self.idle_frames
        self.image = self.current_frames[self.current_frame]
        self.rect = self.image.get_rect(center=(x, y))
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

        # Update blaster position if equipped
        if self.weapon_equipped and hasattr(self.weapon_equipped, 'update_position'):
            mouse_pos = pygame.mouse.get_pos()
            self.weapon_equipped.update_position(self.rect.center, mouse_pos)

        # Update animation based on movement state
        self.frame_counter += 1
        if self.frame_counter >= self.frame_speed:
            self.frame_counter = 0
            
            if self.is_moving:
                # Use walk sequence
                self.walk_frame_index = (self.walk_frame_index + 1) % len(self.walk_sequence)
                frame_to_show = self.walk_sequence[self.walk_frame_index]
                self.image = self.walk_frames[frame_to_show]
            else:
                # Use idle sequence
                self.idle_frame_index = (self.idle_frame_index + 1) % len(self.idle_sequence)
                frame_to_show = self.idle_sequence[self.idle_frame_index]
                self.image = self.idle_frames[frame_to_show]
        

    def equip_weapon(self, weapon):
        if weapon.weapon_type in self.weapons_inventory:
            self.weapon_equipped = weapon

    def use_weapon(self):
        if self.weapon_equipped:
            self.weapon_equipped.attack(self.rect.center, self.direction)
        else:
            print("No weapon equipped")