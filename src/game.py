import pygame

game_score = 0

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

