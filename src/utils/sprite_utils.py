import pygame

def get_sprite_bounds(surface):
    
    mask = pygame.mask.from_surface(surface)
    rect = mask.get_bounding_rects()
    
    if not rect:
        # If no non-transparent pixels found, return full surface rect
        return surface.get_rect()
    
    # Return the first (and typically only) bounding rect
    return rect[0]
