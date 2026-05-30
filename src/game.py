import pygame
import random
from .constants import WIDTH, HEIGHT

game_score = 0
wave_number = 0
pause_state = False
max_enemies_current_wave = 0
enemies_left_in_wave = max_enemies_current_wave
ENEMIES_PER_WAVE = [5, 5, 7, 10, 12, 15, 17, 18, 20, 23, 25]
MOST_ENEMIES_ON_SCREEN = 10  # Max number of enemies to spawn at once for performance reasons
enemy_x_left_spawn_bounds = (-50, -30)  
enemy_x_right_spawn_bounds = (WIDTH + 30, WIDTH + 50)  
WAVE_INTERVAL_TIME = 5000  # milliseconds (5 seconds) between waves
wave_interval_timer = 0
wave_interval_started = False
wave_interval_start_time = 0

def get_enemy_spawn_position():
    """Calculate and return random spawn position at screen edge.
    
    Returns:
        tuple: (x, y) coordinates for enemy spawn
    """
    # Randomly choose left or right edge
    if random.choice([True, False]):
        # Left edge
        x = random.randint(enemy_x_left_spawn_bounds[0], enemy_x_left_spawn_bounds[1])
    else:
        # Right edge
        x = random.randint(enemy_x_right_spawn_bounds[0], enemy_x_right_spawn_bounds[1])
    
    # Random Y position across screen height
    y = random.randint(50, HEIGHT - 50)
    
    return (x, y)


def check_projectile_collision(projectiles, enemies):
    """
    Check collisions between projectiles and enemies.
    Damages enemies and removes projectiles on hit.
    Awards score based on damage (1.5x) and kills (100 points).
    Uses collision_rect if available (for accurate collision), otherwise uses rect.
    
    Args:
        projectiles: pygame.sprite.Group of projectiles
        enemies: pygame.sprite.Group of enemies
    """
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
                enemy.take_damage(projectile.damage)
                
                # Award bonus points for kill
                if was_alive and enemy.current_health <= 0:
                    game_score += 100
                
                projectile.kill()  # Remove projectile after hit
                break  # Only hit one enemy per projectile


def check_player_enemy_collision(player, enemies):
    """
    Check collisions between player and enemies.
    Player takes damage and enemy is knocked back on collision.
    Only one collision is processed per frame per enemy to prevent multiple hits.
    
    Args:
        player: The player object
        enemies: pygame.sprite.Group of enemies
    """
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

def pause_game():
    global pause_state
    pause_state = not pause_state  # Toggle pause state
    return pause_state

