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
from campaign_team_select import CampaignTeamSelect
from campaign_dice_select import CampaignDiceSelect

# ===== INITIALIZATION =====
pygame.init()
#Test
# ===== CONSTANTS =====
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 900

# Board settings
SQUARE_SIZE = 100
BOARD_MARGIN = 50

# Board offset to position it
BOARD_OFFSET_X = 200
BOARD_OFFSET_Y = 50

# Game settings
LAP_BONUS_DAMAGE = 10
NUM_GREEN_TILES = 5
NUM_RED_TILES = 8
DEBUFF_DAMAGE = 5
GREEN_TILE_HEAL = 20
BOSS_MAX_HP = 350
BOSS_INITIAL_DAMAGE = 10
BOSS_DAMAGE_INCREMENT = 1
POISON_STACKS_APPLIED = 5
BURN_DAMAGE_PER_STACK = 3
CHAIN_LIGHTNING_INITIAL_DAMAGE = 20
CHAIN_LIGHTNING_DOT_DAMAGE = 10

# ===== WINDOW SETUP =====
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Monopoly Dice Game")
clock = pygame.time.Clock()

# ===== CONSTANTS DICTIONARY =====
constants = {
    'SQUARE_SIZE': SQUARE_SIZE,
    'BOARD_MARGIN': BOARD_MARGIN,
    'BOARD_OFFSET_X': BOARD_OFFSET_X,
    'BOARD_OFFSET_Y': BOARD_OFFSET_Y
}

# ===== BOARD SETUP =====
board_positions = generate_board_positions(SQUARE_SIZE, BOARD_MARGIN, WINDOW_HEIGHT, BOARD_OFFSET_X, BOARD_OFFSET_Y)


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
        while landing_position < 1:
            landing_position += 24

        possible_tiles.append(landing_position)
    return possible_tiles


def reset_game():
    """Reset game state for a new battle"""
    global player_position, is_moving, move_counter, moves_remaining
    global player_current_hp, boss_current_hp, laps_completed, dice_values
    global green_tiles, red_tiles, yellow_tiles, landed_on_green, debuff_stacks
    global boss_attack_count, boss_current_damage, battle_phase, yellow_buff_active
    global dice_labels, dice_options, yellow_tiles_to_place, yellow_tiles_placed
    global boss_poison_stacks, current_dice_damage
    global boss_burn_stacks, lifesteal_active, chain_lightning_stacks

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
    current_dice_damage = 15  # Track damage from current dice roll
    boss_burn_stacks = 0  # Track burn stacks on boss
    lifesteal_active = False  # Track if lifesteal is active
    chain_lightning_stacks = 0  # Track chain lightning turns remaining

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
# Campaign mode tracking
campaign_mode = False  # True when using campaign flow

battle_phase = "place_yellow"  # Can be "place_yellow" or "rolling"

# Initialize UI components
start_menu = StartMenu(WINDOW_WIDTH, WINDOW_HEIGHT, colors, fonts)
character_select = CharacterSelect(WINDOW_WIDTH, WINDOW_HEIGHT, colors, fonts, available_characters)
campaign_team_select = CampaignTeamSelect(WINDOW_WIDTH, WINDOW_HEIGHT, colors, fonts, available_characters)
dice_select = None  # Will be initialized after character selection
yellow_tile_select = None  # Will be initialized after dice selection
battle_renderer = BattleRenderer(WINDOW_WIDTH, WINDOW_HEIGHT, colors, fonts, constants)

# Select character (will be set in character select screen)
current_character = None

# Campaign mode variables
campaign_character_1 = None
campaign_character_2 = None
campaign_dice_select = None
# Campaign mode 2-character state
character_1_state = None
character_2_state = None
turn_phase = "choose_first"
yellow_tile_effects = {}  # Maps tile number to effect name
last_character_to_move = None  # Track which character moved second for boss targeting

# Calculate dice positions to match rendering
board_center_x = 200 + 50 + (7 * 100) // 2
board_center_y = 50 + 50 + (7 * 100) // 2
dice_start_x = board_center_x - 180
dice_y = board_center_y + 40

