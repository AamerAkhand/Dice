import pygame


class CampaignTeamSelect:
    def __init__(self, screen_width, screen_height, colors, fonts, available_characters):
        """
        Initialize the campaign team selection screen

        Args:
            screen_width: Width of the game window
            screen_height: Height of the game window
            colors: Dictionary of color constants
            fonts: Dictionary of font objects
            available_characters: List of character objects to choose from
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.colors = colors
        self.fonts = fonts
        self.available_characters = available_characters

        # Selected characters (None = not selected yet)
        self.selected_slot_1 = None
        self.selected_slot_2 = None

        # Create character selection buttons
        char_button_width = 200
        char_button_height = 250
        spacing = 50
        start_x = (screen_width - (char_button_width * 2 + spacing)) // 2
        start_y = 200

        self.character_buttons = []
        for i, character in enumerate(available_characters):
            x = start_x + i * (char_button_width + spacing)
            button_rect = pygame.Rect(x, start_y, char_button_width, char_button_height)
            self.character_buttons.append((button_rect, character))

        # Create slot display areas
        slot_width = 300
        slot_height = 80
        slot_x = (screen_width - slot_width) // 2
        slot_1_y = 500
        slot_2_y = 600

        self.slot_1_rect = pygame.Rect(slot_x, slot_1_y, slot_width, slot_height)
        self.slot_2_rect = pygame.Rect(slot_x, slot_2_y, slot_width, slot_height)

        # Create confirm button
        confirm_width = 250
        confirm_height = 60
        confirm_x = (screen_width - confirm_width) // 2
        confirm_y = 720
        self.confirm_button = pygame.Rect(confirm_x, confirm_y, confirm_width, confirm_height)

    def handle_click(self, mouse_pos):
        """
        Check if a character or confirm button was clicked

        Args:
            mouse_pos: Tuple of (x, y) mouse position

        Returns:
            Tuple of (character_1, character_2) if confirm clicked and both slots filled
            None otherwise
        """
        # Check character buttons
        for button_rect, character in self.character_buttons:
            if button_rect.collidepoint(mouse_pos):
                # Assign to first empty slot
                if self.selected_slot_1 is None:
                    self.selected_slot_1 = character
                elif self.selected_slot_2 is None:
                    # Don't allow same character twice
                    if character.name != self.selected_slot_1.name:
                        self.selected_slot_2 = character
                return None

        # Check slot clicks (to deselect)
        if self.slot_1_rect.collidepoint(mouse_pos):
            self.selected_slot_1 = None
            return None

        if self.slot_2_rect.collidepoint(mouse_pos):
            self.selected_slot_2 = None
            return None

        # Check confirm button
        if self.confirm_button.collidepoint(mouse_pos):
            if self.selected_slot_1 is not None and self.selected_slot_2 is not None:
                return (self.selected_slot_1, self.selected_slot_2)

        return None

    def draw(self, screen):
        """
        Draw the team selection screen

        Args:
            screen: Pygame screen surface to draw on
        """
        screen.fill(self.colors['WHITE'])

        # Draw title
        title = self.fonts['large'].render("Select Your Team", True, self.colors['BLACK'])
        title_rect = title.get_rect(center=(self.screen_width // 2, 80))
        screen.blit(title, title_rect)

        # Draw character selection buttons
        for button_rect, character in self.character_buttons:
            # Draw button background
            pygame.draw.rect(screen, self.colors['LIGHT_GRAY'], button_rect, border_radius=10)
            pygame.draw.rect(screen, self.colors['BLACK'], button_rect, 3, border_radius=10)

            # Draw character name
            name_text = self.fonts['medium'].render(character.name, True, self.colors['BLACK'])
            name_rect = name_text.get_rect(center=(button_rect.centerx, button_rect.centery))
            screen.blit(name_text, name_rect)

            # Draw passive description below name
            passive_lines = self._wrap_text(character.passive_description, self.fonts['small'], button_rect.width - 20)
            y_offset = button_rect.centery + 40
            for line in passive_lines:
                passive_text = self.fonts['small'].render(line, True, self.colors['BLACK'])
                passive_rect = passive_text.get_rect(center=(button_rect.centerx, y_offset))
                screen.blit(passive_text, passive_rect)
                y_offset += 25

        # Draw slot 1
        slot_color = self.colors['GREEN'] if self.selected_slot_1 else self.colors['LIGHT_GRAY']
        pygame.draw.rect(screen, slot_color, self.slot_1_rect, border_radius=10)
        pygame.draw.rect(screen, self.colors['BLACK'], self.slot_1_rect, 3, border_radius=10)
        slot_1_text = self.fonts['medium'].render(
            f"Slot 1: {self.selected_slot_1.name if self.selected_slot_1 else 'Empty'}",
            True,
            self.colors['BLACK']
        )
        slot_1_text_rect = slot_1_text.get_rect(center=self.slot_1_rect.center)
        screen.blit(slot_1_text, slot_1_text_rect)

        # Draw slot 2
        slot_color = self.colors['GREEN'] if self.selected_slot_2 else self.colors['LIGHT_GRAY']
        pygame.draw.rect(screen, slot_color, self.slot_2_rect, border_radius=10)
        pygame.draw.rect(screen, self.colors['BLACK'], self.slot_2_rect, 3, border_radius=10)
        slot_2_text = self.fonts['medium'].render(
            f"Slot 2: {self.selected_slot_2.name if self.selected_slot_2 else 'Empty'}",
            True,
            self.colors['BLACK']
        )
        slot_2_text_rect = slot_2_text.get_rect(center=self.slot_2_rect.center)
        screen.blit(slot_2_text, slot_2_text_rect)

        # Draw confirm button (only if both slots filled)
        if self.selected_slot_1 and self.selected_slot_2:
            pygame.draw.rect(screen, self.colors['BLUE'], self.confirm_button, border_radius=10)
            pygame.draw.rect(screen, self.colors['BLACK'], self.confirm_button, 3, border_radius=10)
            confirm_text = self.fonts['medium'].render("Confirm Team", True, self.colors['WHITE'])
            confirm_text_rect = confirm_text.get_rect(center=self.confirm_button.center)
            screen.blit(confirm_text, confirm_text_rect)
        else:
            # Draw grayed out button
            pygame.draw.rect(screen, self.colors['LIGHT_GRAY'], self.confirm_button, border_radius=10)
            pygame.draw.rect(screen, self.colors['BLACK'], self.confirm_button, 3, border_radius=10)
            confirm_text = self.fonts['medium'].render("Select 2 Characters", True, self.colors['BLACK'])
            confirm_text_rect = confirm_text.get_rect(center=self.confirm_button.center)
            screen.blit(confirm_text, confirm_text_rect)

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