import pygame


class CharacterSelect:
    def __init__(self, screen_width, screen_height, colors, fonts, characters):
        """
        Initialize the character selection screen

        Args:
            screen_width: Width of the game window
            screen_height: Height of the game window
            colors: Dictionary of color constants
            fonts: Dictionary of font objects
            characters: List of character instances available to select
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.colors = colors
        self.fonts = fonts
        self.characters = characters

        # Create character selection buttons
        self.character_buttons = []
        button_width = 250
        button_height = 150
        spacing = 50
        total_width = (button_width * len(characters)) + (spacing * (len(characters) - 1))
        start_x = (screen_width - total_width) // 2
        button_y = screen_height // 2 - button_height // 2

        for i, character in enumerate(characters):
            button_x = start_x + (i * (button_width + spacing))
            button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
            self.character_buttons.append((button_rect, character))

    def handle_click(self, mouse_pos):
        """
        Check if a character was clicked

        Args:
            mouse_pos: Tuple of (x, y) mouse position

        Returns:
            Selected character instance if clicked, None otherwise
        """
        for button_rect, character in self.character_buttons:
            if button_rect.collidepoint(mouse_pos):
                return character
        return None

    def draw(self, screen):
        """
        Draw the character selection screen

        Args:
            screen: Pygame screen surface to draw on
        """
        screen.fill(self.colors['WHITE'])

        # Draw title
        title = self.fonts['large'].render("Choose Your Character", True, self.colors['BLACK'])
        title_rect = title.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 200))
        screen.blit(title, title_rect)

        # Draw character buttons
        for button_rect, character in self.character_buttons:
            # Draw button background
            pygame.draw.rect(screen, self.colors['LIGHT_GRAY'], button_rect, border_radius=10)
            pygame.draw.rect(screen, self.colors['BLACK'], button_rect, 3, border_radius=10)

            # Draw character name
            name_text = self.fonts['medium'].render(character.name, True, self.colors['BLACK'])
            name_rect = name_text.get_rect(center=(button_rect.centerx, button_rect.centery - 40))
            screen.blit(name_text, name_rect)

            # Draw character stats (HP)
            hp_text = self.fonts['small'].render(f"HP: {character.max_hp}", True, self.colors['BLACK'])
            hp_rect = hp_text.get_rect(center=(button_rect.centerx, button_rect.centery))
            screen.blit(hp_text, hp_rect)

            # Draw character damage
            damage_text = self.fonts['small'].render(f"Damage: {character.base_damage}", True, self.colors['BLACK'])
            damage_rect = damage_text.get_rect(center=(button_rect.centerx, button_rect.centery + 25))
            screen.blit(damage_text, damage_rect)

            # Draw dice info
            dice_info = " | ".join(character.dice_labels)
            dice_text = self.fonts['small'].render(dice_info, True, self.colors['DARK_BLUE'])
            dice_rect = dice_text.get_rect(center=(button_rect.centerx, button_rect.centery + 50))
            screen.blit(dice_text, dice_rect)