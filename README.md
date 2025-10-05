<<<<<<< HEAD
# Test
=======
# Dice

```markdown
# Monopoly Dice Game

A turn-based board game where you battle a boss by moving around a board using custom dice.

## Features

- **Two playable characters:**
  - **Lapper:** High lap damage with balanced dice
  - **Huntsman:** No lap damage but more strategic options

- **Special tile system:**
  - Green tiles: Heal HP and clear debuffs
  - Red tiles: Apply debuff stacks
  - Yellow tiles: Choose between Double Movement or Poison Strike

- **Custom dice mechanics:** Each character has unique dice sets
- **Boss battle system:** Strategic turn-based combat

## Requirements

- Python 3.13+
- Pygame

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/monopoly-dice-game.git
cd monopoly-dice-game
```

2. Install pygame:
```bash
pip install pygame
```

3. Run the game:
```bash
python main.py
```

## How to Play

1. Select your character
2. Choose your yellow tile effect (Double Movement or Poison Strike)
3. Place your yellow tiles on the board
4. Click dice to roll and move around the board
5. Land on special tiles for effects
6. Complete laps to deal bonus damage (Lapper only)
7. Defeat the boss!

## Controls

- **Mouse:** Click to select options and roll dice

## Assets Required

Make sure these image files are in the same directory:
- `fire.png`
- `heal.png`
- `lightning.png`
- `poison.png`

## File Structure

```
monopoly-dice-game/
├── main.py
├── characters.py
├── board.py
├── battle_renderer.py
├── character_select.py
├── yellow_tile_select.py
├── start_menu.py
├── ui_constants.py
├── fire.png
├── heal.png
├── lightning.png
├── poison.png
└── README.md
```
>>>>>>> 1d96257ad31b75f6dc56d5c66030f4399f81ea02
