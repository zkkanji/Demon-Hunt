from functools import lru_cache

import pygame


@lru_cache(maxsize=None)
def load_image(path):
    """Load and cache an image in the display's native pixel format."""
    image = pygame.image.load(path)
    if pygame.display.get_init() and pygame.display.get_surface() is not None and image.get_alpha() is not None:
        return image.convert_alpha()
    if pygame.display.get_init() and pygame.display.get_surface() is not None:
        return image.convert()
    return image


@lru_cache(maxsize=None)
def scale_image(path, width, height):
    return pygame.transform.scale(load_image(path), (width, height))


@lru_cache(maxsize=None)
def scale_surface(image, width, height):
    """Cache scaling for a surface that was loaded through load_image."""
    return pygame.transform.scale(image, (width, height))
