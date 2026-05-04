import pygame
from pygame.sprite import Sprite

class BaseEntity(Sprite):

    def __init__(self, x, y, color=(255, 0, 0), health=None):
        super().__init__()
        self.health = health
        # visual representation of the entity
        self.image = pygame.Surface((50, 50))
        self.image.fill(color)  # Default color (red)
        self.rect = self.image.get_rect()

        # movement attributes
        self.x = float(x)
        self.y = float(y)
        self.velocity_x = 0.0
        self.velocity_y = 0.0
    
    def update(self):
        # Update the entity's position based on its velocity
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.rect.center = (int(self.x), int(self.y))  # Update the rect position for rendering and collision

    def draw(self, surface):
        surface.blit(self.image, self.rect)