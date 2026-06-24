from src.game import triple_card_selector
from src.constants import UI_COLOR

def _draw_wrapped_desc(screen, font, text, center_x, start_y, max_width, screen_h):
    words = text.split(' ')
    lines = []
    current_line = []
    for word in words:
        test = ' '.join(current_line + [word])
        if font.size(test)[0] <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
            current_line = [word]
    if current_line:
        lines.append(' '.join(current_line))

    line_h = font.get_linesize()
    y = min(start_y, screen_h - len(lines) * line_h - 10)

    for i, line in enumerate(lines):
        surf = font.render(line, True, UI_COLOR)
        screen.blit(surf, (center_x - surf.get_width() // 2, y + i * line_h))

def initialize_upgrade_selection(card_lists):
    # Create a combined list of all cards for random selection
    all_cards = []
    for card_list in card_lists:
        all_cards.extend(card_list)

    # Randomly select 3 cards using the triple selector
    selected_cards = triple_card_selector(all_cards.copy())

    # Reset animation states for selected cards
    for card in selected_cards:
        card.animation_index = 0
        card.animation_tick = 0

    return selected_cards

def update_upgrade_card_weapons(card_list, new_weapon):
    for i in range(len(card_list)):
        card_list[i].update_weapon(new_weapon)

def update_and_draw_upgrade_cards(screen, selected_cards, mouse_pos):
    w, h = screen.get_width(), screen.get_height()
    card_width = selected_cards[0].images[0].get_width()
    card_height = selected_cards[0].images[0].get_height()
    total_cards_width = card_width * 3
    gap = (w - total_cards_width) // 4  # 4 gaps: left, between, between, right

    for i, card in enumerate(selected_cards):
        card.rect.topleft = (gap * (i + 1) + card_width * i, (h - card_height) // 2)
        current_image = card.update(mouse_pos)
        screen.blit(current_image, card.rect)
        if card.is_hovering:
            _draw_wrapped_desc(screen, card.font_letters, card.text, w // 2, card.rect.bottom + 30, w - 80, h)


def handle_card_click(selected_cards, mouse_pos):
    for card in selected_cards:
        # Use collision_rect for tighter click detection
        if card.collision_rect.collidepoint(mouse_pos):
            # Check if it's a weapon unlock card, power-up card, or a regular upgrade card
            if hasattr(card, 'unlock_weapon'):
                card.unlock_weapon()
            elif hasattr(card, 'unlock_powerup'):
                card.unlock_powerup()
            else:
                card.apply_upgrade()
            return True
    return False
