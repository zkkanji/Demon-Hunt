import math
import random
import pygame

class Particle(pygame.sprite.Sprite):
    def __init__(self, pos, color):
        super().__init__()
        self.pos = pygame.Vector2(pos)
        angle = random.uniform(0, math.tau)
        speed = random.uniform(1.5, 4.5)

        self.velocity = pygame.Vector2(
            math.cos(angle) * speed,
            math.sin(angle) * speed
        )

        self.color = color
        self.radius = random.randint(4, 8)
        self.lifetime = random.randint(15,28)
        self.age = 0

        self.image = pygame.Surface((1, 1), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=pos)

    def update(self):
        self.age += 1
        self.pos += self.velocity
        self.velocity *= 0.92
        self.velocity.y += 0.12

        if self.age >= self.lifetime:
            self.kill()
            return

        progress = self.age / self.lifetime
        current_radius = max(1, int(self.radius * (1 - progress)))
        alpha = max(0, int(255 * (1 - progress)))

        size = current_radius * 2 + 2
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)

        pygame.draw.circle(
            self.image,
            (*self.color, alpha),
            (size // 2, size // 2),
            current_radius
        )
        self.rect = self.image.get_rect(
            center=(int(self.pos.x), int(self.pos.y))
        )


def create_hit_burst(particle_group, pos, color=(255, 190, 60), count=12):
    for _ in range(count):
        particle_group.add(Particle(pos, color))
