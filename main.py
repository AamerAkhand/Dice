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
                    character_1, character_2 = selected_team
                    # TODO: Go to dice select next
                    print(f"Selected: {character_1.name} and {character_2.name}")
                    game_state = "campaign_dice_select"

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

                            # Store the damage from the dice that was just rolled
                            current_dice_damage = current_character.dice_damage[i]

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

                            # Apply burn damage to boss (doesn't decay)
                            if boss_burn_stacks > 0:
                                burn_damage = boss_burn_stacks * BURN_DAMAGE_PER_STACK
                                boss_current_hp -= burn_damage

                            # Apply chain lightning DoT damage and tick down
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