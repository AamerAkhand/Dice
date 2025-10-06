import random


def generate_board_positions(square_size, margin, window_height, offset_x=0, offset_y=0):
    """
    Generate positions for a square board forming a 24-tile path
    Layout: 7 tiles bottom, 6 tiles right, 6 tiles top, 5 tiles left

    Args:
        square_size: Size of each square
        margin: Margin from window edges
        window_height: Height of the window
        offset_x: Horizontal offset for the board
        offset_y: Vertical offset for the board

    Returns:
        List of (x, y) tuples for each square position (1-24)
    """
    board_positions = []

    # Define board dimensions (7x7 square board)
    board_width = 7 * square_size
    board_height = 7 * square_size  # Changed from 6 to 7

    # Calculate base position with offsets
    base_x = offset_x + margin
    base_y = offset_y + margin

    # Bottom row (left to right) - squares 1-7 (7 squares)
    for i in range(7):
        x = base_x + i * square_size
        y = base_y + board_height - square_size
        board_positions.append((x, y))

    # Right column (bottom to top, skip bottom corner) - squares 8-13 (6 squares)
    for i in range(1, 7):
        x = base_x + board_width - square_size
        y = base_y + board_height - square_size - i * square_size
        board_positions.append((x, y))

    # Top row (right to left, skip right corner) - squares 14-19 (6 squares)
    for i in range(1, 7):
        x = base_x + board_width - square_size - i * square_size
        y = base_y
        board_positions.append((x, y))

    # Left column (top to bottom, skip both corners) - squares 20-24 (5 squares)
    for i in range(1, 6):
        x = base_x
        y = base_y + i * square_size
        board_positions.append((x, y))

    return board_positions


def generate_green_tiles(num_tiles, excluded_tiles):
    """
    Generate random green tile positions

    Args:
        num_tiles: Number of green tiles to place
        excluded_tiles: List of tile numbers to exclude

    Returns:
        List of tile numbers for green tiles
    """
    available_tiles = [i for i in range(1, 25) if i not in excluded_tiles]
    return random.sample(available_tiles, min(num_tiles, len(available_tiles)))


def generate_red_tiles(num_tiles, excluded_tiles):
    """
    Generate random red tile positions (2 per side, avoiding excluded tiles)

    Args:
        num_tiles: Total number of red tiles (should be 8 for 2 per side)
        excluded_tiles: List of tile numbers to exclude (green tiles)

    Returns:
        List of tile numbers for red tiles
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
            red_tiles.extend(available)

    return sorted(red_tiles)