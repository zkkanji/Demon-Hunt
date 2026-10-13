import pygame
from src.entities.base_entity import BaseEntity
from src.utils.sprite_utils import get_sprite_bounds

class Projectile(BaseEntity):

    def __init__(self, x, y, velocity_x, velocity_y, damage, sprite_image=None, is_critical=False):
        super().__init__(x, y, max_health=None)

        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.damage = damage
        self.is_critical = is_critical
        self.destroy_on_hit = True
        self.hit_entities = set()
        # Override the image and rect for the projectile (won't be necesary once sprites are designed)
        if sprite_image:
            self.image = sprite_image
        else:
            self.image = pygame.Surface((10, 10))
        self.original_image = self.image
        
        # Create collision rect from actual sprite bounds (crop transparent padding)
        bounds = get_sprite_bounds(self.image)
        self.collision_rect = pygame.Rect(0, 0, bounds.width, bounds.height)
        self.collision_rect.center = (int(x), int(y))
        
        # Display rect centered on position
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        # Move the projectile in the specified direction
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.rect.center = (int(self.x), int(self.y))
        # Keep collision rect synced with position
        self.collision_rect.center = (int(self.x), int(self.y))

        #remove projectile if it goes off screen
        if (self.rect.right < 0 or self.rect.left > pygame.display.get_surface().get_width() or
            self.rect.bottom < 0 or self.rect.top > pygame.display.get_surface().get_height()):
            self.kill()


class AnimatedProjectile(Projectile):

    def __init__(self, x, y, velocity_x, velocity_y, damage, frames, sequence, frame_speed=4):
        super().__init__(x, y, velocity_x, velocity_y, damage, sprite_image=frames[0])
        self.frames = frames
        self.frame_speed = frame_speed
        self.frame_counter = 0
        # Pingpong sequence: e.g. [0,1,2,1] for 3 frames
        self.sequence = sequence
        self.seq_index = 0

    def update(self):
        super().update()
        self.frame_counter += 1
        if self.frame_counter >= self.frame_speed:
            self.frame_counter = 0
            self.seq_index = (self.seq_index + 1) % len(self.sequence)
            self.image = self.frames[self.sequence[self.seq_index]]

class BoomerangProjectile(Projectile):

    def __init__(
        self,
        x,
        y,
        velocity_x,
        velocity_y,
        damage,
        player,
        max_distance,
        sprite_image=None,
        is_critical=False,
    ):
        super().__init__(
            x,
            y,
            velocity_x,
            velocity_y,
            damage,
            sprite_image=sprite_image,
            is_critical=is_critical,
        )
        self.player = player
        self.max_distance = max_distance
        self.launch_position = pygame.Vector2(x, y)
        self.speed = pygame.Vector2(velocity_x, velocity_y).length()
        self.returning = False
        self.rotation = 0
        self.rotation_speed = 24
        self.destroy_on_hit = False

    def _sync_position(self):
        self.rect = self.image.get_rect(center=(int(self.x), int(self.y)))
        self.collision_rect.center = self.rect.center

    def update(self):
        if not self.alive():
            return

        if not self.returning:
            movement = pygame.Vector2(self.velocity_x, self.velocity_y)
            next_position = pygame.Vector2(self.x, self.y) + movement
            distance = next_position.distance_to(self.launch_position)
            if distance >= self.max_distance:
                outward_direction = movement.normalize()
                next_position = self.launch_position + outward_direction * self.max_distance
                self.returning = True
            self.x, self.y = next_position
        else:
            to_player = pygame.Vector2(self.player.rect.center) - pygame.Vector2(self.x, self.y)
            distance = to_player.length()
            if distance <= self.speed:
                self.x, self.y = self.player.rect.center
                self._sync_position()
                self.kill()
                return
            direction = to_player.normalize()
            self.velocity_x = direction.x * self.speed
            self.velocity_y = direction.y * self.speed
            self.x += self.velocity_x
            self.y += self.velocity_y

        self.rotation = (self.rotation + self.rotation_speed) % 360
        self.image = pygame.transform.rotate(self.original_image, self.rotation)
        self._sync_position()