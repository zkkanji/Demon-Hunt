import pygame
import sys
from src.constants import WIDTH, HEIGHT, FPS, BG_COLOR
from src.entities.player import Player
from src.weapons.blaster import Blaster   

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("First Zain Game")

clock = pygame.time.Clock()

player = Player(WIDTH // 2, HEIGHT // 2)
blaster = Blaster()
player.weapons_inventory["gun"] = blaster  # Add the blaster to the player's inventory
player.equip_weapon(player.weapons_inventory["gun"])  # Equip the blaster as the current weapon

all_sprites = pygame.sprite.Group(player)

font = pygame.font.Font(None, 24)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BG_COLOR)  # Clear the screen with a green color

    # Here you can add your game logic and drawing code

    ammo_text = font.render(f"Ammo: {blaster.ammo}/{player.misc_inventory['ammo']}", True, (255, 255, 255))
    curr_equipped_text = font.render(f"Equipped: {player.weapon_equipped.name if player.weapon_equipped else 'None'}", True, (255, 255, 255))
    player_health_text = font.render(f"Health: {player.health}", True, (255, 255, 255))
    all_sprites.update()  # Update all sprites
    player.weapons_inventory["gun"].update()  # Update the blaster (which updates its projectiles)

    all_sprites.draw(screen)  # Draw all sprites
    player.weapons_inventory["gun"].projectiles.draw(screen)  # Draw all active projectiles
    screen.blit(player.weapon_equipped.image, player.weapon_equipped.rect)  # Draw the blaster
    screen.blit(ammo_text, (10, 10))  # Display ammo count
    screen.blit(curr_equipped_text, (10, 40))  # Display currently equipped weapon
    screen.blit(player_health_text, (10, 70))  # Display player health
    pygame.display.flip()  # Update the display
    clock.tick(FPS)  # Maintain the frame rate
    
pygame.quit()
sys.exit()