import pygame


class StartMenu:
    def __init__(self, screen_width, screen_height, colors, fonts):
        """
        Initialize the start menu

        Args:
            screen_width: Width of the game window
            screen_height: Height of the game window
            colors: Dictionary of color constants
            fonts: Dictionary of font objects
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.colors = colors
        self.fonts = fonts

        # Create start button
        self.button_rect = pygame.Rect(
            screen_width // 2 - 100,
            screen_height // 2 - 30,
            200,
            60
        )

    def handle_click(self, mouse_pos):
        """
        Check if start button was clicked

        Args:
            mouse_pos: Tuple of (x, y) mouse position

        Returns:
            True if start button was clicked, False otherwise
        """
        return self.button_rect.collidepoint(mouse_pos)

    def draw(self, screen):
        """
        Draw the start menu screen

        Args:
            screen: Pygame screen surface to draw on
        """
        screen.fill(self.colors['WHITE'])

        # Draw title
        title = self.fonts['large'].render("Dice Battle", True, self.colors['BLACK'])
        title_rect = title.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 150))
        screen.blit(title, title_rect)

        # Draw start button
        pygame.draw.rect(screen, self.colors['GREEN'], self.button_rect, border_radius=10)
        pygame.draw.rect(screen, self.colors['BLACK'], self.button_rect, 3, border_radius=10)

        # Draw button text
        button_text = self.fonts['medium'].render("Begin Game", True, self.colors['BLACK'])
        button_text_rect = button_text.get_rect(center=self.button_rect.center)
        screen.blit(button_text, button_text_rect)