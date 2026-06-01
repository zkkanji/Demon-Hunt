from src.game import triple_card_selector
from src.constants import WIDTH, HEIGHT


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
    
    # Calculate card positions (horizontal, equidistant spacing)
    card_width = selected_cards[0].images[0].get_width()
    card_height = selected_cards[0].images[0].get_height()
    
    # Total width needed for all cards
    total_cards_width = card_width * 3
    # Calculate gap between cards to center them
    gap_between_cards = (WIDTH - total_cards_width) // 4  # 4 gaps (left, between, between, right)
    
    # Position cards
    for i in range(3):
        x = gap_between_cards * (i + 1) + card_width * i
        y = (HEIGHT - card_height) // 2
        selected_cards[i].rect.topleft = (x, y)
    
    return selected_cards


def update_and_draw_upgrade_cards(screen, selected_cards, mouse_pos):
    for card in selected_cards:
        current_image = card.update(mouse_pos)
        screen.blit(current_image, card.rect)


def handle_card_click(selected_cards, mouse_pos):
    for card in selected_cards:
        # Use collision_rect for tighter click detection
        if card.collision_rect.collidepoint(mouse_pos):
            # Check if it's a weapon unlock card or a regular upgrade card
            if hasattr(card, 'unlock_weapon'):
                card.unlock_weapon()
            else:
                card.apply_upgrade()
            return True
    return False
