import pygame
import sys
from src.constants import WIDTH, HEIGHT, FPS, BG_COLOR
from src.entities.player import Player
from src.weapons.blaster import Blaster   
from src.weapons.sword import Sword
from src.entities.devil1 import Devil
import src.game as game
from src.game import check_projectile_collision, check_player_enemy_collision, pause_game, advance_wave, get_enemy_spawn_position, check_enemy_enemy_collision
from src.utils.UImanager import UImanager

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

ui_manager = UImanager(screen, player, blaster)

# Load reticles for custom cursor
gun_reticle = pygame.image.load("assets/misc/gun-reticle.png")
melee_reticle = pygame.image.load("assets/misc/melee-reticle.png")

all_sprites = pygame.sprite.Group(player)
enemies = pygame.sprite.Group()

# Initialize first wave
advance_wave()

# Wave spawning system
enemy_spawn_timer = 0
enemy_spawn_rate = 120  # Spawn an enemy every 120 frames (2 seconds at 60 FPS)
enemies_spawned_this_wave = 0  # Track how many enemies have been spawned this wave

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pause_game()
    if not game.pause_state:        
        screen.fill(BG_COLOR)  # Clear the screen with a green color
        pygame.mouse.set_visible(False)
        
        # Draw shadows on the ground BEFORE drawing characters
        if not player.is_dying:
            shadow_rect = player.shadow.get_rect(midbottom=(player.rect.centerx, player.rect.bottom-5))
            screen.blit(player.shadow, shadow_rect)
        
        for enemy in enemies:
            if enemy.enemy_type == "devil":
                shadow_rect = enemy.shadow.get_rect(midbottom=(enemy.rect.centerx-2, enemy.rect.bottom-2))
            screen.blit(enemy.shadow, shadow_rect)
        
        # Wave spawning system - spawn enemies up to the wave limit
        if enemies_spawned_this_wave < game.max_enemies_current_wave:
            enemy_spawn_timer += 1
            if enemy_spawn_timer >= enemy_spawn_rate and len(enemies) < game.MOST_ENEMIES_ON_SCREEN:
                x, y = get_enemy_spawn_position()
                enemy = Devil(x, y)
                enemies.add(enemy)
                enemies_spawned_this_wave += 1  # Increment spawned counter
                enemy_spawn_timer = 0
        
        # Check if wave is complete (all enemies spawned and killed)
        if enemies_spawned_this_wave >= game.max_enemies_current_wave and len(enemies) == 0:
            # Start wave interval timer if not already started
            if not game.wave_interval_started:
                game.wave_interval_started = True
                game.wave_interval_start_time = pygame.time.get_ticks()
            
            # Update wave interval timer
            elapsed = pygame.time.get_ticks() - game.wave_interval_start_time
            game.wave_interval_timer = max(0, game.WAVE_INTERVAL_TIME - elapsed + 1000) 
            
            # Advance to next wave when interval is complete
            if game.wave_interval_timer <= 0:
                enemies_spawned_this_wave = 0  # Reset for next wave
                advance_wave()

        all_sprites.update()  # Update all sprites (includes player with weapon sprites)
        player.weapons_inventory["gun"].update()  # Update the blaster (which updates its projectiles)
        player.weapons_inventory["melee"].update()  # Update the sword (which updates its attack animation)
        enemies.update(player)  # Always update enemies (they check internally if player is alive)
        
        # Check if gun reload should complete (happens every frame)
        blaster.check_reload_completion(player.misc_inventory["ammo"])
        
        ui_manager.update(player, blaster)  # Update UI elements with current player and gun state
        
        # Update melee cooldown bar position and value
        cooldown_remaining = max(0, sword.attack_cooldown - (pygame.time.get_ticks() - sword.time_from_last_attack))
        sword.cooldown_bar.x = player.rect.centerx - (sword.cooldown_bar.container_width // 2)
        sword.cooldown_bar.y = player.rect.top - 16
        sword.cooldown_bar.update(cooldown_remaining)

        # Update gun reload bar position and value
        reload_remaining = max(0, blaster.reload_time - (pygame.time.get_ticks() - blaster.time_of_last_reload))
        blaster.reload_bar.x = player.rect.centerx - (blaster.reload_bar.container_width // 2)
        blaster.reload_bar.y = player.rect.top - 26
        blaster.reload_bar.update(reload_remaining)

        # Collision detection
        check_projectile_collision(blaster.projectiles, enemies)
        check_projectile_collision(sword.sweeps, enemies)
        check_player_enemy_collision(player, enemies)
        check_enemy_enemy_collision(enemies)
        
        # Check enemy sweeps collision with player
        for enemy in enemies:
            for sweep in enemy.melee_sweeps:
                enemy_sweep_collision_rect = getattr(sweep, 'collision_rect', sweep.rect)
                player_collision_rect = getattr(player, 'collision_rect', player.rect)
                
                if enemy_sweep_collision_rect.colliderect(player_collision_rect):
                    if not player.is_hit:
                        player.take_damage(enemy.attack_damage)
                    sweep.kill()  # Remove sweep after hitting player

        all_sprites.draw(screen)  # Draw all sprites
        
        enemies.draw(screen)
        for enemy in enemies:
            enemy.healthbar.draw(screen)  # Draw health bars for enemies
        
        # Draw melee cooldown bar above player (only if cooldown is active)
        if cooldown_remaining > 0:
            sword.cooldown_bar.draw(screen)
        
        # Draw gun reload bar above player (only if reload is in progress)
        if reload_remaining > 0:
            blaster.reload_bar.draw(screen)
        
        player.weapons_inventory["gun"].projectiles.draw(screen)  # Draw all gun projectiles
        player.weapons_inventory["melee"].sweeps.draw(screen)  # Draw all sword sweep projectiles
        
        # Draw all enemy sweeps
        for enemy in enemies:
            enemy.melee_sweeps.draw(screen)
        
        # Draw UI text (includes pause image if paused)
        ui_manager.draw(player)

        mouse_pos = pygame.mouse.get_pos()
        if player.weapon_equipped.weapon_type == "gun":
            reticle_rect = gun_reticle.get_rect(center=mouse_pos)
            screen.blit(gun_reticle, reticle_rect)
        elif player.weapon_equipped.weapon_type == "melee":
            reticle_rect = melee_reticle.get_rect(center=mouse_pos)
            screen.blit(melee_reticle, reticle_rect)
    else:
        # Draw pause screen overlay
        pygame.mouse.set_visible(True)
        ui_manager.draw(player)
        
    

    if not game.pause_state:
        pygame.display.flip()  # Update the display
    else:
        pygame.display.flip()  # Still display when paused
    clock.tick(FPS)  # Maintain the frame rate

    
pygame.quit()
sys.exit()