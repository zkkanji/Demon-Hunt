import pygame
from src.constants import MIN_WIDTH, MIN_HEIGHT, UI_COLOR

class MenuText: 

    def __init__(self, screen):
        self.screen = screen
        self.font_letters = pygame.font.Font(f"assets/fonts/minecraftia/Minecraftia.ttf", 30)
        
        #Credits UI
        ctext1 = "Codebase: Zain Kanji"
        ctext2 = "Graphics: Zain Kanji"
        ctext3 = "Animations: Zain Kanji"
        ctext4 = "Sound: Zain Kanji"

        self.credits1 = self.font_letters.render(ctext1, True, UI_COLOR)
        self.credits2 = self.font_letters.render(ctext2, True, UI_COLOR)   
        self.credits3 = self.font_letters.render(ctext3, True, UI_COLOR)
        self.credits4 = self.font_letters.render(ctext4, True, UI_COLOR)

        cred_xpos = MIN_WIDTH // 2 - 180
        cred_ypos = MIN_HEIGHT // 2 - 130
        cred_gap_int = 70
        self.creditline_pos = (
            (cred_xpos, cred_ypos),
            (cred_xpos, cred_ypos + cred_gap_int*1),
            (cred_xpos, cred_ypos + cred_gap_int*2),
            (cred_xpos, cred_ypos + cred_gap_int*3)
        )

        #Controls UI
        scale = 5
        self.controls1 = pygame.image.load(f"assets/menu/controls/c1.png")
        self.controls1 = pygame.transform.scale(self.controls1, (self.controls1.get_width() * scale, self.controls1.get_height() * scale))
        self.controls2 = pygame.image.load(f"assets/menu/controls/c2.png")
        self.controls2 = pygame.transform.scale(self.controls2, (self.controls2.get_width() * scale, self.controls2.get_height() * scale))  
        self.controls3 = pygame.image.load(f"assets/menu/controls/c3.png")
        self.controls3 = pygame.transform.scale(self.controls3, (self.controls3.get_width() * scale, self.controls3.get_height() * scale))
        self.controls4 = pygame.image.load(f"assets/menu/controls/c4.png")
        self.controls4 = pygame.transform.scale(self.controls4, (self.controls4.get_width() * scale, self.controls4.get_height() * scale))
        cont_xpos = MIN_WIDTH // 2 - 300
        cont_ypos = MIN_HEIGHT // 2 - 300
        cont_gap_int = 150
        self.controls_pos = (
            (cont_xpos, cont_ypos),
            (cont_xpos, cont_ypos + cont_gap_int*1),
            (cont_xpos, cont_ypos + cont_gap_int*2),
            (cont_xpos, cont_ypos + cont_gap_int*2.5)
        )

    def draw(self, game_state):
        if game_state == "credits":
            for i in range(self.creditline_pos.__len__()):
                self.screen.blit(getattr(self, f"credits{i+1}"), self.creditline_pos[i])
        elif game_state == "controls":
            for i in range(self.controls_pos.__len__()):
                self.screen.blit(getattr(self, f"controls{i+1}"), self.controls_pos[i])