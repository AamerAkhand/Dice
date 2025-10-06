import pygame
import os


class YellowTileSelect:
    def __init__(self, screen_width, screen_height, colors, fonts, character):
        """
        Initialize the yellow tile selection screen

        Args:
            screen_width: Width of the game window
            screen_height: Height of the game window
            colors: Dictionary of color constants
            fonts: Dictionary of font objects
            character: The selected character
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.colors = colors
        self.fonts = fonts
        self.character = character

        # Define the yellow tile options
        self.tile_options = [
            {
                'name': 'Double Movement',
                'description': 'Next roll moves 2x distance',
                'icon': 'lightning.png',
                'effect': 'double_movement',
                'num_tiles': 1
            },
            {
                'name': 'Poison Strike',
                'description': 'Apply 5 poison stacks',
                'icon': 'poison.png',
                'effect': 'poison_5',
                'num_tiles': 4
            },
            {
                'name': 'Burning Strike',
                'description': '3 burn stacks (3 dmg/turn)',
                'icon': 'burn.png',
                'effect': 'burning_strike',
                'num_tiles': 2
            },
            {
                'name': 'Lifesteal',
                'description': 'Damage + heal for same amount',
                'icon': 'lifesteal.png',
                'effect': 'lifesteal',
                'num_tiles': 3
            },
            {
                'name': 'Chain Lightning',
                'description': '20 dmg now, 10 dmg next 2 turns',
                'icon': 'chainlightning.png',
                'effect': 'chain_lightning',
                'num_tiles': 3
            }
        ]

        # Create selection buttons
        button_width = 250
        button_height = 180
        margin = 20
        buttons_per_row = 3

        start_y = 150

        self.option_buttons = []
        for i, option in enumerate(self.tile_options):
            row = i // buttons_per_row
            col = i % buttons_per_row

            # Calculate position to center the grid
            total_width = (button_width * buttons_per_row) + (margin * (buttons_per_row - 1))
            start_x = (screen_width - total_width) // 2

            x = start_x + col * (button_width + margin)
            y = start_y + row * (button_height + margin)

            button_rect = pygame.Rect(x, y, button_width, button_height)
            self.option_buttons.append((button_rect, option))

        # Get the directory where this script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # Load icons
        icon_size = (60, 60)

        try:
            lightning_path = os.path.join(script_dir, 'lightning.png')
            self.lightning_icon = pygame.image.load(lightning_path)
            self.lightning_icon = pygame.transform.scale(self.lightning_icon, icon_size)
        except Exception as e:
            print(f"Warning: lightning.png not found - {e}")
            self.lightning_icon = None

        try:
            poison_path = os.path.join(script_dir, 'poison.png')
            self.poison_icon = pygame.image.load(poison_path)
            self.poison_icon = pygame.transform.scale(self.poison_icon, icon_size)
        except Exception as e:
            print(f"Warning: poison.png not found - {e}")
            self.poison_icon = None

        try:
            burn_path = os.path.join(script_dir, 'burn.png')
            self.burn_icon = pygame.image.load(burn_path)
            self.burn_icon = pygame.transform.scale(self.burn_icon, icon_size)
        except Exception as e:
            print(f"Warning: burn.png not found - {e}")
            self.burn_icon = None

        try:
            lifesteal_path = os.path.join(script_dir, 'lifesteal.png')
            self.lifesteal_icon = pygame.image.load(lifesteal_path)
            self.lifesteal_icon = pygame.transform.scale(self.lifesteal_icon, icon_size)
        except Exception as e:
            print(f"Warning: lifesteal.png not found - {e}")
            self.lifesteal_icon = None

        try:
            chainlightning_path = os.path.join(script_dir, 'chainlightning.png')
            self.chainlightning_icon = pygame.image.load(chainlightning_path)
            self.chainlightning_icon = pygame.transform.scale(self.chainlightning_icon, icon_size)
        except Exception as e:
            print(f"Warning: chainlightning.png not found - {e}")
            self.chainlightning_icon = None

    def handle_click(self, mouse_pos):
        """
        Check if a yellow tile option was clicked

        Args:
            mouse_pos: Tuple of (x, y) mouse position

        Returns:
            Selected option dictionary if clicked, None otherwise
        """
        for button_rect, option in self.option_buttons:
            if button_rect.collidepoint(mouse_pos):
                return option
        return None

    def draw(self, screen):
        """
        Draw the yellow tile selection screen

        Args:
            screen: Pygame screen surface to draw on
        """
        screen.fill(self.colors['WHITE'])

        # Draw title
        title = self.fonts['large'].render(f"{self.character.name}: Choose Yellow Tile Effect", True,
                                           self.colors['BLACK'])
        title_rect = title.get_rect(center=(self.screen_width // 2, 50))
        screen.blit(title, title_rect)

        # Draw option buttons
        for button_rect, option in self.option_buttons:
            # Draw button background
            pygame.draw.rect(screen, self.colors['YELLOW'], button_rect, border_radius=10)
            pygame.draw.rect(screen, self.colors['BLACK'], button_rect, 3, border_radius=10)

            # Draw icon
            icon = None
            if option['icon'] == 'lightning.png' and self.lightning_icon:
                icon = self.lightning_icon
            elif option['icon'] == 'poison.png' and self.poison_icon:
                icon = self.poison_icon
            elif option['icon'] == 'burn.png' and self.burn_icon:
                icon = self.burn_icon
            elif option['icon'] == 'lifesteal.png' and self.lifesteal_icon:
                icon = self.lifesteal_icon
            elif option['icon'] == 'chainlightning.png' and self.chainlightning_icon:
                icon = self.chainlightning_icon

            if icon:
                icon_rect = icon.get_rect(center=(button_rect.centerx, button_rect.centery - 40))
                screen.blit(icon, icon_rect)

            # Draw option name
            name_text = self.fonts['small'].render(option['name'], True, self.colors['BLACK'])
            name_rect = name_text.get_rect(center=(button_rect.centerx, button_rect.centery + 20))
            screen.blit(name_text, name_rect)

            # Draw number of tiles
            tiles_text = self.fonts['small'].render(f"Place {option['num_tiles']} tile(s)", True, self.colors['BLACK'])
            tiles_rect = tiles_text.get_rect(center=(button_rect.centerx, button_rect.centery + 45))
            screen.blit(tiles_text, tiles_rect)

            # Draw description (word wrap if needed)
            desc_lines = self._wrap_text(option['description'], self.fonts['small'], button_rect.width - 20)
            y_offset = button_rect.centery + 70
            for line in desc_lines:
                desc_text = self.fonts['small'].render(line, True, self.colors['BLACK'])
                desc_rect = desc_text.get_rect(center=(button_rect.centerx, y_offset))
                screen.blit(desc_text, desc_rect)
                y_offset += 20

    def _wrap_text(self, text, font, max_width):
        """Helper function to wrap text to fit within max_width"""
        words = text.split(' ')
        lines = []
        current_line = []

        for word in words:
            test_line = ' '.join(current_line + [word])
            if font.size(test_line)[0] <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]

        if current_line:
            lines.append(' '.join(current_line))

        return lines