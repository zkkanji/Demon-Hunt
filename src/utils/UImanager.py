import pygame
from src.utils.progressbar import ProgressBar
import src.game as game
from src.constants import UI_COLOR
from src.utils.assets import load_image

class UImanager:
    def __init__(self, screen, player):
        self.screen = screen
        self.font_letters = pygame.font.Font(f"assets/fonts/minecraftia/Minecraftia.ttf", 18)
        self.font_numbers = pygame.font.Font(f"assets/fonts/smallest-pixel-7/smallest_pixel-7.ttf", 24)
        self.font_numbers_large = pygame.font.Font(f"assets/fonts/smallest-pixel-7/smallest_pixel-7.ttf", 48)

        # Health Bar UI (anchored top-left, no dynamic coords needed)
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

        # Pause UI (coords computed at draw-time from screen size)
        self.pause_image_raw = load_image("assets/misc/pause.png")
        pause_logo_scale = 2.5
        self.pause_image = pygame.transform.scale(self.pause_image_raw, (self.pause_image_raw.get_width() * pause_logo_scale, self.pause_image_raw.get_height() * pause_logo_scale))

        # Ammo UI (anchored top-left, static coords)
        self.ammo_logo_coords = (10, 60)
        self.ammo_text_coords = (56, 73)
        ammo_logo_scale = 1.5
        ammo_logo_raw = load_image("assets/misc/ammologo.png")
        self.ammo_logo = pygame.transform.scale(ammo_logo_raw, (ammo_logo_raw.get_width() * ammo_logo_scale, ammo_logo_raw.get_height() * ammo_logo_scale))
        self.ammo_text = self.font_numbers.render(f"{player.weapons_inventory['gun'].ammo}/{player.ammo}", True, UI_COLOR)

        # Game Score UI (text surfaces only; coords computed at draw-time)
        self.score_text = self.font_letters.render(f"score: ", True, UI_COLOR)
        self.score_value = self.font_numbers.render(f"{game.game_score}", True, UI_COLOR)

        # Current Wave UI
        self.wave_text = self.font_letters.render(f"wave: ", True, UI_COLOR)
        self.wave_value = self.font_numbers.render(f"{game.wave_number}", True, UI_COLOR)

        # Enemies Left in Wave UI
        self.enemies_text = self.font_letters.render(f"enemies: ", True, UI_COLOR)
        self.enemies_value = self.font_numbers.render(f"{game.enemies_left_in_wave}", True, UI_COLOR)

        # Wave Interval Timer UI
        self.wave_interval_value = self.font_numbers_large.render(f"{(game.wave_interval_timer + 999) // 1000}", True, UI_COLOR)

        # Current Power-ups UI
        self.power_up_scale = 1.75
        self.power_up_image = None

    def update(self, player):
        self.healthbar.max_value = player.max_health
        self.healthbar.update(player.current_health)
        self.ammo_text = self.font_numbers.render(f"{player.weapons_inventory['gun'].ammo}/{player.ammo}", True, UI_COLOR)
        self.score_value = self.font_numbers.render(f"{game.game_score}", True, UI_COLOR)
        self.wave_value = self.font_numbers.render(f"{game.wave_number}", True, UI_COLOR)
        self.enemies_value = self.font_numbers.render(f"{game.enemies_left_in_wave}", True, UI_COLOR)
        self.wave_interval_value = self.font_numbers_large.render(f"{(game.wave_interval_timer + 999) // 1000}", True, UI_COLOR)
        if player.power_up is not None:
            self.power_up_image = player.power_up.UI_logo
            self.power_up_image = pygame.transform.scale(self.power_up_image, (self.power_up_image.get_width() * self.power_up_scale, self.power_up_image.get_height() * self.power_up_scale))

    def draw(self, player, game_state):
        w = self.screen.get_width()
        h = self.screen.get_height()

        if game_state == "paused":
            self.screen.blit(self.pause_image, (w - 80, h - 90))
        else:
            # Always draw base UI elements
            self.healthbar.draw(self.screen)
            if player.weapon_equipped.weapon_type == "gun":
                self.screen.blit(self.ammo_logo, self.ammo_logo_coords)
                self.screen.blit(self.ammo_text, self.ammo_text_coords)
            if player.power_up is not None:
                self.screen.blit(self.power_up_image, (5, h - 90))
            self.screen.blit(self.score_text, (w - 150, 23))
            self.screen.blit(self.score_value, (w - 70, 25))
            self.screen.blit(self.wave_text, (w - 150, 50))
            self.screen.blit(self.wave_value, (w - 75, 52))
            self.screen.blit(self.enemies_text, (w - 150, 80))
            self.screen.blit(self.enemies_value, (w - 50, 82))

            # Show wave interval timer when interval is active
            if game.wave_interval_timer > 0:
                self.screen.blit(self.wave_interval_value, (w // 2, h // 2 - 20))
