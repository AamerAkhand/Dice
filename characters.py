class Character:
    def __init__(self, name, dice_sets, dice_labels, max_hp, passive_description, base_damage, num_yellow_tiles=1,
                 yellow_icon="lightning.png"):
        self.name = name
        self.dice_sets = dice_sets  # List of 3 dice sets
        self.dice_labels = dice_labels  # List of 3 labels
        self.dice_damage = [base_damage, base_damage, base_damage]  # Damage for each dice (will be updated)
        self.max_hp = max_hp
        self.passive_description = passive_description
        self.base_damage = base_damage  # Damage dealt to boss on normal tiles (fallback)
        self.num_yellow_tiles = num_yellow_tiles  # Number of yellow tiles to place
        self.yellow_icon = yellow_icon  # Icon to use for yellow tiles
        self.yellow_effect = None  # Will be set by player choice

    def get_lap_damage(self, lap_count, base_lap_damage):
        """Calculate lap damage - can be overridden by subclasses. Default is 0 (no lap damage)"""
        return 0

    def yellow_tile_effect(self):
        """Effect when landing on yellow tile - returns the chosen effect"""
        return self.yellow_effect if self.yellow_effect else "double_movement"

    def set_yellow_effect(self, effect, icon):
        """Set the yellow tile effect chosen by the player"""
        self.yellow_effect = effect
        self.yellow_icon = icon

    def get_yellow_tile_damage(self):
        """Get bonus damage when landing on yellow tiles - can be overridden by subclasses"""
        return 0


class Lapper(Character):
    def __init__(self):
        super().__init__(
            name="Lapper",
            dice_sets=[
                [3, 3, 4, 4, 5, 5],
                [5, 5, 5, 6, 6, 6],
                [-2, -2, 8, 8]
            ],
            dice_labels=["Mid", "High", "Risk"],
            max_hp=100,
            passive_description="Lap: 15 * count | Dmg: 15",
            base_damage=15,
            num_yellow_tiles=1,
            yellow_icon="lightning.png"
        )
        self.available_dice = ['risk', 'low', 'heavy', 'swift', 'double', 'chaos']

    def get_lap_damage(self, lap_count, base_lap_damage=None):
        """Lapper does 15 damage per lap count"""
        return 15 * lap_count


class Huntsman(Character):
    def __init__(self):
        super().__init__(
            name="Huntsman",
            dice_sets=[
                [2, 4, 6],
                [1, 3, 5],
                [1, 2, 3]
            ],
            dice_labels=["Even", "Odd", "Low"],
            max_hp=100,
            passive_description="Dmg: 15 | Yellow: 30 dmg | No lap",
            base_damage=15,
            num_yellow_tiles=4,
            yellow_icon="poison.png"
        )
        self.available_dice = ['risk', 'low', 'heavy', 'swift', 'double', 'chaos', 'five']

    def get_lap_damage(self, lap_count, base_lap_damage=None):
        """Huntsman does no lap damage"""
        return 0

    def get_yellow_tile_damage(self):
        """Huntsman deals 30 damage when landing on ANY yellow tile"""
        return 30


# ===== DICE LIBRARY =====
# These dice sets can be used for future characters
# Format: values, label, description, damage, allowed_for

DICE_LIBRARY = {
    'mid': {
        'values': [3, 3, 4, 4, 5, 5],
        'label': 'Mid',
        'description': 'Balanced mid-range movement (3-5)',
        'damage': 15,
        'allowed_for': ['all']
    },
    'high': {
        'values': [5, 5, 5, 6, 6, 6],
        'label': 'High',
        'description': 'High movement rolls (5-6)',
        'damage': 15,
        'allowed_for': ['Lapper']
    },
    'triple': {
        'values': [3, 3, 3, 3, 3, 3],
        'label': 'Triple',
        'description': 'Consistent 3 movement',
        'damage': 15,
        'allowed_for': ['Huntsman']
    },
    'even': {
        'values': [2, 4, 6],
        'label': 'Even',
        'description': 'Even numbers only (2, 4, 6)',
        'damage': 15,
        'allowed_for': ['all']
    },
    'odd': {
        'values': [1, 3, 5],
        'label': 'Odd',
        'description': 'Odd numbers only (1, 3, 5)',
        'damage': 15,
        'allowed_for': ['all']
    },
    'low': {
        'values': [1, 2, 3],
        'label': 'Low',
        'description': 'Low movement rolls (1-3)',
        'damage': 15,
        'allowed_for': ['all']
    },
    'four': {
        'values': [4, 4, 4, 4, 4, 4],
        'label': 'Four',
        'description': 'Consistent 4 movement',
        'damage': 15,
        'allowed_for': ['Huntsman']
    },
    'risk': {
        'values': [-2, -2, 8, 8],
        'label': 'Risk',
        'description': 'High risk, high reward (-2 or 8)',
        'damage': 15,
        'allowed_for': ['Lapper']
    },
    'five': {
        'values': [5, 5, 5, 5, 5, 5],
        'label': 'Five',
        'description': 'Consistent 5 movement',
        'damage': 15,
        'allowed_for': ['Huntsman']
    },
    'heavy': {
        'values': [1, 1, 2, 2, 3, 3],
        'label': 'Heavy',
        'description': 'Slow movement, high damage',
        'damage': 25,
        'allowed_for': ['all']
    },
    'swift': {
        'values': [4, 5, 6, 7, 8],
        'label': 'Swift',
        'description': 'Fast movement, low damage',
        'damage': 8,
        'allowed_for': ['all']
    },
    'critical': {
        'values': [2, 2, 3, 3, 3, 3],
        'label': 'Critical',
        'description': 'Consistent movement, critical chance',
        'damage': 20,
        'allowed_for': ['all']
    },
    'chaos': {
        'values': [-3, 1, 1, 6, 9, 12],
        'label': 'Chaos',
        'description': 'Completely random',
        'damage': 18,
        'allowed_for': ['all']
    },
    'double': {
        'values': [2, 2, 4, 4, 6, 6],
        'label': 'Double',
        'description': 'All even numbers',
        'damage': 15,
        'allowed_for': ['all']
    }
}


def get_available_dice(character_name):
    """
    Get all dice available to a specific character

    Args:
        character_name: Name of the character (e.g., 'Lapper', 'Huntsman')

    Returns:
        Dictionary of available dice for that character
    """
    available = {}
    for dice_key, dice_data in DICE_LIBRARY.items():
        allowed = dice_data.get('allowed_for', [])
        if 'all' in allowed or character_name in allowed:
            available[dice_key] = dice_data
    return available