# Three dice with character-specific options
dice_values = [3, 5, 3]
dice_rects = [
    pygame.Rect(dice_start_x, dice_y, 100, 100),  # Left dice
    pygame.Rect(dice_start_x + 120, dice_y, 100, 100),  # Middle dice
    pygame.Rect(dice_start_x + 240, dice_y, 100, 100)  # Right dice
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
current_dice_damage = 15  # Track damage from current dice roll
boss_burn_stacks = 0  # Track burn stacks on boss (doesn't decay)
lifesteal_active = False  # Track if lifesteal is active (next hit heals)
chain_lightning_stacks = 0  # Track chain lightning turns remaining


def initialize_campaign_battle():
    """Initialize battle state for campaign mode (2 characters)"""
    global player_position, is_moving, move_counter, moves_remaining
    global player_current_hp, boss_current_hp, laps_completed, dice_values
    global green_tiles, red_tiles, yellow_tiles, landed_on_green, debuff_stacks
    global boss_attack_count, boss_current_damage, battle_phase, yellow_buff_active
    global dice_labels, dice_options, yellow_tiles_to_place, yellow_tiles_placed
    global boss_poison_stacks, current_dice_damage
    global boss_burn_stacks, lifesteal_active, chain_lightning_stacks
    global campaign_mode, character_1_state, character_2_state, turn_phase
    global last_character_to_move

    campaign_mode = True

    # Initialize character 1 state
    character_1_state = {
        'character_obj': campaign_character_1,
        'position': 1,
        'current_hp': campaign_character_1.max_hp,
        'max_hp': campaign_character_1.max_hp,
        'is_moving': False,
        'move_counter': 0,
        'moves_remaining': 0,
        'laps_completed': 0,
        'dice_values': [3, 5, 3],
        'dice_labels': campaign_character_1.dice_labels,
        'dice_options': campaign_character_1.dice_sets,
        'dice_damage': campaign_character_1.dice_damage,
        'yellow_buff_active': False,
        'debuff_stacks': 0
    }

    # Initialize character 2 state
    character_2_state = {
        'character_obj': campaign_character_2,
        'position': 1,
        'current_hp': campaign_character_2.max_hp,
        'max_hp': campaign_character_2.max_hp,
        'is_moving': False,
        'move_counter': 0,
        'moves_remaining': 0,
        'laps_completed': 0,
        'dice_values': [3, 5, 3],
        'dice_labels': campaign_character_2.dice_labels,
        'dice_options': campaign_character_2.dice_sets,
        'dice_damage': campaign_character_2.dice_damage,
        'yellow_buff_active': False,
        'debuff_stacks': 0
    }

    # Boss state
    boss_current_hp = BOSS_MAX_HP
    boss_current_damage = BOSS_INITIAL_DAMAGE
    boss_attack_count = 0
    boss_poison_stacks = 0
    boss_burn_stacks = 0
    chain_lightning_stacks = 0

    # Turn tracking
    turn_phase = "choose_first"  # "choose_first", "character_1_second", "character_2_second", "boss_attack"

    # Yellow tile placement phase
    battle_phase = "place_yellow"
    yellow_tiles = []
    yellow_tiles_to_place = campaign_character_1.num_yellow_tiles + campaign_character_2.num_yellow_tiles
    yellow_tiles_placed = 0

    # Yellow tile effect tracking (which tile has which effect)
    yellow_tile_effects = {}  # Will map tile_number -> effect_name

    # Generate board tiles
    green_tiles = generate_green_tiles(NUM_GREEN_TILES, [])
    red_tiles = generate_red_tiles(NUM_RED_TILES, green_tiles)


def get_campaign_dice_click(mouse_pos, character_1_state, character_2_state):
    """
    Determine which character's dice was clicked in campaign mode

    Returns:
        Tuple of (character_index, dice_index) or None
        character_index: 0 for char 1, 1 for char 2
        dice_index: 0, 1, or 2 for which dice
    """
    board_center_x = 200 + 50 + (7 * 100) // 2
    board_center_y = 50 + 50 + (7 * 100) // 2
    dice_y = board_center_y + 40

    # Character 1 dice positions (left)
    char_1_start_x = board_center_x - 400
    for i in range(3):
        x = char_1_start_x + (i * 120)
        rect = pygame.Rect(x, dice_y, 100, 100)
        if rect.collidepoint(mouse_pos):
            return (0, i)  # Character 1, dice i

    # Character 2 dice positions (right)
    char_2_start_x = board_center_x + 40
    for i in range(3):
        x = char_2_start_x + (i * 120)
        rect = pygame.Rect(x, dice_y, 100, 100)
        if rect.collidepoint(mouse_pos):
            return (1, i)  # Character 2, dice i

    return None

# ===== MAIN GAME LOOP =====
running = True

while running:
    # ===== EVENT HANDLING =====
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_state == "start":
                # Check which button was clicked
                button_result = start_menu.handle_click(event.pos)
                if button_result == 'start':
                    game_state = "character_select"  # Old flow
                elif button_result == 'campaign':
                    game_state = "campaign_team_select"  # New flow

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

            elif game_state == "campaign_team_select":
                # Check if team was selected
                selected_team = campaign_team_select.handle_click(event.pos)
                if selected_team is not None:
                    campaign_character_1, campaign_character_2 = selected_team
                    # Create new instances of the characters
                    if campaign_character_1.name == "Lapper":
                        campaign_character_1 = Lapper()
                    elif campaign_character_1.name == "Huntsman":
                        campaign_character_1 = Huntsman()
                    if campaign_character_2.name == "Lapper":
                        campaign_character_2 = Lapper()
                    elif campaign_character_2.name == "Huntsman":
                        campaign_character_2 = Huntsman()

                    # Initialize campaign dice select screen

                    campaign_dice_select = CampaignDiceSelect(WINDOW_WIDTH, WINDOW_HEIGHT, colors, fonts,

                                                              campaign_character_1, campaign_character_2)
                    game_state = "campaign_dice_select"

            elif game_state == "campaign_dice_select":
                # Check if dice were selected
                selected_dice = campaign_dice_select.handle_click(event.pos)
                if selected_dice is not None:
                    char_1_dice_keys, char_2_dice_keys = selected_dice

                    # Set dice for character 1
                    campaign_character_1.dice_sets = []
                    campaign_character_1.dice_labels = []
                    campaign_character_1.dice_damage = []
                    for dice_key in char_1_dice_keys:
                        dice_data = DICE_LIBRARY[dice_key]
                        campaign_character_1.dice_sets.append(dice_data['values'])
                        campaign_character_1.dice_labels.append(dice_data['label'])
                        campaign_character_1.dice_damage.append(dice_data['damage'])

                    # Set dice for character 2
                    campaign_character_2.dice_sets = []
                    campaign_character_2.dice_labels = []
                    campaign_character_2.dice_damage = []
                    for dice_key in char_2_dice_keys:
                        dice_data = DICE_LIBRARY[dice_key]
                        campaign_character_2.dice_sets.append(dice_data['values'])
                        campaign_character_2.dice_labels.append(dice_data['label'])
                        campaign_character_2.dice_damage.append(dice_data['damage'])

                    # Set yellow tile effects based on character
                    if campaign_character_1.name == "Lapper":
                        campaign_character_1.set_yellow_effect('double_movement', 'lightning.png')
                        campaign_character_1.num_yellow_tiles = 1
                    elif campaign_character_1.name == "Huntsman":
                        campaign_character_1.set_yellow_effect('poison_5', 'poison.png')
                        campaign_character_1.num_yellow_tiles = 4

                    if campaign_character_2.name == "Lapper":
                        campaign_character_2.set_yellow_effect('double_movement', 'lightning.png')
                        campaign_character_2.num_yellow_tiles = 1
                    elif campaign_character_2.name == "Huntsman":
                        campaign_character_2.set_yellow_effect('poison_5', 'poison.png')
                        campaign_character_2.num_yellow_tiles = 4

                    # Initialize campaign battle
                    initialize_campaign_battle()
                    game_state = "battle"  # Placeholder for now

            elif game_state == "dice_select":
                # Check if dice selection was confirmed
                selected_dice_keys = dice_select.handle_click(event.pos)
                if selected_dice_keys is not None:
                    # Update character's dice based on selection
                    current_character.dice_sets = []
                    current_character.dice_labels = []
                    current_character.dice_damage = []

                    for dice_key in selected_dice_keys:
                        dice_data = DICE_LIBRARY[dice_key]
                        current_character.dice_sets.append(dice_data['values'])
                        current_character.dice_labels.append(dice_data['label'])
                        current_character.dice_damage.append(dice_data['damage'])

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
                            # Determine which character's tile this is based on placement order
                            if campaign_mode:
                                # Track effect based on character tile counts
                                if yellow_tiles_placed < campaign_character_1.num_yellow_tiles:
                                    # This is character 1's tile
                                    effect = campaign_character_1.yellow_tile_effect()
                                    yellow_tile_effects[clicked_tile] = effect
                                else:
                                    # This is character 2's tile
                                    effect = campaign_character_2.yellow_tile_effect()
                                    yellow_tile_effects[clicked_tile] = effect

                            yellow_tiles_placed += 1

                            # Check if all yellow tiles have been placed

                            if yellow_tiles_placed >= yellow_tiles_to_place:
                                battle_phase = "rolling"  # Move to rolling phase


                elif battle_phase == "rolling":

                    if campaign_mode:
                        # Campaign mode dice clicking
                        dice_click = get_campaign_dice_click(event.pos, character_1_state, character_2_state)

                        if dice_click is not None:
                            char_index, dice_index = dice_click

                            # Don't allow clicking dice for dead characters
                            if char_index == 0 and character_1_state['current_hp'] <= 0:
                                continue  # Character 1 is dead, ignore click
                            if char_index == 1 and character_2_state['current_hp'] <= 0:
                                continue  # Character 2 is dead, ignore click

                            # Check if this is a valid click based on turn phase
                            if turn_phase == "choose_first":
                                # Any character can go first
                                if char_index == 0:
                                    # Character 1 goes first
                                    active_character = character_1_state
                                    turn_phase = "character_2_second"
                                else:
                                    # Character 2 goes first
                                    active_character = character_2_state
                                    turn_phase = "character_1_second"
                                # Roll the dice
                                active_character['dice_values'][dice_index] = random.choice(
                                    active_character['dice_options'][dice_index])

                                active_character['moves_remaining'] = active_character['dice_values'][dice_index]

                                active_character['is_moving'] = True

                            elif turn_phase == "character_1_second" and char_index == 0:
                                # Character 1 must go second
                                active_character = character_1_state
                                last_character_to_move = character_1_state  # ADD THIS LINE
                                # Roll the dice
                                active_character['dice_values'][dice_index] = random.choice(
                                    active_character['dice_options'][dice_index])
                                active_character['moves_remaining'] = active_character['dice_values'][dice_index]
                                active_character['is_moving'] = True
                                turn_phase = "boss_attack"


                            elif turn_phase == "character_2_second" and char_index == 1:
                                # Character 2 must go second
                                active_character = character_2_state
                                last_character_to_move = character_2_state  # ADD THIS LINE
                                # Roll the dice
                                active_character['dice_values'][dice_index] = random.choice(
                                    active_character['dice_options'][dice_index])

                                active_character['moves_remaining'] = active_character['dice_values'][dice_index]
                                active_character['is_moving'] = True
                                turn_phase = "boss_attack"


                    elif not is_moving:
                        # Single player mode (old code)
                        for i, rect in enumerate(dice_rects):
                            if rect.collidepoint(event.pos):
                                dice_values[i] = random.choice(dice_options[i])
                                moves_remaining = dice_values[i] * 2 if yellow_buff_active else dice_values[i]
                                is_moving = True
                                landed_on_green = False
                                current_dice_damage = current_character.dice_damage[i]

                                if yellow_buff_active:
                                    yellow_buff_active = False

                                if debuff_stacks > 0:
                                    player_current_hp -= DEBUFF_DAMAGE * debuff_stacks

                                if boss_poison_stacks > 0:
                                    boss_current_hp -= boss_poison_stacks

                                    boss_poison_stacks -= 1

                                if boss_burn_stacks > 0:
                                    burn_damage = boss_burn_stacks * BURN_DAMAGE_PER_STACK

                                    boss_current_hp -= burn_damage

                                if chain_lightning_stacks > 0:
                                    boss_current_hp -= CHAIN_LIGHTNING_DOT_DAMAGE

                                    chain_lightning_stacks -= 1

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
            if campaign_mode:
                # Campaign mode movement
                # Check if character 1 is moving
                if character_1_state['is_moving']:
                    character_1_state['move_counter'] += 1
                    if character_1_state['move_counter'] >= 10:
                        character_1_state['move_counter'] = 0
                        old_position = character_1_state['position']

                        # Move
                        if character_1_state['moves_remaining'] > 0:
                            character_1_state['position'] += 1
                            character_1_state['moves_remaining'] -= 1

                        # Check for lap completion
                        if old_position == 24 and character_1_state['position'] > 24:
                            character_1_state['laps_completed'] += 1
                            lap_damage = character_1_state['character_obj'].get_lap_damage(
                                character_1_state['laps_completed'])
                            boss_current_hp -= lap_damage

                        # Wrap around board
                        if character_1_state['position'] > 24:
                            character_1_state['position'] = 1


                        # Check if movement complete
                        if character_1_state['moves_remaining'] == 0:
                            character_1_state['is_moving'] = False

                            # Handle tile landing effects for character 1
                            landing_position = character_1_state['position']

                            if landing_position in green_tiles:
                                # Heal and clear debuffs
                                character_1_state['current_hp'] = min(
                                    character_1_state['max_hp'],
                                    character_1_state['current_hp'] + GREEN_TILE_HEAL
                                )
                                character_1_state['debuff_stacks'] = 0

                            elif landing_position in red_tiles:
                                # Add debuff stack
                                character_1_state['debuff_stacks'] += 1

                            elif landing_position in yellow_tiles:
                                # Get the effect for this specific tile
                                effect = yellow_tile_effects.get(landing_position, None)

                                # Apply Huntsman's yellow tile bonus damage if applicable
                                if character_1_state['character_obj'].name == "Huntsman":
                                    yellow_bonus = character_1_state['character_obj'].get_yellow_tile_damage()
                                    boss_current_hp -= yellow_bonus

                                # Apply the tile effect
                                if effect == "double_movement":
                                    character_1_state['yellow_buff_active'] = True
                                elif effect == "poison_5":
                                    boss_poison_stacks += 5
                                    boss_current_hp -= boss_poison_stacks
                                elif effect == "burning_strike":
                                    boss_burn_stacks += 3
                                elif effect == "lifesteal":
                                    lifesteal_active = True
                                elif effect == "chain_lightning":
                                    boss_current_hp -= CHAIN_LIGHTNING_INITIAL_DAMAGE
                                    chain_lightning_stacks = 2

                            else:
                                # Normal tile - deal damage to boss, take boss damage
                                # Get dice damage from the character state
                                dice_damage = character_1_state['character_obj'].base_damage
                                boss_current_hp -= dice_damage

                                # Lifesteal check
                                if lifesteal_active:
                                    character_1_state['current_hp'] = min(
                                        character_1_state['max_hp'],
                                        character_1_state['current_hp'] + dice_damage
                                    )
                                    lifesteal_active = False

                                # Take boss damage
                                character_1_state['current_hp'] -= boss_current_damage
                                boss_attack_count += 1
                                boss_current_damage = BOSS_INITIAL_DAMAGE + (
                                            boss_attack_count * BOSS_DAMAGE_INCREMENT)

                # Check if character 2 is moving
                if character_2_state['is_moving']:
                    character_2_state['move_counter'] += 1
                    if character_2_state['move_counter'] >= 10:
                        character_2_state['move_counter'] = 0
                        old_position = character_2_state['position']

                        # Move
                        if character_2_state['moves_remaining'] > 0:
                            character_2_state['position'] += 1
                            character_2_state['moves_remaining'] -= 1

                        # Check for lap completion
                        if old_position == 24 and character_2_state['position'] > 24:
                            character_2_state['laps_completed'] += 1
                            lap_damage = character_2_state['character_obj'].get_lap_damage(
                                character_2_state['laps_completed'])
                            boss_current_hp -= lap_damage

                        # Wrap around board
                        if character_2_state['position'] > 24:
                            character_2_state['position'] = 1


                        # Check if movement complete
                        if character_2_state['moves_remaining'] == 0:
                            character_2_state['is_moving'] = False

                            # Handle tile landing effects for character 2
                            landing_position = character_2_state['position']

                            if landing_position in green_tiles:
                                # Heal and clear debuffs
                                character_2_state['current_hp'] = min(
                                    character_2_state['max_hp'],
                                    character_2_state['current_hp'] + GREEN_TILE_HEAL
                                )
                                character_2_state['debuff_stacks'] = 0

                            elif landing_position in red_tiles:
                                # Add debuff stack
                                character_2_state['debuff_stacks'] += 1

                            elif landing_position in yellow_tiles:
                                # Get the effect for this specific tile
                                effect = yellow_tile_effects.get(landing_position, None)

                                # Apply Huntsman's yellow tile bonus damage if applicable
                                if character_2_state['character_obj'].name == "Huntsman":
                                    yellow_bonus = character_2_state['character_obj'].get_yellow_tile_damage()
                                    boss_current_hp -= yellow_bonus

                                # Apply the tile effect
                                if effect == "double_movement":
                                    character_2_state['yellow_buff_active'] = True
                                elif effect == "poison_5":
                                    boss_poison_stacks += 5
                                    boss_current_hp -= boss_poison_stacks
                                elif effect == "burning_strike":
                                    boss_burn_stacks += 3
                                elif effect == "lifesteal":
                                    lifesteal_active = True
                                elif effect == "chain_lightning":
                                    boss_current_hp -= CHAIN_LIGHTNING_INITIAL_DAMAGE
                                    chain_lightning_stacks = 2

                            else:
                                # Normal tile - deal damage to boss, take boss damage
                                # Get dice damage from the character state
                                dice_damage = character_2_state['character_obj'].base_damage
                                boss_current_hp -= dice_damage

                                # Lifesteal check
                                if lifesteal_active:
                                    character_2_state['current_hp'] = min(
                                        character_2_state['max_hp'],
                                        character_2_state['current_hp'] + dice_damage
                                    )
                                    lifesteal_active = False

                                # Take boss damage
                                character_2_state['current_hp'] -= boss_current_damage
                                boss_attack_count += 1
                                boss_current_damage = BOSS_INITIAL_DAMAGE + (
                                            boss_attack_count * BOSS_DAMAGE_INCREMENT)

                # Check if both characters done moving and it's boss attack phase
                if (not character_1_state['is_moving'] and
                        not character_2_state['is_moving'] and
                        turn_phase == "boss_attack"):

                    # Determine which character moved second (gets attacked)
                    # Based on previous turn_phase before it was set to "boss_attack"
                    # We need to track who moved second during dice rolling
                    # For now, we'll determine based on turn tracking

                    # Apply start-of-turn effects first
                    # Apply debuff damage to both characters
                    if character_1_state['debuff_stacks'] > 0:
                        debuff_damage = DEBUFF_DAMAGE * character_1_state['debuff_stacks']
                        character_1_state['current_hp'] -= debuff_damage

                    if character_2_state['debuff_stacks'] > 0:
                        debuff_damage = DEBUFF_DAMAGE * character_2_state['debuff_stacks']
                        character_2_state['current_hp'] -= debuff_damage

                    # Apply poison damage to boss and tick down
                    if boss_poison_stacks > 0:
                        boss_current_hp -= boss_poison_stacks
                        boss_poison_stacks -= 1

                    # Apply burn damage to boss (doesn't decay)
                    if boss_burn_stacks > 0:
                        burn_damage = boss_burn_stacks * BURN_DAMAGE_PER_STACK
                        boss_current_hp -= burn_damage

                    # Apply chain lightning DoT and tick down
                    if chain_lightning_stacks > 0:
                        boss_current_hp -= CHAIN_LIGHTNING_DOT_DAMAGE
                        chain_lightning_stacks -= 1

                    # Boss attacks the character who moved second
                    if last_character_to_move:
                        last_character_to_move['current_hp'] -= boss_current_damage

                    # CHECK WIN/LOSS CONDITIONS
                    # Check if boss is defeated
                    if boss_current_hp <= 0:
                        print("VICTORY! Boss defeated!")
                        # TODO: Show victory screen
                        game_state = "start"  # Return to start for now

                    # Check if both characters are dead
                    elif character_1_state['current_hp'] <= 0 and character_2_state['current_hp'] <= 0:
                        print("DEFEAT! Both characters died!")
                        # TODO: Show defeat screen
                        game_state = "start"  # Return to start for now

                    # Reset for next turn
                    turn_phase = "choose_first"

            else:
                # Single player mode - Animate player movement
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
                                # First, deal Huntsman's yellow tile damage if applicable
                                yellow_tile_bonus_damage = current_character.get_yellow_tile_damage()
                                if yellow_tile_bonus_damage > 0:
                                    boss_current_hp -= yellow_tile_bonus_damage

                                # Then apply the chosen yellow tile effect
                                effect = current_character.yellow_tile_effect()
                                if effect == "double_movement":
                                    yellow_buff_active = True
                                elif effect == "poison_5":
                                    # Add 5 poison stacks and deal immediate poison damage
                                    boss_poison_stacks += 5
                                    boss_current_hp -= boss_poison_stacks
                                elif effect == "burning_strike":
                                    # Add 3 burn stacks (doesn't decay)
                                    boss_burn_stacks += 3
                                elif effect == "lifesteal":
                                    # Activate lifesteal for next hit
                                    lifesteal_active = True
                                elif effect == "chain_lightning":
                                    # Deal immediate damage and set up DoT
                                    boss_current_hp -= CHAIN_LIGHTNING_INITIAL_DAMAGE
                                    chain_lightning_stacks = 2  # Will deal damage for next 2 turns
                            else:
                                # Normal tile - damage boss using dice damage and take boss damage
                                damage_dealt = current_dice_damage
                                boss_current_hp -= damage_dealt

                                # Lifesteal effect - heal for damage dealt
                                if lifesteal_active:
                                    player_current_hp = min(player_max_hp, player_current_hp + damage_dealt)
                                    lifesteal_active = False  # Consume the effect

                                player_current_hp -= boss_current_damage
                                boss_attack_count += 1
                                boss_current_damage = BOSS_INITIAL_DAMAGE + (boss_attack_count * BOSS_DAMAGE_INCREMENT)
    # ===== DRAWING =====
    if game_state == "start":
        start_menu.draw(screen)
    elif game_state == "campaign_team_select":
        campaign_team_select.draw(screen)
    elif game_state == "campaign_dice_select":
        campaign_dice_select.draw(screen)
    elif game_state == "character_select":
        character_select.draw(screen)
    elif game_state == "dice_select":
        dice_select.draw(screen)
    elif game_state == "yellow_tile_select":
        yellow_tile_select.draw(screen)
    elif game_state == "battle":
        # Package game state into dictionary for renderer
        if campaign_mode:
            # Campaign mode - use 2-character state
            game_state_dict = {
                'campaign_mode': True,
                'character_1_state': character_1_state,
                'character_2_state': character_2_state,
                'board_positions': board_positions,
                'green_tiles': green_tiles,
                'red_tiles': red_tiles,
                'yellow_tiles': yellow_tiles,
                'yellow_tile_effects': yellow_tile_effects,
                'highlighted_tiles': [],  # TODO: implement for 2 chars
                'boss_current_hp': boss_current_hp,
                'boss_max_hp': boss_max_hp,
                'battle_phase': battle_phase,
                'yellow_tiles_to_place': yellow_tiles_to_place,
                'yellow_tiles_placed': yellow_tiles_placed,
                'boss_current_damage': boss_current_damage,
                'boss_poison_stacks': boss_poison_stacks,
                'boss_burn_stacks': boss_burn_stacks,
                'lifesteal_active': lifesteal_active,
                'chain_lightning_stacks': chain_lightning_stacks,
                'turn_phase': turn_phase
            }
        else:
            # Single player mode - use old state
            game_state_dict = {
                'campaign_mode': False,
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
                'boss_poison_stacks': boss_poison_stacks,
                'boss_burn_stacks': boss_burn_stacks,
                'lifesteal_active': lifesteal_active,
                'chain_lightning_stacks': chain_lightning_stacks
            }
        battle_renderer.draw_battle_screen(screen, game_state_dict)

    # ===== UPDATE DISPLAY =====
    pygame.display.flip()
    clock.tick(60)

# ===== CLEANUP =====
pygame.quit()