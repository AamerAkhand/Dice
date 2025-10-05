import pygame

# Initialize pygame to create fonts
pygame.init()

# ===== COLORS =====
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (100, 150, 255)
DARK_BLUE = (70, 120, 200)
GREEN = (100, 200, 100)
BROWN = (139, 69, 19)
RED = (255, 50, 50)
DARK_RED = (180, 0, 0)
LIGHT_GRAY = (200, 200, 200)
PURPLE = (150, 100, 255)
DARK_PURPLE = (120, 70, 200)
ORANGE = (255, 150, 50)
DARK_ORANGE = (200, 120, 30)
DARK_GREEN = (0, 100, 0)
YELLOW = (255, 255, 0)
DARK_YELLOW = (200, 200, 0)

# ===== FONTS =====
FONT_LARGE = pygame.font.Font(None, 60)
FONT_SMALL = pygame.font.Font(None, 24)
FONT_MEDIUM = pygame.font.Font(None, 36)
FONT_TINY = pygame.font.Font(None, 18)

# ===== FONT DICTIONARY =====
fonts = {
    'large': FONT_LARGE,
    'medium': FONT_MEDIUM,
    'small': FONT_SMALL,
    'tiny': FONT_TINY
}

# ===== COLOR DICTIONARY =====
colors = {
    'WHITE': WHITE,
    'BLACK': BLACK,
    'GREEN': GREEN,
    'RED': RED,
    'DARK_RED': DARK_RED,
    'LIGHT_GRAY': LIGHT_GRAY,
    'DARK_GREEN': DARK_GREEN,
    'YELLOW': YELLOW,
    'DARK_YELLOW': DARK_YELLOW,
    'DARK_BLUE': DARK_BLUE,
    'BLUE': BLUE,
    'PURPLE': PURPLE,
    'ORANGE': ORANGE,
    'DARK_PURPLE': DARK_PURPLE,
    'DARK_ORANGE': DARK_ORANGE
}