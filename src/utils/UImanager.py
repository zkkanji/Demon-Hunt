import pygame
from src.entities import player
from src.utils.progressbar import ProgressBar
import src.game
from src.constants import WIDTH, HEIGHT

class UImanager:
    def __init__(self, screen, player, gun):
        self.screen = screen
        self.font = pygame.font.Font(f"assets/fonts/smallest-pixel-7/smallest_pixel-7.ttf", 24)

        # Health Bar UI
        healthbar_coords = (10, 0)
        healthbar_xscale = 6
        healthbar_yscale = 3
        self.healthbar = ProgressBar(healthbar_coords[0], 
                                    healthbar_coords[1], 
                                    player.current_health, 
                                    f"assets/misc/playerhealthbar.png", healthbar_xscale, 
                                    healthbar_yscale, 
                                    xmargin=11,
                                    ymargin=6.5,
                                    fill_color=(0, 255, 0)
                                    )
        
        # Ammo UI
        self.ammo_logo_coords = (10, 60)
        self.ammo_text_coords = (56, 73)
        ammo_logo_scale = 1.5
        ammo_logo_raw = pygame.image.load(f"assets/misc/ammologo.png")
        self.ammo_logo = pygame.transform.scale(ammo_logo_raw, (ammo_logo_raw.get_width() * ammo_logo_scale, ammo_logo_raw.get_height() * ammo_logo_scale))
        self.ammo_text = self.font.render(f"{gun.ammo}/{player.misc_inventory['ammo']}", True, (0, 0, 0))

        # Game Score UI
        self.score_coords = (WIDTH -130, 30)
        self.score_text = self.font.render(f"Score: {src.game.game_score}", True, (0, 0, 0))

    def update(self, player, gun):
        self.healthbar.update(player.current_health)
        self.ammo_text = self.font.render(f"{gun.ammo}/{player.misc_inventory['ammo']}", True, (0, 0, 0))
        self.score_text = self.font.render(f"Score: {src.game.game_score}", True, (0, 0, 0))

    def draw(self, player):
        self.healthbar.draw(self.screen)
        if player.weapon_equipped.weapon_type == "gun":
            self.screen.blit(self.ammo_logo, self.ammo_logo_coords)
            self.screen.blit(self.ammo_text, self.ammo_text_coords)
        self.screen.blit(self.score_text, self.score_coords)