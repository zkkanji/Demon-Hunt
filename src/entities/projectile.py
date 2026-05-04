import pygame
from src.entities.base_entity import BaseEntity

class Projectile(BaseEntity):

    def __init__(self, x, y, velocity_x, velocity_y, damage, color=(255, 255, 0)):
        super().__init__(x, y, color, health=None)

        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.damage = damage
        # Override the image and rect for the projectile (won't be necesary once sprites are designed)
        self.image = pygame.Surface((10, 10))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        # Move the projectile in the specified direction
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.rect.center = (int(self.x), int(self.y))  

        #remove projectile if it goes off screen
        if (self.rect.right < 0 or self.rect.left > pygame.display.get_surface().get_width() or
            self.rect.bottom < 0 or self.rect.top > pygame.display.get_surface().get_height()):
            self.kill()