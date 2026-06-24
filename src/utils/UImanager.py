import pygame
from src.utils.progressbar import ProgressBar
import src.game as game
from src.constants import WIDTH, HEIGHT, UI_COLOR

class UImanager:
    def __init__(self, screen, player):
        self.screen = screen
        self.font_letters = pygame.font.Font(f"assets/fonts/minecraftia/Minecraftia.ttf", 18)
        self.font_numbers = pygame.font.Font(f"assets/fonts/smallest-pixel-7/smallest_pixel-7.ttf", 24)
        self.font_numbers_large = pygame.font.Font(f"assets/fonts/smallest-pixel-7/smallest_pixel-7.ttf", 48)

        # Health Bar UI
        healthbar_coords = (10, 0)
        healthbar_xscale = 6
        healthbar_yscale = 3
        self.healthbar = ProgressBar(healthbar_coords[0], 
                                    healthbar_coords[1], 
                                    player.current_health, 
                                    f"assets/misc/playerhealthbar.png", 
                                    healthbar_xscale, 
                                    healthbar_yscale, 
                                    xmargin=11,
                                    ymargin=6.5,
                                    fill_color=(74, 211, 90)
                                    )
        
        # Pause UI
        self.pause_coords = (WIDTH - 80, HEIGHT - 90)
        self.pause_image_raw = pygame.image.load(f"assets/misc/pause.png")
        pause_logo_scale = 2.5
        self.pause_image = pygame.transform.scale(self.pause_image_raw, (self.pause_image_raw.get_width() * pause_logo_scale, self.pause_image_raw.get_height() * pause_logo_scale))
        
        # Ammo UI
        self.ammo_logo_coords = (10, 60)
        self.ammo_text_coords = (56, 73)
        ammo_logo_scale = 1.5
        ammo_logo_raw = pygame.image.load(f"assets/misc/ammologo.png")
        self.ammo_logo = pygame.transform.scale(ammo_logo_raw, (ammo_logo_raw.get_width() * ammo_logo_scale, ammo_logo_raw.get_height() * ammo_logo_scale))
        self.ammo_text = self.font_numbers.render(f"{player.weapons_inventory["gun"].ammo}/{player.ammo}", True, UI_COLOR)

        # Game Score UI
        self.score_text_coords = (WIDTH -150, 23)
        self.score_value_coords = (WIDTH -70, 25)
        self.score_text = self.font_letters.render(f"score: ", True, UI_COLOR)
        self.score_value = self.font_numbers.render(f"{game.game_score}", True, UI_COLOR)

        # Current Wave UI
        self.wave_text_coords = (WIDTH - 150, 50)
        self.wave_value_coords = (WIDTH - 75, 52)
        self.wave_text = self.font_letters.render(f"wave: ", True, UI_COLOR)
        self.wave_value = self.font_numbers.render(f"{game.wave_number}", True, UI_COLOR)

        # Enemies Left in Wave UI
        self.enemies_text_coords = (WIDTH - 150, 80)
        self.enemies_value_coords = (WIDTH - 50, 82)
        self.enemies_text = self.font_letters.render(f"enemies: ", True, UI_COLOR)
        self.enemies_value = self.font_numbers.render(f"{game.enemies_left_in_wave}", True, UI_COLOR)

        # Wave Interval Timer UI
        self.wave_interval_coords = (WIDTH // 2, HEIGHT // 2 - 20)
        self.wave_interval_value = self.font_numbers_large.render(f"{game.wave_interval_timer // 1000}", True, UI_COLOR)

        # Current Power-ups UI
        self.power_up_coords = (5, HEIGHT - 90)
        self.power_up_scale = 1.75
        self.power_up_image = None

    def update(self, player, gun):
        self.healthbar.max_value = player.max_health
        self.healthbar.update(player.current_health)
        self.ammo_text = self.font_numbers.render(f"{player.weapons_inventory['gun'].ammo}/{player.ammo}", True, UI_COLOR)
        self.score_value = self.font_numbers.render(f"{game.game_score}", True, UI_COLOR)
        self.wave_value = self.font_numbers.render(f"{game.wave_number}", True, UI_COLOR)
        self.enemies_value = self.font_numbers.render(f"{game.enemies_left_in_wave}", True, UI_COLOR)
        self.wave_interval_value = self.font_numbers_large.render(f"{game.wave_interval_timer // 1000}", True, UI_COLOR)
        if player.power_up is not None:
            self.power_up_image = player.power_up.UI_logo
            self.power_up_image = pygame.transform.scale(self.power_up_image, (self.power_up_image.get_width() * self.power_up_scale, self.power_up_image.get_height() * self.power_up_scale))

    def draw(self, player):
        if game.pause_state and not game.upgrade_selection_active:
            self.screen.blit(self.pause_image, self.pause_coords)
        else:
            # Always draw base UI elements
            self.healthbar.draw(self.screen)
            if player.weapon_equipped.weapon_type == "gun":
                self.screen.blit(self.ammo_logo, self.ammo_logo_coords)
                self.screen.blit(self.ammo_text, self.ammo_text_coords)
            if player.power_up is not None:
                self.screen.blit(self.power_up_image, self.power_up_coords)
            self.screen.blit(self.score_text, self.score_text_coords)
            self.screen.blit(self.score_value, self.score_value_coords)
            self.screen.blit(self.wave_text, self.wave_text_coords)
            self.screen.blit(self.wave_value, self.wave_value_coords)
            self.screen.blit(self.enemies_text, self.enemies_text_coords)
            self.screen.blit(self.enemies_value, self.enemies_value_coords)
            
            # Show wave interval timer when interval is active
            if game.wave_interval_timer > 1000:
                self.screen.blit(self.wave_interval_value, self.wave_interval_coords)
        
        