import pygame
import random

game_score = 0
wave_number = 0
max_enemies_current_wave = 0
enemies_left_in_wave = max_enemies_current_wave
ENEMIES_PER_WAVE = [5, 5, 7, 10, 11, 12, 14, 15, 17]
MOST_ENEMIES_ON_SCREEN = 10  # Max number of enemies to spawn at once for performance reasons
WAVE_INTERVAL_TIME = 5000  # milliseconds (5 seconds) between waves
wave_interval_timer = 0
wave_interval_started = False
wave_interval_start_time = 0

def get_enemy_spawn_position():
    surface = pygame.display.get_surface()
    screen_w, screen_h = surface.get_width(), surface.get_height()

    # Randomly choose left or right edge
    if random.choice([True, False]):
        x = random.randint(-50, -30)
    else:
        x = random.randint(screen_w + 30, screen_w + 50)

    # Random Y position across screen height
    y = random.randint(50, screen_h - 50)

    return (x, y)


def check_projectile_collision(projectiles, enemies):
    global game_score
    
    for projectile in projectiles:
        # Use collision_rect if available (for rotating sweeps/padded sprites), otherwise use rect
        proj_collision_rect = getattr(projectile, 'collision_rect', projectile.rect)
        
        # Check if projectile hits any enemy
        for enemy in enemies:
            # Use collision rect if available, otherwise use rect
            enemy_collision_rect = getattr(enemy, 'collision_rect', enemy.rect)
            
            if proj_collision_rect.colliderect(enemy_collision_rect):
                # Award points for damage (1.5x the damage dealt)
                game_score += int(projectile.damage * 1.5)
                
                # Check if enemy is alive before taking damage
                was_alive = enemy.current_health > 0
                
                # Apply damage to enemy
                enemy.take_damage(projectile.damage, projectile.is_critical)
                
                # Award bonus points for kill
                if was_alive and enemy.current_health <= 0:
                    game_score += 100
                
                projectile.kill()  # Remove projectile after hit
                break  # Only hit one enemy per projectile


def check_player_enemy_collision(player, enemies):
    # Use collision_rect if available, otherwise use rect
    player_collision_rect = getattr(player, 'collision_rect', player.rect)
    
    for enemy in enemies:
        # Use collision rect if available, otherwise use rect
        enemy_collision_rect = getattr(enemy, 'collision_rect', enemy.rect)
        
        if player_collision_rect.colliderect(enemy_collision_rect):
            # Only apply damage if player is not already in hit state (cooldown prevention)
            if not player.is_hit:
                # Apply damage to player
                player.take_damage(enemy.attack_damage)
            
            # Apply knockback to enemy (opposite direction of movement)
            knockback_x = -enemy.direction[0] * enemy.knockback_velocity
            knockback_y = -enemy.direction[1] * enemy.knockback_velocity
            
            enemy.velocity_x = knockback_x
            enemy.velocity_y = knockback_y
            enemy.is_moving = False  # Stop regular movement during knockback (shows idle frames)
            
            # Store knockback state with timer for duration
            enemy.is_knockback = True
            enemy.knockback_timer = pygame.time.get_ticks()

def check_enemy_enemy_collision(enemies):
    enemies_list = list(enemies)
    for i in range(len(enemies_list) - 1):
        for j in range(i + 1, len(enemies_list)):
            enemy1 = enemies_list[i]
            enemy2 = enemies_list[j]

            rect1 = getattr(enemy1, 'collision_rect', enemy1.rect)
            rect2 = getattr(enemy2, 'collision_rect', enemy2.rect)

            if rect1.colliderect(rect2):
                dx = enemy1.x - enemy2.x
                dy = enemy1.y - enemy2.y
                distance = (dx ** 2 + dy ** 2) ** 0.5

                if distance > 0:
                    push_x = (dx / distance) * 2
                    push_y = (dy / distance) * 2

                    enemy1.x += push_x
                    enemy1.y += push_y
                    enemy2.x -= push_x
                    enemy2.y -= push_y

                    #Update Enemy Rects
                    enemy1.rect.center = (int(enemy1.x), int(enemy1.y))
                    enemy1.collision_rect.center = enemy1.rect.center
                    enemy2.rect.center = (int(enemy2.x), int(enemy2.y))
                    enemy2.collision_rect.center = enemy2.rect.center

def check_player_drop_collision(player, drop):
    player_collision_rect = getattr(player, 'collision_rect', player.rect)
    return player_collision_rect.colliderect(drop.rect)

def check_bomb_explosion_collisions(bombs, enemies, player):
    for bomb in bombs:
        if bomb.state != "exploding":
            continue

        for enemy in enemies:
            if enemy in bomb.damaged_entities:
                continue
            enemy_collision_rect = getattr(enemy, 'collision_rect', enemy.rect)
            if bomb.rect.colliderect(enemy_collision_rect):
                enemy.take_damage(bomb.damage)
                bomb.damaged_entities.add(enemy)

        if player not in bomb.damaged_entities:
            player_collision_rect = getattr(player, 'collision_rect', player.rect)
            if bomb.rect.colliderect(player_collision_rect):
                player.take_damage(bomb.damage)
                bomb.damaged_entities.add(player)

def check_sword_projectile_collisions(sword_projectiles, enemy_projectiles):
    for sword in sword_projectiles:
        sword_collision_rect = getattr(sword, 'collision_rect', sword.rect)
        for enemy_proj in enemy_projectiles:
            enemy_proj_collision_rect = getattr(enemy_proj, 'collision_rect', enemy_proj.rect)
            if sword_collision_rect.colliderect(enemy_proj_collision_rect):
                sword.kill()
                enemy_proj.kill()
                break  # Exit inner loop since the sword is destroyed

def advance_wave():
    global wave_number, enemies_left_in_wave, max_enemies_current_wave, wave_interval_started, wave_interval_start_time
    wave_number += 1
    if wave_number > len(ENEMIES_PER_WAVE):
        max_enemies_current_wave = ENEMIES_PER_WAVE[len(ENEMIES_PER_WAVE) - 1]  # Cap at max defined enemies if wave exceeds list
    else:
        max_enemies_current_wave = ENEMIES_PER_WAVE[wave_number - 1]
    enemies_left_in_wave = max_enemies_current_wave
    wave_interval_started = False  # Reset for next wave check

def decrement_wave_enemies():
    global enemies_left_in_wave
    if enemies_left_in_wave > 0:
        enemies_left_in_wave -= 1

def triple_card_selector(cards):
    if len(cards) >= 3:
        card_triple = []
        for i in range(3):
            index = random.randint(0, len(cards) - 1)
            card_triple.append(cards[index])
            cards.remove(cards[index])  # Remove selected card to avoid duplicates in triple
        return card_triple
    return cards   


