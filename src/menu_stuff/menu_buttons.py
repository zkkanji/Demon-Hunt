import pygame

class MenuButton:

    def __init__(self, image_path, x, y, action, scale=3):
        self.idle_image_raw = pygame.image.load(f"assets/menu/buttons/{image_path}1.png").convert_alpha()
        self.hover_image_raw = pygame.image.load(f"assets/menu/buttons/{image_path}2.png").convert_alpha()
        self.action = action
        self.is_hovered = False
        self.scale = scale
        self.rect = pygame.Rect(x, y, 0, 0)
        self._scale_images()
        self.set_position(x, y)

    def _scale_images(self):
        size = (
            int(self.idle_image_raw.get_width() * self.scale),
            int(self.idle_image_raw.get_height() * self.scale),
        )
        hover_size = (
            int(self.hover_image_raw.get_width() * self.scale),
            int(self.hover_image_raw.get_height() * self.scale),
        )
        self.idle_image = pygame.transform.scale(self.idle_image_raw, size)
        self.hover_image = pygame.transform.scale(self.hover_image_raw, hover_size)
        self.image = self.hover_image if self.is_hovered else self.idle_image

    def set_position(self, x, y):
        self.rect = self.image.get_rect(topleft=(x, y))
        visible_bounds = self.idle_image.get_bounding_rect()
        self.click_rect = visible_bounds.move(self.rect.topleft)

    def set_scale(self, scale):
        self.scale = scale
        top_left = self.rect.topleft
        self._scale_images()
        self.set_position(*top_left)

    def set_geometry(self, x, y, scale=None):
        if scale is not None:
            self.scale = scale
            self._scale_images()
        self.set_position(x, y)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def update(self, mouse_pos):
        if self.is_hovering(mouse_pos):
            self.image = self.hover_image
            self.is_hovered = True
        else:
            self.image = self.idle_image
            self.is_hovered = False

    def is_hovering(self, mouse_pos):
        return self.click_rect.collidepoint(mouse_pos)

    def clicked(self, mouse_pos):
        if self.click_rect.collidepoint(mouse_pos):
            return self.action
        return None