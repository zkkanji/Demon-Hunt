import pygame
from pygame.sprite import Sprite

class BaseEntity(Sprite):

    def __init__(self, x, y, width, height, color=(255, 0, 0), health=None):
        super().__init__()
        self.health = health
        # visual representation of the entity
        self.image = pygame.Surface((width, height))
        self.image.fill(color)  # Default color (red)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        # movement attributes
        self.x = float(x)
        self.y = float(y)
        self.velocity_x = 0.0
        self.velocity_y = 0.0
    
    def update(self):
        # Update the entity's position based on its velocity
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.rect.topleft = (int(self.x), int(self.y))

    def draw(self, surface):
        surface.blit(self.image, self.rect)