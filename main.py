import pygame
import random
from start_menu import StartMenu
from character_select import CharacterSelect
from dice_select import DiceSelect
from yellow_tile_select import YellowTileSelect
from battle_renderer import BattleRenderer
from board import generate_board_positions, generate_green_tiles, generate_red_tiles
from characters import Lapper, Huntsman, DICE_LIBRARY
from ui_constants import colors, fonts, BLUE, DARK_BLUE, PURPLE, DARK_PURPLE, ORANGE, DARK_ORANGE

# ===== INITIALIZATION =====
pygame.init()

# ===== CONSTANTS =====
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800

# Board settings
SQUARE_SIZE = 100
BOARD_MARGIN = 50

# Game settings
LAP_BONUS_DAMAGE = 10
NUM_GREEN_TILES = 5
NUM_RED_TILES = 8
DEBUFF_DAMAGE = 5
GREEN_TILE_HEAL = 20
BOSS_MAX_HP = 350
BOSS_INITIAL_DAMAGE = 10
BOSS_DAMAGE_INCREMENT = 1
POISON_STACKS_APPLIED = 3

# ===== WINDOW SETUP =====
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Monopoly Dice Game")
clock = pygame.time.Clock()

# ===== CONSTANTS DICTIONARY =====
constants = {
    'SQUARE_SIZE': SQUARE_SIZE,
    'BOARD_MARGIN': BOARD_MARGIN
}

# ===== BOARD SETUP =====
board_positions = generate_board_positions(SQUARE_SIZE, BOARD_MARGIN, WINDOW_HEIGHT)

# ===== AVAILABLE CHARACTERS =====
available_characters = [Lapper(), Huntsman()]


# ===== HELPER FUNCTIONS =====
def get_tile_at_position(mouse_pos):
    """
    Get the tile number at a given mouse position

    Args:
        mouse_pos: Tuple of (x, y) mouse position

    Returns:
        Tile number (1-24) if clicking on a tile, None otherwise
    """
    for i, (x, y) in enumerate(board_positions):
        tile_rect = pygame.Rect(x, y, SQUARE_SIZE, SQUARE_SIZE)
        if tile_rect.collidepoint(mouse_pos):
            return i + 1  # Tiles are 1-indexed
    return None


def get_possible_landing_tiles(dice_index):
    """Get list of possible tile numbers player can land on for a given dice"""
    if dice_index is None:
        return []

    possible_tiles = []
    # Get unique values from the dice set
    unique_rolls = list(set(dice_options[dice_index]))
    for option in unique_rolls:
        # Apply double movement if yellow buff is active
        movement = option * 2 if yellow_buff_active else option
        landing_position = player_position + movement

        # Handle wrapping around the board
        while landing_position > 24:
            landing_position -= 24

        possible_tiles.append(landing_position)
    return possible_tiles


def reset_game():
    """Reset game state for a new battle"""
    global player_position, is_moving, move_counter, moves_remaining
    global player_current_hp, boss_current_hp, laps_completed, dice_values
    global green_tiles, red_tiles, yellow_tiles, landed_on_green, debuff_stacks
    global boss_attack_count, boss_current_damage, battle_phase, yellow_buff_active
    global dice_labels, dice_options, yellow_tiles_to_place, yellow_tiles_placed
    global boss_poison_stacks

    player_position = 1
    is_moving = False
    move_counter = 0
    moves_remaining = 0
    player_current_hp = current_character.max_hp
    boss_current_hp = BOSS_MAX_HP
    laps_completed = 0
    dice_values = [3, 5, 3]
    landed_on_green = False
    debuff_stacks = 0
    boss_attack_count = 0
    boss_current_damage = BOSS_INITIAL_DAMAGE
    battle_phase = "place_yellow"  # Start in yellow placement phase
    yellow_tiles = []  # Will be populated as player places them
    yellow_buff_active = False  # Track if yellow tile buff is active
    yellow_tiles_to_place = current_character.num_yellow_tiles
    yellow_tiles_placed = 0
    boss_poison_stacks = 0  # Track poison stacks on boss

    # Update dice based on selected character
    dice_labels = current_character.dice_labels
    dice_options = current_character.dice_sets

    # Generate random green tiles first (no restrictions)
    green_tiles = generate_green_tiles(NUM_GREEN_TILES, [])

    # Generate random red tiles (2 per side, excluding green tiles)
    red_tiles = generate_red_tiles(NUM_RED_TILES, green_tiles)


# ===== GAME STATE =====
# Game screen state
game_state = "start"  # Can be "start", "character_select", "dice_select", "yellow_tile_select", or "battle"
battle_phase = "place_yellow"  # Can be "place_yellow" or "rolling"

# Initialize UI components
start_menu = StartMenu(WINDOW_WIDTH, WINDOW_HEIGHT, colors, fonts)
character_select = CharacterSelect(WINDOW_WIDTH, WINDOW_HEIGHT, colors, fonts, available_characters)
dice_select = None  # Will be initialized after character selection
yellow_tile_select = None  # Will be initialized after dice selection
battle_renderer = BattleRenderer(WINDOW_WIDTH, WINDOW_HEIGHT, colors, fonts, constants)

