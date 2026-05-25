import pygame
from src.utils.sprite_utils import get_sprite_bounds

class ProgressBar:
    def __init__ (self, x, y, max_value, sprite_path, sprite_scalex, sprite_scaley, xmargin=2, ymargin=2, fill_color=(255, 0, 0)):
        self.x = x
        self.y = y
        self.max_value = max_value
        self.current_value = max_value
        sprite_bar = pygame.image.load(sprite_path)
        self.sprite_container = pygame.transform.scale(sprite_bar, (int(sprite_bar.get_width() * sprite_scalex), int(sprite_bar.get_height() * sprite_scaley)))
        self.fill_color = fill_color
        
        # Store full sprite container dimensions for positioning/centering
        self.container_width = self.sprite_container.get_width()
        self.container_height = self.sprite_container.get_height()
        
        # Get actual sprite bounds without padding
        bounds = get_sprite_bounds(self.sprite_container)
        self.bar_width = bounds.width
        self.bar_height = bounds.height
        self.bounds_offset_x = bounds.x
        self.bounds_offset_y = bounds.y
        
        # Margin inside the bar (pixels from edge)
        self.fill_marginx = xmargin
        self.fill_marginy = ymargin

    def update(self, current_value):
        self.current_value = max(0, min(current_value, self.max_value))

    def draw(self, surface):
        surface.blit(self.sprite_container, (self.x, self.y))
        ratio = self.current_value / self.max_value
        # Reduce width by x margin on both sides
        available_width = self.bar_width - (self.fill_marginx * 2)
        fill_width = int(available_width * ratio)
        if fill_width > 0:
            # Start at bounds offset + margins, with x/y margins applied
            fill_rect = pygame.Rect(
                self.x + self.bounds_offset_x + self.fill_marginx,
                self.y + self.bounds_offset_y + self.fill_marginy,
                fill_width,
                self.bar_height - (self.fill_marginy * 2)
            )
            pygame.draw.rect(surface, self.fill_color, fill_rect)
