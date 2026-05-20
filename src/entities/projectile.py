import pygame
from src.entities.base_entity import BaseEntity
from src.utils.sprite_utils import get_sprite_bounds

class Projectile(BaseEntity):

    def __init__(self, x, y, velocity_x, velocity_y, damage, color=(255, 255, 0), sprite_image=None):
        super().__init__(x, y, color, max_health=None)

        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.damage = damage
        # Override the image and rect for the projectile (won't be necesary once sprites are designed)
        if sprite_image:
            self.image = sprite_image
        else:
            self.image = pygame.Surface((10, 10))
            self.image.fill(color)
        
        # Create collision rect from actual sprite bounds (crop transparent padding)
        bounds = get_sprite_bounds(self.image)
        self.collision_rect = pygame.Rect(0, 0, bounds.width, bounds.height)
        self.collision_rect.center = (int(x), int(y))
        
        # Display rect centered on position
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        # Move the projectile in the specified direction
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.rect.center = (int(self.x), int(self.y))
        # Keep collision rect synced with position
        self.collision_rect.center = (int(self.x), int(self.y))

        #remove projectile if it goes off screen
        if (self.rect.right < 0 or self.rect.left > pygame.display.get_surface().get_width() or
            self.rect.bottom < 0 or self.rect.top > pygame.display.get_surface().get_height()):
            self.kill()