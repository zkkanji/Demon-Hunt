import pygame
from .base_weapon import BaseWeapon
from src.utils.progressbar import ProgressBar

class GunBase(BaseWeapon):

    def __init__(self, name, 
                damage,
                is_automatic,
                ammo_limit,
                reload_time,
                attack_cooldown,
                weapon_type = "gun"):
        
        super().__init__(name, damage, is_automatic, weapon_type)

        self.ammo_limit = ammo_limit
        self.reload_time = reload_time
        self.time_of_last_reload = 0
        self.is_reloading = False
        self.ammo = ammo_limit  # Start with a full magazine
        self.reload_bar = ProgressBar(0, 0, self.reload_time, "assets/misc/player-util-bar.png", 1.6, 1.6, fill_color=(227, 229, 82))
        self.ammo_to_transfer = 0  # Store how much ammo to transfer when reload completes
        self.attack_cooldown = attack_cooldown
        self.time_since_last_shot = 0
        self.is_shooting = False

    def reload(self, player_ammo):
        if self.ammo < self.ammo_limit and player_ammo > 0:
            current_time = pygame.time.get_ticks()
            
            # START reload (first call)
            if self.time_of_last_reload == 0:
                # Calculate and store how much ammo to transfer when timer completes
                ammo_needed = self.ammo_limit - self.ammo
                self.ammo_to_transfer = min(player_ammo, ammo_needed)
                
                self.time_of_last_reload = current_time
                self.is_reloading = True  # Reload starts
                return player_ammo - self.ammo_to_transfer  # Deduct from player's inventory now
        
        # If already has full ammo, not reloading
        if self.ammo >= self.ammo_limit:
            self.is_reloading = False
        
        return player_ammo

    def check_reload_completion(self):
        """Check if reload should finish and complete it (runs every frame)"""
        if self.is_reloading and self.time_of_last_reload != 0:
            current_time = pygame.time.get_ticks()
            elapsed_time = current_time - self.time_of_last_reload
            
            if elapsed_time >= self.reload_time:
                # Reload time finished - transfer the stored ammo to magazine
                self.ammo += self.ammo_to_transfer
                self.ammo_to_transfer = 0
                
                # Reload complete - reset state
                self.is_reloading = False
                self.time_of_last_reload = 0

    def check_shot_ready(self):
        if self.is_shooting:
            return False
        if self.time_since_last_shot == 0:
            return True
        return (pygame.time.get_ticks() - self.time_since_last_shot) >= self.attack_cooldown
