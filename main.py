import pygame
import sys
from src.constants import WIDTH, HEIGHT, FPS, BG_COLOR
from src.entities.player import Player
from src.weapons.pistol import Pistol   

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("First Zain Game")

clock = pygame.time.Clock()

player = Player(WIDTH // 2, HEIGHT // 2)
pistol = Pistol()
player.equip_weapon(pistol)

all_sprites = pygame.sprite.Group(player)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BG_COLOR)  # Clear the screen with a green color

    # Here you can add your game logic and drawing code
    all_sprites.update()  # Update all sprites
    pistol.update()  # Update the pistol (which updates its projectiles)

    all_sprites.draw(screen)  # Draw all sprites
    pistol.projectiles.draw(screen)  # Draw all active projectiles

    pygame.display.flip()  # Update the display
    clock.tick(FPS)  # Maintain the frame rate
    
pygame.quit()
sys.exit()