"""Utilities for sprite collision and bounds calculations."""

import pygame


def get_sprite_bounds(surface):
    """
    Get the bounding rect of non-transparent pixels in a surface.
    Returns a rect with the actual visible sprite bounds (crops transparent padding).
    
    Args:
        surface: pygame.Surface to analyze
        
    Returns:
        pygame.Rect with x, y, width, height of non-transparent content
    """
    mask = pygame.mask.from_surface(surface)
    rect = mask.get_bounding_rects()
    
    if not rect:
        # If no non-transparent pixels found, return full surface rect
        return surface.get_rect()
    
    # Return the first (and typically only) bounding rect
    return rect[0]
