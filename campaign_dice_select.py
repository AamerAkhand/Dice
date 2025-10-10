import pygame
from characters import DICE_LIBRARY


class CampaignDiceSelect:
    def __init__(self, screen_width, screen_height, colors, fonts, character_1, character_2):
        """
        Initialize the campaign dice selection screen for 2 characters

        Args:
            screen_width: Width of the game window
            screen_height: Height of the game window
            colors: Dictionary of color constants
            fonts: Dictionary of font objects
            character_1: First selected character
            character_2: Second selected character
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.colors = colors
        self.fonts = fonts
        self.character_1 = character_1
        self.character_2 = character_2

        # Get available dice for each character
        self.char_1_available_dice = character_1.available_dice
        self.char_2_available_dice = character_2.available_dice

        # Track selected dice (list of dice keys)
        self.char_1_selected = []
        self.char_2_selected = []

        # Create dice option buttons for character 1 (left side)
        self.char_1_buttons = self._create_dice_buttons(
            self.char_1_available_dice,
            start_x=50,
            start_y=150
        )

        # Create dice option buttons for character 2 (right side)
        self.char_2_buttons = self._create_dice_buttons(
            self.char_2_available_dice,
            start_x=screen_width // 2 + 50,
            start_y=150
        )

        # Create confirm button
        confirm_width = 250
        confirm_height = 60
        confirm_x = (screen_width - confirm_width) // 2
        confirm_y = screen_height - 100
        self.confirm_button = pygame.Rect(confirm_x, confirm_y, confirm_width, confirm_height)

    def _create_dice_buttons(self, available_dice, start_x, start_y):
        """Create button rectangles for dice options"""
        buttons = []
        button_width = 150
        button_height = 100
        buttons_per_row = 3
        spacing_x = 20
        spacing_y = 20

        for i, dice_key in enumerate(available_dice):
            row = i // buttons_per_row
            col = i % buttons_per_row
            x = start_x + col * (button_width + spacing_x)
            y = start_y + row * (button_height + spacing_y)
            button_rect = pygame.Rect(x, y, button_width, button_height)
            buttons.append((button_rect, dice_key))

        return buttons

    def handle_click(self, mouse_pos):
        """
        Check if a dice option or confirm button was clicked

        Args:
            mouse_pos: Tuple of (x, y) mouse position

        Returns:
            Tuple of (char_1_dice_keys, char_2_dice_keys) if confirm clicked
            None otherwise
        """
        # Check character 1 dice buttons
        for button_rect, dice_key in self.char_1_buttons:
            if button_rect.collidepoint(mouse_pos):
                if dice_key in self.char_1_selected:
                    # Deselect
                    self.char_1_selected.remove(dice_key)
                elif len(self.char_1_selected) < 3:
                    # Select (max 3)
                    self.char_1_selected.append(dice_key)
                return None

        # Check character 2 dice buttons
        for button_rect, dice_key in self.char_2_buttons:
            if button_rect.collidepoint(mouse_pos):
                if dice_key in self.char_2_selected:
                    # Deselect
                    self.char_2_selected.remove(dice_key)
                elif len(self.char_2_selected) < 3:
                    # Select (max 3)
                    self.char_2_selected.append(dice_key)
                return None

        # Check confirm button
        if self.confirm_button.collidepoint(mouse_pos):
            if len(self.char_1_selected) == 3 and len(self.char_2_selected) == 3:
                return (self.char_1_selected, self.char_2_selected)

        return None

    def draw(self, screen):
        """
        Draw the dice selection screen

        Args:
            screen: Pygame screen surface to draw on
        """
        screen.fill(self.colors['WHITE'])

        # Draw title
        title = self.fonts['large'].render("Select Dice for Each Character", True, self.colors['BLACK'])
        title_rect = title.get_rect(center=(self.screen_width // 2, 50))
        screen.blit(title, title_rect)

        # Draw character 1 label
        char_1_label = self.fonts['medium'].render(f"{self.character_1.name} (Select 3)", True, self.colors['BLACK'])
        screen.blit(char_1_label, (50, 100))

        # Draw character 1 dice buttons
        for button_rect, dice_key in self.char_1_buttons:
            dice_data = DICE_LIBRARY[dice_key]
            is_selected = dice_key in self.char_1_selected

            # Button color
            button_color = self.colors['GREEN'] if is_selected else self.colors['LIGHT_GRAY']
            pygame.draw.rect(screen, button_color, button_rect, border_radius=10)
            pygame.draw.rect(screen, self.colors['BLACK'], button_rect, 3, border_radius=10)

            # Dice label
            label_text = self.fonts['small'].render(dice_data['label'], True, self.colors['BLACK'])
            label_rect = label_text.get_rect(center=(button_rect.centerx, button_rect.centery - 20))
            screen.blit(label_text, label_rect)

            # Dice values
            values_text = self.fonts['small'].render(str(dice_data['values']), True, self.colors['BLACK'])
            values_rect = values_text.get_rect(center=(button_rect.centerx, button_rect.centery + 10))
            screen.blit(values_text, values_rect)

            # Damage
            damage_text = self.fonts['small'].render(f"Dmg: {dice_data['damage']}", True, self.colors['BLACK'])
            damage_rect = damage_text.get_rect(center=(button_rect.centerx, button_rect.centery + 30))
            screen.blit(damage_text, damage_rect)

        # Draw character 2 label
        char_2_label = self.fonts['medium'].render(f"{self.character_2.name} (Select 3)", True, self.colors['BLACK'])
        screen.blit(char_2_label, (self.screen_width // 2 + 50, 100))

        # Draw character 2 dice buttons
        for button_rect, dice_key in self.char_2_buttons:
            dice_data = DICE_LIBRARY[dice_key]
            is_selected = dice_key in self.char_2_selected

            # Button color
            button_color = self.colors['GREEN'] if is_selected else self.colors['LIGHT_GRAY']
            pygame.draw.rect(screen, button_color, button_rect, border_radius=10)
            pygame.draw.rect(screen, self.colors['BLACK'], button_rect, 3, border_radius=10)

            # Dice label
            label_text = self.fonts['small'].render(dice_data['label'], True, self.colors['BLACK'])
            label_rect = label_text.get_rect(center=(button_rect.centerx, button_rect.centery - 20))
            screen.blit(label_text, label_rect)

            # Dice values
            values_text = self.fonts['small'].render(str(dice_data['values']), True, self.colors['BLACK'])
            values_rect = values_text.get_rect(center=(button_rect.centerx, button_rect.centery + 10))
            screen.blit(values_text, values_rect)

            # Damage
            damage_text = self.fonts['small'].render(f"Dmg: {dice_data['damage']}", True, self.colors['BLACK'])
            damage_rect = damage_text.get_rect(center=(button_rect.centerx, button_rect.centery + 30))
            screen.blit(damage_text, damage_rect)

        # Draw selection count
        char_1_count = self.fonts['small'].render(
            f"Selected: {len(self.char_1_selected)}/3",
            True,
            self.colors['BLACK']
        )
        screen.blit(char_1_count, (50, self.screen_height - 150))

        char_2_count = self.fonts['small'].render(
            f"Selected: {len(self.char_2_selected)}/3",
            True,
            self.colors['BLACK']
        )
        screen.blit(char_2_count, (self.screen_width // 2 + 50, self.screen_height - 150))

        # Draw confirm button
        both_ready = len(self.char_1_selected) == 3 and len(self.char_2_selected) == 3
        if both_ready:
            pygame.draw.rect(screen, self.colors['BLUE'], self.confirm_button, border_radius=10)
            pygame.draw.rect(screen, self.colors['BLACK'], self.confirm_button, 3, border_radius=10)
            confirm_text = self.fonts['medium'].render("Confirm Dice", True, self.colors['WHITE'])
        else:
            pygame.draw.rect(screen, self.colors['LIGHT_GRAY'], self.confirm_button, border_radius=10)
            pygame.draw.rect(screen, self.colors['BLACK'], self.confirm_button, 3, border_radius=10)
            confirm_text = self.fonts['medium'].render("Select 3 Dice Each", True, self.colors['BLACK'])

        confirm_text_rect = confirm_text.get_rect(center=self.confirm_button.center)
        screen.blit(confirm_text, confirm_text_rect)