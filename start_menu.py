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

        # Create buttons
        button_width = 300
        button_height = 80
        button_x = (screen_width - button_width) // 2

        # Start Game button (original flow)
        start_button_y = (screen_height - button_height) // 2 - 60
        self.start_button = pygame.Rect(button_x, start_button_y, button_width, button_height)

        # Campaign Test button (new flow)
        campaign_button_y = start_button_y + button_height + 30
        self.campaign_button = pygame.Rect(button_x, campaign_button_y, button_width, button_height)

    def handle_click(self, mouse_pos):
        """
        Check if start button or campaign button was clicked

        Args:
            mouse_pos: Tuple of (x, y) mouse position

        Returns:
            'start' if start button clicked
            'campaign' if campaign button clicked
            None if neither clicked
        """
        if self.start_button.collidepoint(mouse_pos):
            return 'start'
        elif self.campaign_button.collidepoint(mouse_pos):
            return 'campaign'
        return None

    def draw(self, screen):
        """
        Draw the start menu

        Args:
            screen: Pygame screen surface to draw on
        """
        screen.fill(self.colors['WHITE'])

        # Draw title
        title = self.fonts['large'].render("Monopoly Dice Game", True, self.colors['BLACK'])
        title_rect = title.get_rect(center=(self.screen_width // 2, 150))
        screen.blit(title, title_rect)

        # Draw Start Game button
        pygame.draw.rect(screen, self.colors['BLUE'], self.start_button, border_radius=10)
        pygame.draw.rect(screen, self.colors['BLACK'], self.start_button, 3, border_radius=10)
        start_text = self.fonts['medium'].render("Start Game", True, self.colors['WHITE'])
        start_text_rect = start_text.get_rect(center=self.start_button.center)
        screen.blit(start_text, start_text_rect)

        # Draw Campaign Test button
        pygame.draw.rect(screen, self.colors['PURPLE'], self.campaign_button, border_radius=10)
        pygame.draw.rect(screen, self.colors['BLACK'], self.campaign_button, 3, border_radius=10)
        campaign_text = self.fonts['medium'].render("Campaign (Test)", True, self.colors['WHITE'])
        campaign_text_rect = campaign_text.get_rect(center=self.campaign_button.center)
        screen.blit(campaign_text, campaign_text_rect)