# Select character (will be set in character select screen)
current_character = None

# Three dice with character-specific options
dice_values = [3, 5, 3]
dice_rects = [
    pygame.Rect(WINDOW_WIDTH // 2 - 170, WINDOW_HEIGHT // 2, 100, 100),  # Left dice
    pygame.Rect(WINDOW_WIDTH // 2 - 50, WINDOW_HEIGHT // 2, 100, 100),  # Middle dice
    pygame.Rect(WINDOW_WIDTH // 2 + 70, WINDOW_HEIGHT // 2, 100, 100)  # Right dice
]
dice_colors = [(BLUE, DARK_BLUE), (PURPLE, DARK_PURPLE), (ORANGE, DARK_ORANGE)]
dice_labels = []
dice_options = []

player_position = 1  # Start at square 1
is_moving = False
move_counter = 0
moves_remaining = 0
player_max_hp = 100
player_current_hp = 100
boss_max_hp = BOSS_MAX_HP
boss_current_hp = BOSS_MAX_HP
hovered_dice = None  # Track which dice is being hovered over
laps_completed = 0  # Track number of laps
green_tiles = []  # Will be populated when game starts
red_tiles = []  # Boss tiles that debuff player
yellow_tiles = []  # Player's special tiles
yellow_tiles_to_place = 1  # Number of yellow tiles to place
yellow_tiles_placed = 0  # Number of yellow tiles already placed
landed_on_green = False  # Track if current landing is on green tile
debuff_stacks = 0  # Track number of debuff stacks (each stack = 5 damage per turn)
boss_attack_count = 0  # Track number of boss attacks
boss_current_damage = BOSS_INITIAL_DAMAGE  # Current boss damage
yellow_buff_active = False  # Track if yellow tile buff is active (double movement next roll)
boss_poison_stacks = 0  # Track poison stacks on boss

# ===== MAIN GAME LOOP =====
running = True

while running:
    # ===== EVENT HANDLING =====
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_state == "start":
                # Check if start button clicked
                if start_menu.handle_click(event.pos):
                    game_state = "character_select"

            elif game_state == "character_select":
                # Check if character was selected
                selected_character = character_select.handle_click(event.pos)
                if selected_character is not None:
                    # Create a new instance of the selected character class
                    if selected_character.name == "Lapper":
                        current_character = Lapper()
                    elif selected_character.name == "Huntsman":
                        current_character = Huntsman()

                    player_max_hp = current_character.max_hp
                    player_current_hp = current_character.max_hp
                    # Initialize dice select screen with chosen character
                    dice_select = DiceSelect(WINDOW_WIDTH, WINDOW_HEIGHT, colors, fonts, current_character)
                    game_state = "dice_select"

            elif game_state == "dice_select":
                # Check if dice selection was confirmed
                selected_dice_keys = dice_select.handle_click(event.pos)
                if selected_dice_keys is not None:
                    # Update character's dice based on selection
                    current_character.dice_sets = []
                    current_character.dice_labels = []

                    for dice_key in selected_dice_keys:
                        dice_data = DICE_LIBRARY[dice_key]
                        current_character.dice_sets.append(dice_data['values'])
                        current_character.dice_labels.append(dice_data['label'])

                    # Initialize yellow tile select screen
                    yellow_tile_select = YellowTileSelect(WINDOW_WIDTH, WINDOW_HEIGHT, colors, fonts, current_character)
                    game_state = "yellow_tile_select"

            elif game_state == "yellow_tile_select":
                # Check if yellow tile option was selected
                selected_option = yellow_tile_select.handle_click(event.pos)
                if selected_option is not None:
                    # Set the character's yellow tile effect and number of tiles
                    current_character.set_yellow_effect(selected_option['effect'], selected_option['icon'])
                    current_character.num_yellow_tiles = selected_option['num_tiles']
                    reset_game()
                    game_state = "battle"

            elif game_state == "battle":
                if battle_phase == "place_yellow":
                    # Player is placing yellow tiles
                    clicked_tile = get_tile_at_position(event.pos)
                    if clicked_tile is not None:
                        # Check if tile is empty (not green, red, or already yellow)
                        if (clicked_tile not in green_tiles and
                                clicked_tile not in red_tiles and
                                clicked_tile not in yellow_tiles):
                            yellow_tiles.append(clicked_tile)
                            yellow_tiles_placed += 1

                            # Check if all yellow tiles have been placed
                            if yellow_tiles_placed >= yellow_tiles_to_place:
                                battle_phase = "rolling"  # Move to rolling phase

                elif battle_phase == "rolling" and not is_moving:
                    # Check which dice was clicked
                    for i, rect in enumerate(dice_rects):
                        if rect.collidepoint(event.pos):
                            dice_values[i] = random.choice(dice_options[i])
                            # Apply double movement if yellow buff is active
                            moves_remaining = dice_values[i] * 2 if yellow_buff_active else dice_values[i]
                            is_moving = True
                            landed_on_green = False  # Reset flag

                            # Consume the yellow buff after using it
                            if yellow_buff_active:
                                yellow_buff_active = False

                            # Apply debuff damage before rolling if debuffed
                            if debuff_stacks > 0:
                                player_current_hp -= DEBUFF_DAMAGE * debuff_stacks

                            # Apply poison damage to boss and tick down stacks
                            if boss_poison_stacks > 0:
                                boss_current_hp -= boss_poison_stacks
                                boss_poison_stacks -= 1

                            break

    # Check for mouse hover over dice (only in battle rolling phase)
    if game_state == "battle" and battle_phase == "rolling":
        mouse_pos = pygame.mouse.get_pos()
        hovered_dice = None
        if not is_moving:
            for i, rect in enumerate(dice_rects):
                if rect.collidepoint(mouse_pos):
                    hovered_dice = i
                    break

    # ===== GAME LOGIC =====
    if game_state == "battle" and battle_phase == "rolling":
        # Animate player movement
        if is_moving:
            move_counter += 1
            if move_counter >= 10:  # Move every 10 frames
                move_counter = 0
                old_position = player_position

                # Determine direction of movement
                if moves_remaining > 0:
                    player_position += 1
                    moves_remaining -= 1
                elif moves_remaining < 0:
                    player_position -= 1
                    moves_remaining += 1

                # Check if completed a lap (going forward past 24)
                if old_position == 24 and player_position > 24:
                    laps_completed += 1
                    # Use character's lap damage calculation
                    lap_damage = current_character.get_lap_damage(laps_completed)
                    boss_current_hp -= lap_damage

                # Handle wrapping around the board
                if player_position > 24:
                    player_position = 1
                elif player_position < 1:
                    player_position = 24

                # Check if movement is complete
                if moves_remaining == 0:
                    is_moving = False

                    # Check what type of tile player landed on
                    if player_position in green_tiles:
                        # Heal player for fixed amount and remove all debuff stacks
                        player_current_hp = min(player_max_hp, player_current_hp + GREEN_TILE_HEAL)
                        landed_on_green = True
                        debuff_stacks = 0  # Clears all stacks
                    elif player_position in red_tiles:
                        # Add a debuff stack - NO damage to or from boss
                        debuff_stacks += 1
                    elif player_position in yellow_tiles:
                        # Yellow tile - apply character-specific effect
                        effect = current_character.yellow_tile_effect()
                        if effect == "double_movement":
                            yellow_buff_active = True
                        elif effect == "damage_30_poison_3":
                            # Deal 30 damage immediately
                            boss_current_hp -= 30
                            # Add 3 poison stacks and deal immediate poison damage
                            boss_poison_stacks += POISON_STACKS_APPLIED
                            boss_current_hp -= boss_poison_stacks
                    else:
                        # Normal tile - damage boss using character's base damage and take boss damage
                        boss_current_hp -= current_character.base_damage
                        player_current_hp -= boss_current_damage
                        boss_attack_count += 1
                        boss_current_damage = BOSS_INITIAL_DAMAGE + (boss_attack_count * BOSS_DAMAGE_INCREMENT)

    # ===== DRAWING =====
    if game_state == "start":
        start_menu.draw(screen)
    elif game_state == "character_select":
        character_select.draw(screen)
    elif game_state == "dice_select":
        dice_select.draw(screen)
    elif game_state == "yellow_tile_select":
        yellow_tile_select.draw(screen)
    elif game_state == "battle":
        # Package game state into dictionary for renderer
        game_state_dict = {
            'board_positions': board_positions,
            'green_tiles': green_tiles,
            'red_tiles': red_tiles,
            'yellow_tiles': yellow_tiles,
            'highlighted_tiles': get_possible_landing_tiles(hovered_dice) if battle_phase == "rolling" else [],
            'player_position': player_position,
            'player_current_hp': player_current_hp,
            'player_max_hp': player_max_hp,
            'boss_current_hp': boss_current_hp,
            'boss_max_hp': boss_max_hp,
            'dice_rects': dice_rects,
            'dice_colors': dice_colors,
            'dice_values': dice_values,
            'dice_labels': dice_labels,
            'character': current_character,
            'laps_completed': laps_completed,
            'is_moving': is_moving,
            'debuff_stacks': debuff_stacks,
            'battle_phase': battle_phase,
            'yellow_buff_active': yellow_buff_active,
            'boss_current_damage': boss_current_damage,
            'yellow_tiles_to_place': yellow_tiles_to_place,
            'yellow_tiles_placed': yellow_tiles_placed,
            'boss_poison_stacks': boss_poison_stacks
        }
        battle_renderer.draw_battle_screen(screen, game_state_dict)

    # ===== UPDATE DISPLAY =====
    pygame.display.flip()
    clock.tick(60)

# ===== CLEANUP =====
pygame.quit()