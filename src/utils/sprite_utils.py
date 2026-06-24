import pygame

def make_shadow(raw_image, sprite_width, alpha=100):
    """Scale shadow to match a sprite's width with flat ellipse proportions."""
    shadow_w = int(sprite_width * 0.7)
    shadow_h = int(sprite_width * 0.4)
    shadow = pygame.transform.scale(raw_image, (shadow_w, shadow_h))
    shadow.set_alpha(alpha)
    return shadow

def get_sprite_bounds(surface):
    
    mask = pygame.mask.from_surface(surface)
    rect = mask.get_bounding_rects()
    
    if not rect:
        # If no non-transparent pixels found, return full surface rect
        return surface.get_rect()
    
    # Return the first (and typically only) bounding rect
    return rect[0]
