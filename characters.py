class Character:
    def __init__(self, name, dice_sets, dice_labels, max_hp, passive_description, base_damage, num_yellow_tiles=1,
                 yellow_icon="lightning.png"):
        self.name = name
        self.dice_sets = dice_sets  # List of 3 dice sets
        self.dice_labels = dice_labels  # List of 3 labels
        self.max_hp = max_hp
        self.passive_description = passive_description
        self.base_damage = base_damage  # Damage dealt to boss on normal tiles
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
            passive_description="Dmg: 15 | No lap damage",
            base_damage=15,
            num_yellow_tiles=4,
            yellow_icon="poison.png"
        )

    def get_lap_damage(self, lap_count, base_lap_damage=None):
        """Huntsman does no lap damage"""
        return 0


# ===== DICE LIBRARY =====
# These dice sets can be used for future characters
# Format: dice_set, label, description

DICE_LIBRARY = {
    'mid': {
        'values': [3, 3, 4, 4, 5, 5],
        'label': 'Mid',
        'description': 'Balanced mid-range movement (3-5)'
    },
    'high': {
        'values': [5, 5, 5, 6, 6, 6],
        'label': 'High',
        'description': 'High movement rolls (5-6)'
    },
    'triple': {
        'values': [3, 3, 3, 3, 3, 3],
        'label': 'Triple',
        'description': 'Consistent 3 movement'
    },
    'even': {
        'values': [2, 4, 6],
        'label': 'Even',
        'description': 'Even numbers only (2, 4, 6)'
    },
    'odd': {
        'values': [1, 3, 5],
        'label': 'Odd',
        'description': 'Odd numbers only (1, 3, 5)'
    },
    'low': {
        'values': [1, 2, 3],
        'label': 'Low',
        'description': 'Low movement rolls (1-3)'
    },
    'four': {
        'values': [4, 4, 4, 4, 4, 4],
        'label': 'Four',
        'description': 'Consistent 4 movement'
    },
    'risk': {
        'values': [-2, -2, 8, 8],
        'label': 'Risk',
        'description': 'High risk, high reward (-2 or 8)'
    },
    'five': {
        'values': [5, 5, 5, 5, 5, 5],
        'label': 'Five',
        'description': 'Consistent 5 movement'
    }
}