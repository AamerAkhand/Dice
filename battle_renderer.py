import pygame
import os


class BattleRenderer:
    def __init__(self, screen_width, screen_height, colors, fonts, constants):
        """
        Initialize the battle renderer

        Args:
            screen_width: Width of game window
            screen_height: Height of game window
            colors: Dictionary of color constants
            fonts: Dictionary of font objects
            constants: Dictionary of game constants (SQUARE_SIZE, BOARD_MARGIN, etc.)
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.colors = colors
        self.fonts = fonts
        self.constants = constants

        # Get the directory where this script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # Load and scale tile icons
        icon_size = (60, 60)  # Adjust size as needed

        # Load yellow tile icons (character-specific)
        try:
            poison_path = os.path.join(script_dir, 'poison.png')
            self.poison_icon = pygame.image.load(poison_path)
            self.poison_icon = pygame.transform.scale(self.poison_icon, icon_size)
        except Exception as e:
            print(f"Warning: poison.png not found - {e}")
            self.poison_icon = None

        try:
            lightning_path = os.path.join(script_dir, 'lightning.png')
            self.lightning_icon = pygame.image.load(lightning_path)
            self.lightning_icon = pygame.transform.scale(self.lightning_icon, icon_size)
        except Exception as e:
            print(f"Warning: lightning.png not found - {e}")
            self.lightning_icon = None

        # Load red tile icon
        try:
            fire_path = os.path.join(script_dir, 'fire.png')
            self.fire_icon = pygame.image.load(fire_path)
            self.fire_icon = pygame.transform.scale(self.fire_icon, icon_size)
        except Exception as e:
            print(f"Warning: fire.png not found - {e}")
            self.fire_icon = None

        # Load green tile icon
        try:
            heal_path = os.path.join(script_dir, 'heal.png')
            self.heal_icon = pygame.image.load(heal_path)
            self.heal_icon = pygame.transform.scale(self.heal_icon, icon_size)
        except Exception as e:
            print(f"Warning: heal.png not found - {e}")
            self.heal_icon = None

    def draw_board(self, screen, board_positions, green_tiles, red_tiles, yellow_tiles, highlighted_tiles, character,
                   yellow_tile_effects=None):
        """Draw the game board with tiles"""
        for i, (x, y) in enumerate(board_positions):
            tile_number = i + 1  # Tiles numbered 1-24

            # Determine tile color (priority: red > green > yellow > white)
            if tile_number in red_tiles:
                tile_color = self.colors['DARK_RED']
            elif tile_number in green_tiles:
                tile_color = self.colors['GREEN']
            elif tile_number in yellow_tiles:
                tile_color = self.colors['YELLOW']
            else:
                tile_color = self.colors['WHITE']

            # Draw square
            pygame.draw.rect(screen, tile_color, (x, y, self.constants['SQUARE_SIZE'],
                                                  self.constants['SQUARE_SIZE']))

            # Draw red outline if this tile is a possible landing spot
            if tile_number in highlighted_tiles:
                pygame.draw.rect(screen, self.colors['RED'],
                                 (x, y, self.constants['SQUARE_SIZE'], self.constants['SQUARE_SIZE']), 5)
            else:
                pygame.draw.rect(screen, self.colors['BLACK'],
                                 (x, y, self.constants['SQUARE_SIZE'], self.constants['SQUARE_SIZE']), 2)

            # Draw square number
            text = self.fonts['small'].render(str(tile_number), True, self.colors['BLACK'])
            screen.blit(text, (x + 5, y + 5))

            # Draw icons for special tiles
            icon = None
            if tile_number in yellow_tiles:
                # Check yellow_tile_effects to determine which icon
                if yellow_tile_effects and tile_number in yellow_tile_effects:
                    effect = yellow_tile_effects[tile_number]
                    if effect == "poison_5" and self.poison_icon:
                        icon = self.poison_icon
                    elif effect == "double_movement" and self.lightning_icon:
                        icon = self.lightning_icon
                else:
                    # Fallback to character's default icon
                    if character and character.yellow_icon == "poison.png" and self.poison_icon:
                        icon = self.poison_icon
                    elif character and character.yellow_icon == "lightning.png" and self.lightning_icon:
                        icon = self.lightning_icon
            elif tile_number in red_tiles and self.fire_icon:
                icon = self.fire_icon
            elif tile_number in green_tiles and self.heal_icon:
                icon = self.heal_icon

            # Center the icon in the tile
            if icon:
                icon_rect = icon.get_rect(center=(x + self.constants['SQUARE_SIZE'] // 2,
                                                  y + self.constants['SQUARE_SIZE'] // 2))
                screen.blit(icon, icon_rect)

    def draw_player(self, screen, position, board_positions, current_hp, max_hp, player_color=None):
        """Draw player token with HP bar"""
        x, y = board_positions[position - 1]  # Adjust for 1-indexed
        center_x = x + self.constants['SQUARE_SIZE'] // 2
        center_y = y + self.constants['SQUARE_SIZE'] // 2

        # Use provided color or default to RED
        if player_color is None:
            player_color = self.colors['RED']

        # Draw player circle
        pygame.draw.circle(screen, player_color, (center_x, center_y), 20)
        pygame.draw.circle(screen, self.colors['BLACK'], (center_x, center_y), 20, 3)

        # Draw player HP bar above player
        bar_width = 50
        bar_height = 6
        bar_x = center_x - bar_width // 2
        bar_y = center_y - 35

        # Background
        pygame.draw.rect(screen, self.colors['LIGHT_GRAY'], (bar_x, bar_y, bar_width, bar_height))

        # Current HP
        hp_percentage = max(0, current_hp / max_hp)
        current_bar_width = int(bar_width * hp_percentage)
        pygame.draw.rect(screen, self.colors['DARK_GREEN'], (bar_x, bar_y, current_bar_width, bar_height))

        # Border
        pygame.draw.rect(screen, self.colors['BLACK'], (bar_x, bar_y, bar_width, bar_height), 1)

    def draw_boss(self, screen, current_hp, max_hp):
        """Draw boss with HP bar in center of board"""
        # Position boss in center of the board
        board_center_x = 200 + 50 + (7 * 100) // 2  # offset_x + margin + (board_width / 2)
        board_center_y = 50 + 50 + (7 * 100) // 2  # offset_y + margin + (board_height / 2)

        boss_x = board_center_x  # Centered
        boss_y = board_center_y - 100  # 100px above center

        # Draw boss (larger circle)
        pygame.draw.circle(screen, self.colors['DARK_RED'], (boss_x, boss_y), 40)
        pygame.draw.circle(screen, self.colors['BLACK'], (boss_x, boss_y), 40, 4)

        # Draw boss HP bar
        bar_width = 200
        bar_height = 25
        bar_x = boss_x - bar_width // 2
        bar_y = boss_y + 60

        # Background
        pygame.draw.rect(screen, self.colors['LIGHT_GRAY'], (bar_x, bar_y, bar_width, bar_height))

        # Current HP
        hp_percentage = max(0, current_hp / max_hp)
        current_bar_width = int(bar_width * hp_percentage)
        pygame.draw.rect(screen, self.colors['DARK_RED'], (bar_x, bar_y, current_bar_width, bar_height))

        # Border
        pygame.draw.rect(screen, self.colors['BLACK'], (bar_x, bar_y, bar_width, bar_height), 3)

        # HP text
        hp_text = self.fonts['small'].render(f"{max(0, current_hp)}/{max_hp}", True, self.colors['BLACK'])
        text_rect = hp_text.get_rect(center=(boss_x, bar_y + bar_height // 2))
        screen.blit(hp_text, text_rect)

        # Boss label
        boss_label = self.fonts['medium'].render("BOSS", True, self.colors['BLACK'])
        label_rect = boss_label.get_rect(center=(boss_x, boss_y - 60))
        screen.blit(boss_label, label_rect)

    def draw_dice(self, screen, dice_rects, dice_colors, dice_values, dice_labels):
        """Draw all three dice with labels - positioned in center of board"""
        # Position dice in center of the board
        board_center_x = 200 + 50 + (7 * 100) // 2  # offset_x + margin + (board_width / 2)
        board_center_y = 50 + 50 + (7 * 100) // 2  # offset_y + margin + (board_height / 2)

        # Center the dice horizontally around the board center
        dice_start_x = board_center_x - 180  # Start position to center 3 dice with spacing
        dice_y = board_center_y + 40  # 40px below center

        for i, (colors, value, label) in enumerate(zip(dice_colors, dice_values, dice_labels)):
            x = dice_start_x + (i * 120)
            rect = pygame.Rect(x, dice_y, 100, 100)

            # Draw label above dice
            label_text = self.fonts['small'].render(label, True, self.colors['BLACK'])
            label_rect = label_text.get_rect(center=(rect.centerx, rect.top - 15))
            screen.blit(label_text, label_rect)

            # Draw dice
            pygame.draw.rect(screen, colors[0], rect, border_radius=15)
            pygame.draw.rect(screen, colors[1], rect, width=4, border_radius=15)

            # Draw dice value
            text = self.fonts['large'].render(str(value), True, self.colors['WHITE'])
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)

    def draw_campaign_dice(self, screen, character_1_state, character_2_state, turn_phase):
        """Draw dice for both characters in campaign mode"""
        # Position calculations
        board_center_x = 200 + 50 + (7 * 100) // 2
        board_center_y = 50 + 50 + (7 * 100) // 2
        dice_y = board_center_y + 40

        # Character 1 dice (left side)
        char_1_start_x = board_center_x - 400
        char_1_label_y = dice_y - 50

        # Draw character 1 label
        char_1_label = self.fonts['medium'].render(
            character_1_state['character_obj'].name,
            True,
            self.colors['BLACK']
        )
        label_rect = char_1_label.get_rect(center=(char_1_start_x + 180, char_1_label_y))
        screen.blit(char_1_label, label_rect)

        # Draw character 1 HP
        hp_text = self.fonts['small'].render(
            f"HP: {character_1_state['current_hp']}/{character_1_state['max_hp']}",
            True,
            self.colors['BLACK']
        )
        hp_rect = hp_text.get_rect(center=(char_1_start_x + 180, char_1_label_y + 25))
        screen.blit(hp_text, hp_rect)

        # Determine if character 1 dice should be highlighted
        char_1_active = (turn_phase == "choose_first" or turn_phase == "character_1_second")

        # Draw character 1 dice
        for i in range(3):
            x = char_1_start_x + (i * 120)
            rect = pygame.Rect(x, dice_y, 100, 100)

            # Highlight if active
            if char_1_active:
                # Draw glow effect
                pygame.draw.rect(screen, self.colors['YELLOW'],
                                 (x - 5, dice_y - 5, 110, 110),
                                 border_radius=15)

            # Draw dice label
            label = character_1_state['dice_labels'][i]
            label_text = self.fonts['small'].render(label, True, self.colors['BLACK'])
            label_rect = label_text.get_rect(center=(rect.centerx, rect.top - 15))
            screen.blit(label_text, label_rect)

            # Draw dice
            dice_color = self.colors['BLUE'] if i == 0 else (self.colors['PURPLE'] if i == 1 else self.colors['ORANGE'])
            dice_border = self.colors['DARK_BLUE'] if i == 0 else (
                self.colors['DARK_PURPLE'] if i == 1 else self.colors['DARK_ORANGE'])
            pygame.draw.rect(screen, dice_color, rect, border_radius=15)
            pygame.draw.rect(screen, dice_border, rect, width=4, border_radius=15)

            # Draw dice value
            value = character_1_state['dice_values'][i]
            value_text = self.fonts['large'].render(str(value), True, self.colors['WHITE'])
            value_rect = value_text.get_rect(center=rect.center)
            screen.blit(value_text, value_rect)

        # Character 2 dice (right side)
        char_2_start_x = board_center_x + 40
        char_2_label_y = dice_y - 50

        # Draw character 2 label
        char_2_label = self.fonts['medium'].render(
            character_2_state['character_obj'].name,
            True,
            self.colors['BLACK']
        )
        label_rect = char_2_label.get_rect(center=(char_2_start_x + 180, char_2_label_y))
        screen.blit(char_2_label, label_rect)

        # Draw character 2 HP
        hp_text = self.fonts['small'].render(
            f"HP: {character_2_state['current_hp']}/{character_2_state['max_hp']}",
            True,
            self.colors['BLACK']
        )
        hp_rect = hp_text.get_rect(center=(char_2_start_x + 180, char_2_label_y + 25))
        screen.blit(hp_text, hp_rect)

        # Determine if character 2 dice should be highlighted
        char_2_active = (turn_phase == "choose_first" or turn_phase == "character_2_second")

        # Draw character 2 dice
        for i in range(3):
            x = char_2_start_x + (i * 120)
            rect = pygame.Rect(x, dice_y, 100, 100)

            # Highlight if active
            if char_2_active:
                # Draw glow effect
                pygame.draw.rect(screen, self.colors['YELLOW'],
                                 (x - 5, dice_y - 5, 110, 110),
                                 border_radius=15)

            # Draw dice label
            label = character_2_state['dice_labels'][i]
            label_text = self.fonts['small'].render(label, True, self.colors['BLACK'])
            label_rect = label_text.get_rect(center=(rect.centerx, rect.top - 15))
            screen.blit(label_text, label_rect)

            # Draw dice
            dice_color = self.colors['BLUE'] if i == 0 else (self.colors['PURPLE'] if i == 1 else self.colors['ORANGE'])
            dice_border = self.colors['DARK_BLUE'] if i == 0 else (
                self.colors['DARK_PURPLE'] if i == 1 else self.colors['DARK_ORANGE'])
            pygame.draw.rect(screen, dice_color, rect, border_radius=15)
            pygame.draw.rect(screen, dice_border, rect, width=4, border_radius=15)

            # Draw dice value
            value = character_2_state['dice_values'][i]
            value_text = self.fonts['large'].render(str(value), True, self.colors['WHITE'])
            value_rect = value_text.get_rect(center=rect.center)
            screen.blit(value_text, value_rect)

    def draw_character_info(self, screen, character):
        """Draw character name and passive side by side in top-left corner"""
        # Character name
        name_text = self.fonts['medium'].render(character.name, True, self.colors['BLACK'])
        screen.blit(name_text, (10, 10))

        # Get width of name to position passive to the right
        name_width = name_text.get_width()

        # Passive description (to the right of name)
        passive_text = self.fonts['small'].render(character.passive_description, True, self.colors['BLACK'])
        screen.blit(passive_text, (20 + name_width, 18))

    def draw_boss_damage_info(self, screen, boss_current_damage, boss_poison_stacks):
        """Draw boss damage info in top-right corner"""
        damage_text = self.fonts['medium'].render(f"Boss Damage: {boss_current_damage}", True, self.colors['DARK_RED'])
        text_rect = damage_text.get_rect(topright=(self.screen_width - 10, 10))
        screen.blit(damage_text, text_rect)

        # Draw poison stacks if active
        if boss_poison_stacks > 0:
            poison_text = self.fonts['small'].render(f"Poisoned: {boss_poison_stacks} stacks", True,
                                                     self.colors['GREEN'])
            poison_rect = poison_text.get_rect(topright=(self.screen_width - 10, 45))
            screen.blit(poison_text, poison_rect)

    def draw_game_info(self, screen, player_position, laps_completed, is_moving, debuff_stacks, battle_phase,
                       yellow_buff_active, yellow_tiles_to_place, yellow_tiles_placed, boss_burn_stacks,
                       lifesteal_active, chain_lightning_stacks):
        """Draw position, laps, debuff status, and instructions on the LEFT side"""
        info_x = 30  # Left side of screen
        info_y = 150
        line_height = 30

        # Draw instruction based on battle phase
        if battle_phase == "place_yellow":
            tiles_remaining = yellow_tiles_to_place - yellow_tiles_placed
            instruction_text = f"Place {tiles_remaining} special tile(s)"
            instruction = self.fonts['medium'].render(instruction_text, True, self.colors['DARK_YELLOW'])
            screen.blit(instruction, (info_x, info_y))
            info_y += line_height + 10
        else:
            instruction_text = "Moving..." if is_moving else "Click a dice to roll!"
            instruction = self.fonts['medium'].render(instruction_text, True, self.colors['BLACK'])
            screen.blit(instruction, (info_x, info_y))
            info_y += line_height + 10

            # Draw current position info
            pos_text = self.fonts['small'].render(f"Position: {player_position}", True, self.colors['BLACK'])
            screen.blit(pos_text, (info_x, info_y))
            info_y += line_height

            # Draw laps completed
            laps_text = self.fonts['small'].render(f"Laps: {laps_completed}", True, self.colors['BLACK'])
            screen.blit(laps_text, (info_x, info_y))
            info_y += line_height + 20

            # Active Effects Section
            effects_header = self.fonts['medium'].render("Active Effects:", True, self.colors['BLACK'])
            screen.blit(effects_header, (info_x, info_y))
            info_y += line_height + 5

            # Draw yellow buff status if active
            if yellow_buff_active:
                buff_text = self.fonts['small'].render("• Double Movement", True, self.colors['DARK_YELLOW'])
                screen.blit(buff_text, (info_x + 10, info_y))
                info_y += line_height

            # Draw debuff status if active
            if debuff_stacks > 0:
                damage_per_turn = debuff_stacks * 5
                debuff_text = self.fonts['small'].render(f"• Debuffed x{debuff_stacks} (-{damage_per_turn} HP)", True,
                                                         self.colors['DARK_RED'])
                screen.blit(debuff_text, (info_x + 10, info_y))
                info_y += line_height

            # Draw burn stacks if active
            if boss_burn_stacks > 0:
                damage_per_turn = boss_burn_stacks * 3
                burn_text = self.fonts['small'].render(f"• Boss Burning x{boss_burn_stacks} ({damage_per_turn} dmg)",
                                                       True, self.colors['DARK_ORANGE'])
                screen.blit(burn_text, (info_x + 10, info_y))
                info_y += line_height

            # Draw lifesteal status if active
            if lifesteal_active:
                lifesteal_text = self.fonts['small'].render("• Lifesteal Ready", True, self.colors['DARK_RED'])
                screen.blit(lifesteal_text, (info_x + 10, info_y))
                info_y += line_height

            # Draw chain lightning stacks if active
            if chain_lightning_stacks > 0:
                chain_text = self.fonts['small'].render(f"• Chain Lightning ({chain_lightning_stacks} turns)", True,
                                                        self.colors['PURPLE'])
                screen.blit(chain_text, (info_x + 10, info_y))
                info_y += line_height

            # If no effects active
            if not any([yellow_buff_active, debuff_stacks > 0, boss_burn_stacks > 0, lifesteal_active,
                        chain_lightning_stacks > 0]):
                none_text = self.fonts['small'].render("• None", True, self.colors['LIGHT_GRAY'])
                screen.blit(none_text, (info_x + 10, info_y))

    def draw_battle_screen(self, screen, game_state):
        """
        Main draw method - draws the entire battle screen

        Args:
            screen: Pygame screen surface
            game_state: Dictionary containing all game state variables
        """
        screen.fill(self.colors['WHITE'])

        # Check if campaign mode or single player mode
        if game_state.get('campaign_mode', False):
            # Campaign mode - draw 2 characters
            self.draw_board(screen, game_state['board_positions'],
                            game_state['green_tiles'], game_state['red_tiles'],
                            game_state['yellow_tiles'],
                            game_state.get('highlighted_tiles', []),
                            game_state['character_1_state']['character_obj'],
                            game_state.get('yellow_tile_effects', {}))

            self.draw_boss(screen, game_state['boss_current_hp'], game_state['boss_max_hp'])

            # Draw both players
            char_1 = game_state['character_1_state']
            char_2 = game_state['character_2_state']

            self.draw_player(screen, char_1['position'], game_state['board_positions'],
                             char_1['current_hp'], char_1['max_hp'], self.colors['RED'])
            self.draw_player(screen, char_2['position'], game_state['board_positions'],
                             char_2['current_hp'], char_2['max_hp'], self.colors['BLUE'])

            # Draw dice for both characters
            if game_state['battle_phase'] == "rolling":
                self.draw_campaign_dice(screen, char_1, char_2, game_state['turn_phase'])

            # TODO: Draw character info for both

            self.draw_boss_damage_info(screen, game_state['boss_current_damage'],
                                       game_state['boss_poison_stacks'])

            # Campaign-specific UI
            if game_state['battle_phase'] == "place_yellow":
                # Yellow tile placement UI
                tiles_remaining = game_state['yellow_tiles_to_place'] - game_state['yellow_tiles_placed']
                instruction_text = f"Place {tiles_remaining} special tile(s)"
                instruction = self.fonts['medium'].render(instruction_text, True, self.colors['DARK_YELLOW'])
                screen.blit(instruction, (30, 150))
            else:
                # Show turn phase
                turn_text = ""
                if game_state['turn_phase'] == "choose_first":
                    turn_text = "Choose first character to move"
                elif game_state['turn_phase'] == "character_1_second":
                    turn_text = f"Choose {char_1['character_obj'].name}'s dice"
                elif game_state['turn_phase'] == "character_2_second":
                    turn_text = f"Choose {char_2['character_obj'].name}'s dice"
                elif game_state['turn_phase'] == "boss_attack":
                    turn_text = "Boss attacks!"

                instruction = self.fonts['medium'].render(turn_text, True, self.colors['BLACK'])
                screen.blit(instruction, (30, 150))

        else:
            # Single player mode - use old rendering
            self.draw_board(screen, game_state['board_positions'],
                            game_state['green_tiles'], game_state['red_tiles'],
                            game_state['yellow_tiles'],
                            game_state['highlighted_tiles'],
                            game_state['character'],
                            None)
            self.draw_boss(screen, game_state['boss_current_hp'], game_state['boss_max_hp'])
            self.draw_player(screen, game_state['player_position'],
                             game_state['board_positions'],
                             game_state['player_current_hp'], game_state['player_max_hp'])
            self.draw_dice(screen, game_state['dice_rects'], game_state['dice_colors'],
                           game_state['dice_values'], game_state['dice_labels'])
            self.draw_character_info(screen, game_state['character'])
            self.draw_boss_damage_info(screen, game_state['boss_current_damage'],
                                       game_state['boss_poison_stacks'])
            self.draw_game_info(screen, game_state['player_position'],
                                game_state['laps_completed'], game_state['is_moving'],
                                game_state['debuff_stacks'], game_state['battle_phase'],
                                game_state['yellow_buff_active'],
                                game_state['yellow_tiles_to_place'], game_state['yellow_tiles_placed'],
                                game_state['boss_burn_stacks'], game_state['lifesteal_active'],
                                game_state['chain_lightning_stacks'])