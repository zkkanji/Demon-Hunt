import pygame
from pygame.sprite import Sprite
from src.utils.sprite_utils import make_shadow

class DamageNumber:
    def __init__(self, pos, amount, is_critical=False):
        self.x, self.y = pos
        self.amount = amount
        self.is_critical = is_critical
        self.fonts = [pygame.font.Font(f"assets/fonts/smallest-pixel-7/smallest_pixel-7.ttf", i)
            for i in range(2, 25, 2)
        ]
        self.regular_text = self.fonts[0].render(str(self.amount), True, (227, 229, 82))
        self.crit_text = self.fonts[0].render(str(self.amount), True, (251, 50, 50))    
        self.text = self.crit_text if self.is_critical else self.regular_text
        self.spawn_time = pygame.time.get_ticks()  # Record when the damage number was created
        self.lifetime = 600  #ms
        self.font_iterator = 0

    def is_expired(self):
        return pygame.time.get_ticks() - self.spawn_time > self.lifetime

    def update(self):
        if self.font_iterator < len(self.fonts):
            self.y -= 0.8
            text_color = (251, 50, 50) if self.is_critical else (227, 229, 82)
            self.text = self.fonts[self.font_iterator].render(str(self.amount), True, text_color)
            self.font_iterator += 1

    def draw(self, screen):
        screen.blit(self.text, (self.x, self.y))

class EnemyDrops(Sprite):
    def __init__(self, pos, amount, player, player_attribute):
        super().__init__()
        self.x, self.y = pos
        self.amount = amount
        self.player = player
        self.player_attribute = player_attribute
        image_scale = 0
        raw_image = None
        if self.player_attribute == "ammo":
            image_scale = 1.3
            raw_image = pygame.image.load(f"assets/misc/drops/ammo.png").convert_alpha()
        elif self.player_attribute == "current_health":
            image_scale = 1.5
            raw_image = pygame.image.load(f"assets/misc/drops/health.png").convert_alpha()
        self.image = pygame.transform.scale(raw_image, (raw_image.get_width() * image_scale, raw_image.get_height() * image_scale))   
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.lifetime = 125000 #ms
        self.spawn_time = pygame.time.get_ticks()
        self.effecting_attribute = getattr(self.player, self.player_attribute)
        shadow_image_raw = pygame.image.load("assets/misc/entity-shadow.png").convert_alpha()
        self.shadow = make_shadow(shadow_image_raw, self.rect.width)
        self.base_y = float(self.y)
        self.hover_offset = 0.0
        self.hover_direction = 1
        self.is_collected = False
    
    def collect(self):
        self.effecting_attribute = getattr(self.player, self.player_attribute)
        if self.player_attribute == "current_health":
            new_val = min(self.effecting_attribute + self.amount, self.player.max_health)
            setattr(self.player, self.player_attribute, new_val)
        else:
            setattr(self.player, self.player_attribute, self.effecting_attribute + self.amount)
        self.effecting_attribute = getattr(self.player, self.player_attribute)
        self.is_collected = True  

    def is_expired(self):
        return pygame.time.get_ticks() - self.spawn_time > self.lifetime

    def update(self):
        if self.is_expired() or self.is_collected:
            self.kill()  # Remove from all groups
        self.hover_offset += 0.3 * self.hover_direction
        if abs(self.hover_offset) >= 10:
            self.hover_direction *= -1
        self.rect.centery = int(self.base_y + self.hover_offset)

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

