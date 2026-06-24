import pygame
#from . import power_ups as pup
from src.constants import WIDTH, UI_COLOR

class card:
    
    def __init__(self, text, image_folder):
        self.text = text
        image_scale = 8
        image_idle = pygame.image.load(f"{image_folder}/card.png")
        image_hover = pygame.image.load(f"{image_folder}/card-hover.png")
        self.images = (pygame.transform.scale(image_idle, (image_idle.get_width() * image_scale, image_idle.get_height() * image_scale)), 
                       pygame.transform.scale(image_hover, (image_hover.get_width() * image_scale, image_hover.get_height() * image_scale)))
        animation_frames_raw = [
            pygame.image.load(f"assets/upgrade-cards/card-animation/f{i}.png")
            for i in range(1, 9)
        ]
        self.animation_frames = [
            pygame.transform.scale(image, (image.get_width() * image_scale, image.get_height() * image_scale))
            for image in animation_frames_raw
        ]
        self.rect = self.images[0].get_rect()
        # Create a tighter collision rect to avoid overlapping card detection
        self.collision_rect = self.rect.inflate(-self.rect.width * 0.5, -self.rect.height * 0.3)
        self.animation_index = 0
        self.animation_tick = 0
        self.is_hovering = False
        self.ticks_per_frame = 3
        self.card_type = None

        # Description text setup
        self.font_letters = pygame.font.Font(f"assets/fonts/minecraftia/Minecraftia.ttf", 24)
        #self.font_letters.set_bold(True)
        self.desc = self.font_letters.render(self.text, True, UI_COLOR)
        self.center_distance = self.desc.get_rect().width // 2
        self.desc_coords = ((WIDTH // 2) - self.center_distance, self.rect.bottom + 140)

    def update(self, mouse_pos):
        # Update collision rect position to match rect
        self.collision_rect.center = self.rect.center
        # Check if hovering over the card using collision rect
        self.is_hovering = self.collision_rect.collidepoint(mouse_pos)
        
        # Handle animation playback
        if self.animation_index < len(self.animation_frames):
            # Still animating
            self.animation_tick += 1
            if self.animation_tick >= self.ticks_per_frame:
                self.animation_tick = 0
                self.animation_index += 1
        
        # Return appropriate image
        if self.animation_index < len(self.animation_frames):
            # Still in animation phase
            return self.animation_frames[self.animation_index]
        else:
            # Animation complete, use idle/hover images
            if self.is_hovering:
                image_index = 1  
            else:
                image_index = 0  
            return self.images[image_index]

# Player attribute upgrade card class
class player_upgrade_card(card):
    def __init__(self, name, upgrade_amount, image_folder, player, attribute_name):
        super().__init__(name, image_folder)
        self.upgrade_amount = upgrade_amount
        self.player = player
        self.attribute_name = attribute_name
        self.effecting_attribute_value = getattr(player, attribute_name)
        self.card_type = "upgrade"

    def apply_upgrade(self):
        self.effecting_attribute_value = getattr(self.player, self.attribute_name)
        setattr(self.player, self.attribute_name, self.effecting_attribute_value + self.upgrade_amount)
        self.effecting_attribute_value = getattr(self.player, self.attribute_name)
        if self.attribute_name == "max_health":
            self.player.current_health += self.upgrade_amount  

# Weapon attribute upgrade card class
class weapon_upgrade_card(card): 

    def __init__(self, name, upgrade_amount, image_folder, weapon, attribute_name):
        super().__init__(name, image_folder)
        self.upgrade_amount = upgrade_amount
        self.weapon = weapon
        self.attribute_name = attribute_name
        self.effecting_attribute_value = getattr(weapon, attribute_name, None)
        self.card_type = "upgrade"

    def apply_upgrade(self):
        self.effecting_attribute_value = getattr(self.weapon, self.attribute_name)
        setattr(self.weapon, self.attribute_name, self.effecting_attribute_value + self.upgrade_amount)
        self.effecting_attribute_value = getattr(self.weapon, self.attribute_name)

    def update_weapon(self, weapon):
        self.weapon = weapon

# Weapon unlocking card class
class weapon_unlock_card(card):
    def __init__(self, name, player, weapon_to_unlock, image_folder):
        super().__init__(name, image_folder)
        self.player = player
        self.weapon_to_unlock = weapon_to_unlock
        self.card_type = "weapon_unlock"
    
    def unlock_weapon(self):
        if self.weapon_to_unlock not in self.player.gun_inventory and self.weapon_to_unlock not in self.player.melee_inventory:
            if self.weapon_to_unlock.weapon_type == "gun":
                self.player.gun_inventory.append(self.weapon_to_unlock)
            elif self.weapon_to_unlock.weapon_type == "melee":
                self.player.melee_inventory.append(self.weapon_to_unlock)

class power_up_card(card):
    def __init__(self, player, power_up, image_folder):
        super().__init__(power_up.text, image_folder)
        self.player = player
        self.power_up = power_up
        self.card_type = "power_up"

    def unlock_powerup(self):
        self.player.power_up = self.power_up