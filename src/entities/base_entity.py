import pygame
from pygame.sprite import Sprite

class BaseEntity(Sprite):

    def __init__(self, x, y, max_health=None):
        super().__init__()
        self.max_health = max_health
        self.current_health = max_health
        # visual representation of the entity
        self.image = pygame.Surface((50, 50))
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

        surface = pygame.display.get_surface()
        screen_w, screen_h = surface.get_width(), surface.get_height()

        #entity border control
        if self.rect.left < 0:
            self.rect.left = 0
            self.x = self.rect.centerx
        if self.rect.right > screen_w:
            self.rect.right = screen_w
            self.x = self.rect.centerx
        if self.rect.top < 0:
            self.rect.top = 0
            self.y = self.rect.centery
        if self.rect.bottom > screen_h:
            self.rect.bottom = screen_h
            self.y = self.rect.centery

    def draw(self, surface):
        surface.blit(self.image, self.rect)