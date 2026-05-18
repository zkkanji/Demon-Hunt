import pygame
import sys
from src.constants import WIDTH, HEIGHT, FPS, BG_COLOR
from src.entities.player import Player
from src.weapons.blaster import Blaster   
from src.weapons.sword import Sword
from src.entities.enemy1 import Enemy1
from src.game import check_projectile_collision

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("First Zain Game")

clock = pygame.time.Clock()

player = Player(WIDTH // 2, HEIGHT // 2)
blaster = Blaster()
sword = Sword()
player.weapons_inventory["gun"] = blaster  # Add the blaster to the player's inventory
player.weapons_inventory["melee"] = sword  # Add the sword to the player's inventory
player.equip_weapon(player.weapons_inventory["gun"])  # Equip the blaster as the current weapon

# Load reticles for custom cursor
gun_reticle = pygame.image.load("assets/misc/gun-reticle.png")
melee_reticle = pygame.image.load("assets/misc/melee-reticle.png")

# Hide the default pygame cursor
pygame.mouse.set_visible(False)

all_sprites = pygame.sprite.Group(player)
enemies = pygame.sprite.Group()
enemy1 = Enemy1(400, 300)
enemies.add(enemy1)

font = pygame.font.Font(None, 24)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BG_COLOR)  # Clear the screen with a green color

    #UI Text
    ammo_text = font.render(f"Ammo: {blaster.ammo}/{player.misc_inventory['ammo']}", True, (255, 255, 255))
    curr_equipped_text = font.render(f"Equipped: {player.weapon_equipped.name if player.weapon_equipped else 'None'}", True, (255, 255, 255))
    player_health_text = font.render(f"Health: {player.health}", True, (255, 255, 255))

    all_sprites.update()  # Update all sprites
    player.weapons_inventory["gun"].update()  # Update the blaster (which updates its projectiles)
    player.weapons_inventory["melee"].update()  # Update the sword (which updates its attack animation)
    enemies.update()

    # Collision detection
    check_projectile_collision(blaster.projectiles, enemies)
    # Sword sweep collision will be handled here once SweepProjectile is created
    check_projectile_collision(sword.sweeps, enemies)

    all_sprites.draw(screen)  # Draw all sprites
    enemies.draw(screen)
    player.weapons_inventory["gun"].projectiles.draw(screen)  # Draw all gun projectiles
    player.weapons_inventory["melee"].sweeps.draw(screen)  # Draw all sword sweep projectiles
    
    # DEBUG: Draw hitboxes
    # Draw player collision rect (blue)
    player_collision_rect = getattr(player, 'collision_rect', player.rect)
    pygame.draw.rect(screen, (100, 149, 237), player_collision_rect, 2)
    
    # Draw bullet projectile hitboxes (yellow) - use collision_rect if available
    for projectile in blaster.projectiles:
        collision_rect = getattr(projectile, 'collision_rect', projectile.rect)
        pygame.draw.rect(screen, (255, 255, 0), collision_rect, 2)
    
    # Draw sword sweep hitboxes (green) - use collision_rect if available
    for sweep in player.weapons_inventory["melee"].sweeps:
        collision_rect = getattr(sweep, 'collision_rect', sweep.rect)
        pygame.draw.rect(screen, (0, 255, 0), collision_rect, 2)
    
    # Draw enemy hitboxes (red) - use collision_rect if available
    for enemy in enemies:
        collision_rect = getattr(enemy, 'collision_rect', enemy.rect)
        pygame.draw.rect(screen, (255, 0, 0), collision_rect, 2)
    
    # Draw gun if equipped (sword is part of player sprite)
    if player.weapon_equipped.weapon_type == "gun":
        screen.blit(player.weapon_equipped.image, player.weapon_equipped.rect)
    
    # Draw UI text
    if player.weapon_equipped.weapon_type == "gun":
        screen.blit(ammo_text, (10, 10))  # Display ammo count
    screen.blit(curr_equipped_text, (10, 40))  # Display currently equipped weapon
    screen.blit(player_health_text, (10, 70))  # Display player health
    
    # Draw custom reticle at mouse position
    mouse_pos = pygame.mouse.get_pos()
    if player.weapon_equipped.weapon_type == "gun":
        reticle_rect = gun_reticle.get_rect(center=mouse_pos)
        screen.blit(gun_reticle, reticle_rect)
    elif player.weapon_equipped.weapon_type == "melee":
        reticle_rect = melee_reticle.get_rect(center=mouse_pos)
        screen.blit(melee_reticle, reticle_rect)
    
    pygame.display.flip()  # Update the display
    clock.tick(FPS)  # Maintain the frame rate
    
pygame.quit()
sys.exit()