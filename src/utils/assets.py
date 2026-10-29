from functools import lru_cache

import pygame


class LazyFrames:
    """Load and cache an animation frame list on its first access."""

    def __init__(self, loader):
        self._loader = loader
        self._frames = None

    def _get_frames(self):
        if self._frames is None:
            self._frames = self._loader()
        return self._frames

    def __getitem__(self, index):
        return self._get_frames()[index]

    def __len__(self):
        return len(self._get_frames())

    def __iter__(self):
        return iter(self._get_frames())


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


def load_scaled_frames(path_template, frame_numbers, scale):
    frames = []
    for frame_number in frame_numbers:
        image = load_image(path_template.format(i=frame_number))
        frames.append(
            scale_surface(
                image,
                int(image.get_width() * scale),
                int(image.get_height() * scale),
            )
        )
    return frames


def lazy_scaled_frames(path_template, frame_numbers, scale):
    return LazyFrames(
        lambda: load_scaled_frames(path_template, frame_numbers, scale)
    )
