import pygame
import os
from characters import get_available_dice


class DiceSelect:
    def __init__(self, screen_width, screen_height, colors, fonts, character):
        """
        Initialize the dice selection screen

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

        # Get available dice for this character
        self.available_dice = get_available_dice(character.name)

        # Track selected dice (up to 3)
        self.selected_dice = []

        # Create dice option buttons
        self.dice_buttons = []
        self._create_dice_buttons()

        # Create confirm button
        confirm_width = 200
        confirm_height = 50
        confirm_x = screen_width // 2 - confirm_width // 2
        confirm_y = screen_height - 100
        self.confirm_button = pygame.Rect(confirm_x, confirm_y, confirm_width, confirm_height)

    def _create_dice_buttons(self):
        """Create button rectangles for each available dice"""
        button_width = 180
        button_height = 120
        margin = 20
        dice_per_row = 4

        start_y = 150

        dice_list = list(self.available_dice.items())

        for i, (dice_key, dice_data) in enumerate(dice_list):
            row = i // dice_per_row
            col = i % dice_per_row

            # Calculate position to center the grid
            total_width = (button_width * dice_per_row) + (margin * (dice_per_row - 1))
            start_x = (self.screen_width - total_width) // 2

            x = start_x + col * (button_width + margin)
            y = start_y + row * (button_height + margin)

            button_rect = pygame.Rect(x, y, button_width, button_height)
            self.dice_buttons.append((button_rect, dice_key, dice_data))

    def handle_click(self, mouse_pos):
        """
        Handle mouse clicks on dice buttons or confirm

        Args:
            mouse_pos: Tuple of (x, y) mouse position

        Returns:
            List of selected dice if confirmed, None otherwise
        """
        # Check if confirm button clicked
        if self.confirm_button.collidepoint(mouse_pos) and len(self.selected_dice) == 3:
            return self.selected_dice

        # Check if a dice button was clicked
        for button_rect, dice_key, dice_data in self.dice_buttons:
            if button_rect.collidepoint(mouse_pos):
                if dice_key in self.selected_dice:
                    # Deselect if already selected
                    self.selected_dice.remove(dice_key)
                elif len(self.selected_dice) < 3:
                    # Select if not at limit
                    self.selected_dice.append(dice_key)
                break

        return None

    def draw(self, screen):
        """
        Draw the dice selection screen

        Args:
            screen: Pygame screen surface to draw on
        """
        screen.fill(self.colors['WHITE'])

        # Draw title
        title = self.fonts['large'].render(f"{self.character.name}: Select 3 Dice", True, self.colors['BLACK'])
        title_rect = title.get_rect(center=(self.screen_width // 2, 50))
        screen.blit(title, title_rect)

        # Draw subtitle
        subtitle_text = f"Selected: {len(self.selected_dice)}/3"
        subtitle = self.fonts['medium'].render(subtitle_text, True, self.colors['BLACK'])
        subtitle_rect = subtitle.get_rect(center=(self.screen_width // 2, 100))
        screen.blit(subtitle, subtitle_rect)

        # Draw dice buttons
        for button_rect, dice_key, dice_data in self.dice_buttons:
            # Determine if this dice is selected
            is_selected = dice_key in self.selected_dice

            # Draw button background
            if is_selected:
                # Highlight selected dice
                button_color = self.colors['BLUE']
                border_color = self.colors['DARK_BLUE']
                border_width = 5
            else:
                button_color = self.colors['LIGHT_GRAY']
                border_color = self.colors['BLACK']
                border_width = 2

            pygame.draw.rect(screen, button_color, button_rect, border_radius=10)
            pygame.draw.rect(screen, border_color, button_rect, border_width, border_radius=10)

            # Draw dice label
            label_text = self.fonts['medium'].render(dice_data['label'], True, self.colors['BLACK'])
            label_rect = label_text.get_rect(center=(button_rect.centerx, button_rect.centery - 30))
            screen.blit(label_text, label_rect)

            # Draw dice values preview (show unique values)
            unique_values = sorted(set(dice_data['values']))
            values_str = ', '.join(map(str, unique_values))
            values_text = self.fonts['small'].render(values_str, True, self.colors['BLACK'])
            values_rect = values_text.get_rect(center=(button_rect.centerx, button_rect.centery))
            screen.blit(values_text, values_rect)

            # Draw damage
            damage_text = self.fonts['small'].render(f"Dmg: {dice_data['damage']}", True, self.colors['BLACK'])
            damage_rect = damage_text.get_rect(center=(button_rect.centerx, button_rect.centery + 25))
            screen.blit(damage_text, damage_rect)

            # Draw selection number if selected
            if is_selected:
                selection_num = self.selected_dice.index(dice_key) + 1
                num_text = self.fonts['large'].render(str(selection_num), True, self.colors['WHITE'])
                num_rect = num_text.get_rect(topright=(button_rect.right - 10, button_rect.top + 10))
                screen.blit(num_text, num_rect)

        # Draw confirm button
        if len(self.selected_dice) == 3:
            button_color = self.colors['GREEN']
            text_color = self.colors['BLACK']
        else:
            button_color = self.colors['LIGHT_GRAY']
            text_color = self.colors['BLACK']

        pygame.draw.rect(screen, button_color, self.confirm_button, border_radius=10)
        pygame.draw.rect(screen, self.colors['BLACK'], self.confirm_button, 3, border_radius=10)

        confirm_text = self.fonts['medium'].render("Confirm Selection", True, text_color)
        confirm_rect = confirm_text.get_rect(center=self.confirm_button.center)
        screen.blit(confirm_text, confirm_rect)