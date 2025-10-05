import random


def generate_board_positions(square_size, board_margin, window_height):
    """
    Generate board square positions (24 squares total, clockwise, 7 per side with shared corners)

    Args:
        square_size: Size of each square
        board_margin: Margin from window edge
        window_height: Height of the window

    Returns:
        List of (x, y) tuples for board positions
    """
    board_positions = []

    # Bottom row (left to right) - squares 1-7 (7 squares)
    for i in range(7):
        x = board_margin + i * square_size
        y = window_height - board_margin - square_size
        board_positions.append((x, y))

    # Right column (bottom to top, skip bottom corner) - squares 8-13 (6 squares)
    for i in range(1, 7):
        x = window_height - board_margin - square_size  # Using window_height for square board
        y = window_height - board_margin - square_size - i * square_size
        board_positions.append((x, y))

    # Top row (right to left, skip right corner) - squares 14-19 (6 squares)
    for i in range(1, 7):
        x = window_height - board_margin - square_size - i * square_size
        y = board_margin
        board_positions.append((x, y))

    # Left column (top to bottom, skip both corners) - squares 20-24 (5 squares)
    for i in range(1, 6):
        x = board_margin
        y = board_margin + i * square_size
        board_positions.append((x, y))

    return board_positions


def generate_green_tiles(num_tiles, excluded_tiles):
    """
    Generate random green tile positions (no restrictions, can be anywhere)

    Args:
        num_tiles: Number of green tiles to generate
        excluded_tiles: List of tiles to exclude from selection

    Returns:
        List of tile numbers (1-24) for green tiles
    """
    available_tiles = [t for t in range(1, 25) if t not in excluded_tiles]
    green_tiles = random.sample(available_tiles, min(num_tiles, len(available_tiles)))
    return sorted(green_tiles)


def generate_red_tiles(num_tiles, excluded_tiles):
    """
    Generate random red tile positions with exactly 2 per side

    Args:
        num_tiles: Number of red tiles to generate (should be 8 for 2 per side)
        excluded_tiles: List of tiles to exclude from selection

    Returns:
        List of tile numbers (1-24) for red tiles
    """
    # Define the four sides
    bottom_side = list(range(1, 8))  # Tiles 1-7
    right_side = list(range(8, 14))  # Tiles 8-13
    top_side = list(range(14, 20))  # Tiles 14-19
    left_side = list(range(20, 25))  # Tiles 20-24

    sides = [bottom_side, right_side, top_side, left_side]

    red_tiles = []

    # Pick exactly 2 from each side
    for side in sides:
        available = [t for t in side if t not in excluded_tiles and t not in red_tiles]
        if len(available) >= 2:
            tiles = random.sample(available, 2)
            red_tiles.extend(tiles)
        elif len(available) > 0:
            # If less than 2 available, take what we can get
            red_tiles.extend(available)
    return sorted(red_tiles)