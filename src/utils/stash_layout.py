import pygame
from src.constants import STASH_BG_COLOR, UI_COLOR
from src.menu_stuff.menu_buttons import MenuButton


class StashLayout:
    def __init__(self, player):
        self.player = player
        self.current_guns = []
        self.current_melees = []
        self.equip_buttons = {}
        self.weapon_rects = {}
        self.hovered_tooltip = None
        self.back_button = MenuButton("back", 0, 0, "back", scale=2)
        self.font_headers = pygame.font.Font(f"assets/fonts/minecraftia/Minecraftia.ttf", 24)
        self.font_letters = pygame.font.Font(f"assets/fonts/minecraftia/Minecraftia.ttf", 16)
        self.font_numbers = pygame.font.Font(f"assets/fonts/smallest-pixel-7/smallest_pixel-7.ttf", 24)
        self.get_weapons()

    def get_weapons(self):
        self.current_guns = list(self.player.gun_inventory)
        self.current_melees = list(self.player.melee_inventory)

    def _draw_centered_text(self, surface, text, font, center, color=UI_COLOR):
        image = font.render(text, True, color)
        surface.blit(image, image.get_rect(center=center))

    def _draw_weapon(self, surface, weapon, rect, stats):
        mouse_pos = pygame.mouse.get_pos()
        idle_image = weapon.weapon_cards[0]
        card_rect = idle_image.get_rect(center=rect.center)
        visible_rect = idle_image.get_bounding_rect().move(card_rect.topleft)
        hovered = visible_rect.collidepoint(mouse_pos)
        image = weapon.weapon_cards[1 if hovered else 0]
        image_rect = image.get_rect(center=rect.center)
        self.weapon_rects[weapon] = visible_rect
        surface.blit(image, image_rect)

        button = self.equip_buttons.get(weapon)
        if button is not None:
            button_x = visible_rect.centerx // 2 + 5
            button_y = visible_rect.centery + 33
            button.set_position(button_x, button_y)
            button.update(mouse_pos)
            button.draw(surface)

        if hovered:
            self.hovered_tooltip = (stats, mouse_pos)

    def _draw_stats_tooltip(self, surface, stats, mouse_pos):
        lines = [
            f"{label.replace('_', ' ').title()}: {value}"
            for label, value in stats.items()
        ]
        padding = 10
        line_height = self.font_letters.get_linesize()
        width = max(
            self.font_letters.size(line)[0] for line in lines
        ) + padding * 2
        height = line_height * len(lines) + padding * 2
        x, y = mouse_pos[0] + 16, mouse_pos[1] + 16
        if x + width > surface.get_width():
            x = mouse_pos[0] - width - 16
        if y + height > surface.get_height():
            y = mouse_pos[1] - height - 16

        tooltip = pygame.Surface((width, height), pygame.SRCALPHA)
        tooltip.fill((20, 20, 20, 235))
        pygame.draw.rect(tooltip, UI_COLOR, tooltip.get_rect(), 2)
        for index, line in enumerate(lines):
            image = self.font_letters.render(line, True, UI_COLOR)
            tooltip.blit(image, (padding, padding + index * line_height))
        surface.blit(tooltip, (x, y))

    def _create_equip_buttons(self):
        equipped_weapons = {
            self.player.weapons_inventory["gun"],
            self.player.weapons_inventory["melee"],
        }
        self.equip_buttons = {
            weapon: MenuButton("equip", 0, 0, ("equip", weapon), scale=2)
            for weapon in self.current_guns + self.current_melees
            if weapon not in equipped_weapons
        }

    def draw(self, surface):
        self.get_weapons()
        equipped_weapons = {
            self.player.weapons_inventory["gun"],
            self.player.weapons_inventory["melee"],
        }
        expected_buttons = (
            set(self.current_guns + self.current_melees) - equipped_weapons
        )
        if set(self.equip_buttons) != expected_buttons:
            self._create_equip_buttons()

        surface.fill(STASH_BG_COLOR)
        self.weapon_rects = {}
        self.hovered_tooltip = None
        self._draw_centered_text(
            surface,
            "Stash",
            self.font_headers,
            (surface.get_width() // 2, 45),
        )
        self._draw_centered_text(
            surface,
            "Guns",
            self.font_headers,
            (60, 105),
        )
        self._draw_centered_text(
            surface,
            "Melees",
            self.font_headers,
            (62, 350),
        )

        self._draw_weapon_row(
            surface,
            self.current_guns,
            190,
            self.get_gun_stats,
        )
        self._draw_weapon_row(
            surface,
            self.current_melees,
            460,
            self.get_melee_stats,
        )

        self.back_button.set_position(
            surface.get_width() - self.back_button.rect.width - 24,
            surface.get_height() - self.back_button.rect.height - 24,
        )
        self.back_button.update(pygame.mouse.get_pos())
        self.back_button.draw(surface)
        if self.hovered_tooltip is not None:
            stats, mouse_pos = self.hovered_tooltip
            self._draw_stats_tooltip(surface, stats, mouse_pos)

    def _draw_weapon_row(self, surface, weapons, y, stats_getter):
        if not weapons:
            return
        card_width = weapons[0].weapon_cards[0].get_width()
        gap = min(24, (surface.get_width() - len(weapons) * card_width) // (len(weapons) + 1))
        for index, weapon in enumerate(weapons):
            x = gap + card_width // 2 + index * (card_width + gap)
            rect = weapons[index].weapon_cards[0].get_rect(center=(x, y))
            self._draw_weapon(surface, weapon, rect, stats_getter(weapon))

    def handle_click(self, mouse_pos):
        if self.back_button.clicked(mouse_pos) == "back":
            return "back"

        for weapon, button in self.equip_buttons.items():
            action = button.clicked(mouse_pos)
            if action and action[0] == "equip":
                self.player.weapon_swap(action[1])
                if self.player.weapon_equipped and self.player.weapon_equipped.weapon_type == weapon.weapon_type:
                    self.player.equip_weapon(weapon)
                return "equipped"
        return None

    def get_gun_stats(self, gun):
        gun_stats = {
            "name": gun.name.capitalize(),
            "damage": gun.damage,
            "mag_size": gun.ammo_limit,
            "crit_chance": gun.crit_chance,
            "crit_multiplier": gun.crit_multiplier,
        }
        return gun_stats

    def get_melee_stats(self, melee):
        melee_stats = {
            "name": melee.name.capitalize(),
            "damage": melee.damage,
            "melee_range": melee.melee_range,
            "crit_chance": melee.crit_chance,
            "crit_multiplier": melee.crit_multiplier,
        }
        return melee_stats
    