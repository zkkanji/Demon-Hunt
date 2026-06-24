import pygame
import sys
import random
import src.game as game
from src.constants import WIDTH, HEIGHT, FPS, BG_COLOR
from src.entities.player import Player
from src.weapons.blaster import Blaster   
from src.weapons.shotgun import Shotgun
from src.weapons.sword import Sword
from src.entities.devil1 import Devil1
from src.entities.devil2 import Devil2
from src.game import check_projectile_collision, check_player_enemy_collision, pause_game, advance_wave, get_enemy_spawn_position, check_enemy_enemy_collision, check_player_drop_collision, check_bomb_explosion_collisions
from src.utils.UImanager import UImanager
from src.utils.upgrade_cards import player_upgrade_card, weapon_upgrade_card, weapon_unlock_card, power_up_card
from src.utils.power_ups import Invincibility, SpeedBoost, Bomb_PowerUp
from src.utils.card_selection import initialize_upgrade_selection, update_and_draw_upgrade_cards, handle_card_click, update_upgrade_card_weapons

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Demon Hunt")

clock = pygame.time.Clock()

player = Player(WIDTH // 2, HEIGHT // 2)
blaster = Blaster()
sword = Sword()
shotgun = Shotgun()
player.gun_inventory.append(blaster)  
player.melee_inventory.append(sword)
player.gun_inventory.append(shotgun)  # Add shotgun to gun inventory rn for testing
player.weapon_swap(shotgun)
player.weapon_swap(sword) 
player.equip_weapon(player.weapons_inventory["gun"])  # Equip the blaster as the current weapon

ui_manager = UImanager(screen, player)

# Load reticles for custom cursor
gun_reticle = pygame.image.load("assets/misc/gun-reticle.png")
melee_reticle = pygame.image.load("assets/misc/melee-reticle.png")
pause_snapshot = None

all_sprites = pygame.sprite.Group(player)
enemies = pygame.sprite.Group()
enemy_drops = pygame.sprite.Group()
enemy_projectiles = pygame.sprite.Group()  # projectiles that outlive their enemy
bombs = pygame.sprite.Group()

# Initialize first wave
advance_wave()

# Wave spawning system
enemy_spawn_timer = 0
enemy_spawn_rate = 120  # Spawn an enemy every 120 frames (2 seconds at 60 FPS)
enemies_spawned_this_wave = 0  # Track how many enemies have been spawned this wave

# Health buff cards
health_up_10 = player_upgrade_card("Increase Max Health by 10", 10, f"assets/upgrade-cards/health-upgrade/health+10", player, "max_health")
health_up_15 = player_upgrade_card("Increase Max Health by 15", 15, f"assets/upgrade-cards/health-upgrade/health+15", player, "max_health")
health_up_20 = player_upgrade_card("Increase Max Health by 20", 20, f"assets/upgrade-cards/health-upgrade/health+20", player, "max_health")
health_upgrade_cards = [health_up_10, health_up_15, health_up_20]

# Equipped Gun buff cards
gun_dmg_up_5 = weapon_upgrade_card("Increase Equipped Gun Damage by 5", 5, f"assets/upgrade-cards/gun-upgrade/gun+5", player.weapons_inventory["gun"], "damage")
gun_dmg_up_10 = weapon_upgrade_card("Increase Equipped Gun Damage by 10", 10, f"assets/upgrade-cards/gun-upgrade/gun+10", player.weapons_inventory["gun"], "damage")
gun_dmg_up_15 = weapon_upgrade_card("Increase Equipped Gun Damage by 15", 15, f"assets/upgrade-cards/gun-upgrade/gun+15", player.weapons_inventory["gun"], "damage")
gun_upgrade_cards = [gun_dmg_up_5, gun_dmg_up_10, gun_dmg_up_15]

# Equipped Melee buff cards
melee_dmg_up_5 = weapon_upgrade_card("Increase Equipped Melee Damage by 5", 5, f"assets/upgrade-cards/melee-upgrade/melee+5", player.weapons_inventory["melee"], "damage")
melee_dmg_up_10 = weapon_upgrade_card("Increase Equipped Melee Damage by 10", 10, f"assets/upgrade-cards/melee-upgrade/melee+10", player.weapons_inventory["melee"], "damage")
melee_dmg_up_15 = weapon_upgrade_card("Increase Equipped Melee Damage by 15", 15, f"assets/upgrade-cards/melee-upgrade/melee+15", player.weapons_inventory["melee"], "damage")
melee_upgrade_cards = [melee_dmg_up_5, melee_dmg_up_10, melee_dmg_up_15]

# Equipped Gun Magazine Size buff cards
mag_up_2 = weapon_upgrade_card("Increase Current Gun Magazine Size by 2", 2, f"assets/upgrade-cards/mag-upgrade/mag+2", player.weapons_inventory["gun"], "ammo_limit")
mag_up_3 = weapon_upgrade_card("Increase Current Gun Magazine Size by 3", 3, f"assets/upgrade-cards/mag-upgrade/mag+3", player.weapons_inventory["gun"], "ammo_limit")
mag_up_5 = weapon_upgrade_card("Increase Current Gun Magazine Size by 5", 5, f"assets/upgrade-cards/mag-upgrade/mag+5", player.weapons_inventory["gun"], "ammo_limit")
mag_up_6 = weapon_upgrade_card("Increase Current Gun Magazine Size by 6", 6, f"assets/upgrade-cards/mag-upgrade/mag+6", player.weapons_inventory["gun"], "ammo_limit")
mag_up_9 = weapon_upgrade_card("Increase Current Gun Magazine Size by 9", 9, f"assets/upgrade-cards/mag-upgrade/mag+9", player.weapons_inventory["gun"], "ammo_limit")
blaster_magazine_upgrade_cards = [mag_up_2, mag_up_3, mag_up_5]
shotgun_magazine_upgrade_cards = [mag_up_3, mag_up_6, mag_up_9]

# Equipped Melee Range buff cards
range_up_5 = weapon_upgrade_card("Increase Current Melee Range by 5", 5, f"assets/upgrade-cards/melee-radius-upgrade/radius+5", player.weapons_inventory["melee"], "melee_range")
range_up_10 = weapon_upgrade_card("Increase Current Melee Range by 10", 10, f"assets/upgrade-cards/melee-radius-upgrade/radius+10", player.weapons_inventory["melee"], "melee_range")
range_up_15 = weapon_upgrade_card("Increase Current Melee Range by 15", 15, f"assets/upgrade-cards/melee-radius-upgrade/radius+15", player.weapons_inventory["melee"], "melee_range")
melee_range_upgrade_cards = [range_up_5, range_up_10, range_up_15]

# Power-up cards
invincibility_powerup = Invincibility(player, 10000)
speed_boost_powerup = SpeedBoost(player, 10000)

invincibility_card = power_up_card(player, invincibility_powerup, f"assets/upgrade-cards/powerup-cards/invincibility")
speed_boost_card = power_up_card(player, speed_boost_powerup, f"assets/upgrade-cards/powerup-cards/speed-boost")

bomb_powerup = Bomb_PowerUp(player, 0)
bomb_card = power_up_card(player, bomb_powerup, f"assets/upgrade-cards/powerup-cards/bomb")
power_up_cards = [invincibility_card, speed_boost_card, bomb_card]

# Variable to store selected cards during upgrade selection
selected_upgrade_cards = None

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            # Only allow pause toggle if upgrade cards are not being shown
            if not game.upgrade_selection_active:
                pause_game()
        elif event.type == pygame.MOUSEBUTTONDOWN:
                # Handle card clicks during upgrade selection
                if game.upgrade_selection_active and selected_upgrade_cards:
                    mouse_pos = pygame.mouse.get_pos()
                    if handle_card_click(selected_upgrade_cards, mouse_pos):
                        game.wave_interval_started = True 
                        game.upgrade_selection_active = False
                        selected_upgrade_cards = None
                        game.pause_state = False
                        game.wave_interval_start_time = pygame.time.get_ticks()
                        
                        # Reset spawned counter for next wave
                        enemies_spawned_this_wave = 0
                    
    if not game.pause_state:        
        screen.fill(BG_COLOR)  # Clear the screen with a green color
        pygame.mouse.set_visible(False)
        
        # Update wave interval timer if active
        if game.wave_interval_started:
            elapsed = pygame.time.get_ticks() - game.wave_interval_start_time
            game.wave_interval_timer = max(0, game.WAVE_INTERVAL_TIME - elapsed) + 1000
            if game.wave_interval_timer <= 1000:
                game.wave_interval_started = False
                advance_wave()  # Advance to next wave when interval ends
        
        # Draw shadows on the ground BEFORE drawing characters
        if player.is_alive:
            shadow_rect = player.shadow.get_rect(midbottom=(player.rect.centerx, player.rect.bottom-5))
            screen.blit(player.shadow, (shadow_rect.x, shadow_rect.y-16.5))
        
        for enemy in enemies:
            shadow_rect = enemy.shadow.get_rect(midbottom=(enemy.rect.centerx-2, enemy.rect.bottom-2))
            screen.blit(enemy.shadow, (shadow_rect.x, shadow_rect.y-6))

        for drop in enemy_drops:
            shadow_rect = drop.shadow.get_rect(midbottom=(drop.rect.centerx, drop.rect.bottom))
            screen.blit(drop.shadow, (shadow_rect.x, shadow_rect.y+7))
        
        # Wave spawning system - spawn enemies up to the wave limit (but NOT during interval)
        if enemies_spawned_this_wave < game.max_enemies_current_wave and not game.wave_interval_started:
            enemy_spawn_timer += 1
            if enemy_spawn_timer >= enemy_spawn_rate and len(enemies) < game.MOST_ENEMIES_ON_SCREEN:
                x, y = get_enemy_spawn_position()
                enemy = random.choice([Devil1])(x, y)
                enemies.add(enemy)
                enemies_spawned_this_wave += 1  # Increment spawned counter
                enemy_spawn_timer = 0
        
        # Check if wave is complete (all enemies spawned and killed)
        if enemies_spawned_this_wave >= game.max_enemies_current_wave and len(enemies) == 0:
            # Show upgrade card selection immediately (before timer)
            if not game.upgrade_selection_active:
                # Initialize upgrade card selection overlay
                card_lists = [
                    health_upgrade_cards,
                    gun_upgrade_cards,
                    melee_upgrade_cards,
                    melee_range_upgrade_cards,
                    power_up_cards
                ]
                if player.weapons_inventory["gun"].name == "Blaster":
                    update_upgrade_card_weapons(blaster_magazine_upgrade_cards, player.weapons_inventory["gun"])
                    card_lists.append(blaster_magazine_upgrade_cards)
                elif player.weapons_inventory["gun"].name == "Shotgun":
                    update_upgrade_card_weapons(shotgun_magazine_upgrade_cards, player.weapons_inventory["gun"])
                    card_lists.append(shotgun_magazine_upgrade_cards)
                selected_upgrade_cards = initialize_upgrade_selection(card_lists)
                game.upgrade_selection_active = True
                game.pause_state = True

        all_sprites.update()  # Update all sprites (includes player with weapon sprites)
        player.weapons_inventory["gun"].update()  # Update the blaster (which updates its projectiles)
        player.weapons_inventory["melee"].update()  # Update the sword (which updates its attack animation)
        living_before = list(enemies)
        enemies.update(player)  # Always update enemies (they check internally if player is alive)

        # Harvest drops and orphaned projectiles from enemies that died this frame
        for enemy in living_before:
            if not enemy.alive():
                for drop in enemy.pending_drops:
                    enemy_drops.add(drop)
                enemy.pending_drops.clear()
                if hasattr(enemy, 'projectiles'):
                    for proj in list(enemy.projectiles):
                        enemy_projectiles.add(proj)
                    enemy.projectiles.empty()
        enemy_drops.update()
        enemy_projectiles.update()

        # Harvest bombs dropped this frame
        for bomb in bomb_powerup.pending_bombs:
            bombs.add(bomb)
        bomb_powerup.pending_bombs.clear()
        bombs.update()
        
        # Check if gun reload should complete for every gun in inventory
        for gun in player.gun_inventory:
            gun.check_reload_completion()

        ui_manager.update(player, blaster)  # Update UI elements with current player and gun state

        # Update melee cooldown bar position and value
        cooldown_remaining = max(0, sword.attack_cooldown - (pygame.time.get_ticks() - sword.time_from_last_attack))
        sword.cooldown_bar.x = player.rect.centerx - (sword.cooldown_bar.container_width // 2)
        sword.cooldown_bar.y = player.rect.top - 16
        sword.cooldown_bar.update(cooldown_remaining)

        # Update gun reload bar for the currently equipped gun
        equipped_gun = player.weapon_equipped if (player.weapon_equipped and player.weapon_equipped.weapon_type == "gun") else None
        if equipped_gun:
            reload_remaining = max(0, equipped_gun.reload_time - (pygame.time.get_ticks() - equipped_gun.time_of_last_reload))
            equipped_gun.reload_bar.x = player.rect.centerx - (equipped_gun.reload_bar.container_width // 2)
            equipped_gun.reload_bar.y = player.rect.top - 26
            equipped_gun.reload_bar.update(reload_remaining)
        else:
            reload_remaining = 0

        # Collision detection
        check_projectile_collision(player.weapons_inventory["gun"].projectiles, enemies)
        check_projectile_collision(sword.sweeps, enemies)
        check_player_enemy_collision(player, enemies)
        check_enemy_enemy_collision(enemies)
        for drop in enemy_drops:
            if check_player_drop_collision(player, drop):
                drop.collect()
        check_bomb_explosion_collisions(bombs, enemies, player)

        # Check enemy sweeps collision with player
        for enemy in enemies:
            if hasattr(enemy, 'melee_sweeps'):
                for sweep in enemy.melee_sweeps:
                    enemy_sweep_collision_rect = getattr(sweep, 'collision_rect', sweep.rect)
                    player_collision_rect = getattr(player, 'collision_rect', player.rect)

                    if enemy_sweep_collision_rect.colliderect(player_collision_rect):
                        if not player.is_hit:
                            player.take_damage(enemy.attack_damage)
                        sweep.kill()  # Remove sweep after hitting player

        # Check enemy projectiles collision with player
        player_collision_rect = getattr(player, 'collision_rect', player.rect)
        for enemy in enemies:
            for proj in list(getattr(enemy, 'projectiles', [])):
                proj_rect = getattr(proj, 'collision_rect', proj.rect)
                if proj_rect.colliderect(player_collision_rect):
                    if not player.is_hit:
                        player.take_damage(enemy.attack_damage)
                    proj.kill()
        for proj in list(enemy_projectiles):
            proj_rect = getattr(proj, 'collision_rect', proj.rect)
            if proj_rect.colliderect(player_collision_rect):
                if not player.is_hit:
                    player.take_damage(proj.damage)
                proj.kill()

        # Drawing of all things on screen
        all_sprites.draw(screen)
        enemies.draw(screen)
        enemy_drops.draw(screen)
        for bomb in bombs:
            bomb.draw(screen)
        for enemy in enemies:
            enemy.healthbar.draw(screen)  # Draw health bars for enemies
            for dn in enemy.damage_numbers:
                dn.draw(screen)
            if hasattr(enemy, 'projectiles'):
                enemy.projectiles.draw(screen)  # Draw enemy projectiles if they exist
            elif hasattr(enemy, 'melee_sweeps'):
                enemy.melee_sweeps.draw(screen)  # Draw enemy melee sweeps if they exist

        # Draw melee cooldown bar above player (only if cooldown is active)
        if cooldown_remaining > 0:
            sword.cooldown_bar.draw(screen)
        
        # Draw gun reload bar above player (only if reload is in progress)
        if reload_remaining > 0 and equipped_gun:
            equipped_gun.reload_bar.draw(screen)
        
        player.weapons_inventory["gun"].projectiles.draw(screen)  # Draw all gun projectiles
        player.weapons_inventory["melee"].sweeps.draw(screen)  # Draw all sword sweep projectiles
        enemy_projectiles.draw(screen)  # Draw orphaned projectiles from dead enemies
        
        # Draw UI text (includes pause image if paused)
        ui_manager.draw(player)
        pause_snapshot = screen.copy()  # Capture the current screen for pause overlay

        mouse_pos = pygame.mouse.get_pos()
        if player.weapon_equipped.weapon_type == "gun":
            reticle_rect = gun_reticle.get_rect(center=mouse_pos)
            screen.blit(gun_reticle, reticle_rect)
        elif player.weapon_equipped.weapon_type == "melee":
            reticle_rect = melee_reticle.get_rect(center=mouse_pos)
            screen.blit(melee_reticle, reticle_rect)
    elif game.pause_state:
        # Draw pause screen overlay
        pygame.mouse.set_visible(True)
        screen.blit(pause_snapshot, (0, 0))  # Show the captured game screen when paused
        overlay = pygame.Surface((WIDTH, HEIGHT)); overlay.set_alpha(62); overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0)) 
        ui_manager.draw(player)
        
        # Draw upgrade cards if selection is active
        if game.upgrade_selection_active and selected_upgrade_cards:
            mouse_pos = pygame.mouse.get_pos()
            update_and_draw_upgrade_cards(screen, selected_upgrade_cards, mouse_pos)
        

    if not game.pause_state:
        pygame.display.flip()  # Update the display
    else:
        pygame.display.flip()  # Still display when paused
    clock.tick(FPS)  # Maintain the frame rate

pygame.quit()
sys.exit()