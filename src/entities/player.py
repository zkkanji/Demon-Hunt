import pygame
from .base_entity import BaseEntity

class Player(BaseEntity):

    def __init__(self, x, y, width=50, height=50, color=(0, 0, 255), direction=None):
        super().__init__(x, y, width, height, color)

        self.direction = direction  # Track the player's facing direction
        self.weapons_inventory = {
            "gun": None,  # Placeholder for the player's gun
            "melee": None  # Placeholder for the player's melee weapon
        }  
        self.misc_inventory = {
            "ammo" : 50
        }
        self.weapon_equipped = None  # Track which weapon is currently equipped
        self.previous_space_pressed = False

    def handle_input(self):
        keys = pygame.key.get_pressed()
        self.velocity_x = 0
        self.velocity_y = 0

        if keys[pygame.K_a]:
            self.velocity_x = -5
        if keys[pygame.K_d]:
            self.velocity_x = 5
        if keys[pygame.K_w]:
            self.velocity_y = -5
        if keys[pygame.K_s]:
            self.velocity_y = 5
        if self.weapon_equipped and self.weapon_equipped.is_automatic:
            if keys[pygame.K_SPACE]:
                self.use_weapon()
        elif self.weapon_equipped and not self.weapon_equipped.is_automatic:
            if keys[pygame.K_SPACE] and not self.previous_space_pressed:
                self.use_weapon()
            self.previous_space_pressed = keys[pygame.K_SPACE]
        if keys[pygame.K_r]:
            if self.weapon_equipped.weapon_type == "gun":
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

    def equip_weapon(self, weapon):
        if weapon.weapon_type in self.weapons_inventory:
            self.weapon_equipped = weapon

    def use_weapon(self):
        if self.weapon_equipped:
            self.weapon_equipped.attack(self.rect.center, self.direction)
        else:
            print("No weapon equipped")