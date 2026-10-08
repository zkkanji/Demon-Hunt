import pygame
import random
from src.utils.sprite_utils import get_sprite_bounds, make_shadow

class RockLandscaping:

    class Rock:
        def __init__(self, image, x, y):
            self.image = image
            self.x = x
            self.y = y
            self.image_rect = self.image.get_rect(topleft=(x, y))
            bounds = get_sprite_bounds(self.image)
            self.rect = bounds.move(self.image_rect.topleft)
            self.shadow_image_raw = pygame.image.load("assets/misc/entity-shadow.png").convert_alpha()
            self.shadow = make_shadow(self.shadow_image_raw, self.image.get_width())
            self.shadow.set_alpha(70)  

        def draw(self, surface):
            shadow_rect = self.shadow.get_rect(
                midbottom=(self.rect.centerx, self.rect.bottom + 17)
            )
            surface.blit(self.shadow, shadow_rect)
            surface.blit(self.image, self.image_rect)
            
    def __init__(self, screen, rock_scale, avoid_rect=None):
        self.screen = screen
        display_info = pygame.display.Info()
        self.terrain_width = max(screen.get_width(), display_info.current_w)
        self.terrain_height = max(screen.get_height(), display_info.current_h)
        self.rock_images_raw = [
            pygame.image.load(f"assets/landscaping/rocks/rock{i}.png").convert_alpha()
            for i in range(1, 7)
        ]
        self.rock_images = [
            pygame.transform.scale(
                img,
                (int(img.get_width() * rock_scale), int(img.get_height() * rock_scale)),
            )
            for img in self.rock_images_raw
        ]
        self.rocks = []
        self.rock_distance = 150
        self.avoid_rect = avoid_rect

    def generate_rocks(self):
        """Create a new non-overlapping set of rocks for the maximum terrain size."""
        self.rocks.clear()
        if self.terrain_width <= 0 or self.terrain_height <= 0:
            return

        target_count = max(
            1,
            int((self.terrain_width * self.terrain_height) / (self.rock_distance ** 2) * 0.55),
        )
        max_attempts = target_count * 40
        attempts = 0

        while len(self.rocks) < target_count and attempts < max_attempts:
            attempts += 1
            image = random.choice(self.rock_images)
            max_x = max(0, self.terrain_width - image.get_width())
            max_y = max(0, self.terrain_height - image.get_height())
            x = random.randint(0, max_x)
            y = random.randint(0, max_y)
            candidate = image.get_rect(topleft=(x, y))

            if self.avoid_rect and candidate.colliderect(self.avoid_rect):
                continue
            if any(
                candidate.inflate(self.rock_distance, self.rock_distance).colliderect(rock.rect)
                for rock in self.rocks
            ):
                continue

            self.place_rocks(image, x, y)

    def place_rocks(self, image, x, y):
        self.rocks.append(self.Rock(image, x, y))


    def draw(self):
        for rock in self.rocks:
            rock.draw(self.screen)
