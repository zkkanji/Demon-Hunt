# Demon Hunt

A pixel-art, wave-based arena game built with Python and Pygame.

This project started as an experiment in making a game from scratch and has
grown into a playable combat loop with animated enemies, multiple weapon types,
upgrade choices, power-ups, a stash screen, custom UI, and original game art.

## Features

- Survive waves of demons in a top-down arena.
- Fight with ranged and melee weapons:
  - Blaster
  - Shotgun
  - Sword
  - Boomerang
- Face three enemy types with different attack behaviors.
- Choose an upgrade after clearing a wave.
- Improve health, weapon damage, magazine size, melee range, and critical hits.
- Collect and use power-ups, including:
  - Invincibility
  - Speed boost
  - Bombs
- Collect enemy drops and manage weapons and upgrades through the stash.
- Use animated pixel-art characters, particles, health bars, damage numbers,
  custom reticles, and menu screens.
- Pause, restart after defeat, and view the controls and credits in-game.

## Requirements

- Python 3
- Pygame

The game currently uses a fixed 1000 x 700 window and targets 60 FPS.

## Getting Started

Clone the repository and move into the project directory:

```bash
git clone https://github.com/zkkanji/first_game.git
cd first_game
```

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows, activate the environment with:

```powershell
.venv\Scripts\activate
```

Install Pygame:

```bash
python -m pip install pygame
```

Start the game:

```bash
python main.py
```

To skip the title screen and start directly in the arena:

```bash
python main.py --start-game
```

Run commands from the repository root so the game can find its `assets/` and
`src/` directories.

## Controls

| Action | Input |
| --- | --- |
| Move | `W` `A` `S` `D` |
| Aim | Mouse |
| Attack | `Space` |
| Reload | `R` |
| Equip ranged weapon | `1` |
| Equip melee weapon | `2` |
| Use held power-up | `E` |
| Pause / resume | `Escape` |

Automatic weapons fire while Space is held. Melee weapons use one attack per
Space press.

## Project Structure

```text
.
├── main.py                 # Game loop, states, input, and rendering
├── src/
│   ├── entities/           # Player, enemies, drops, and combat entities
│   ├── weapons/            # Blaster, shotgun, sword, and boomerang
│   ├── menu_stuff/         # Menus, buttons, and menu text
│   ├── utils/              # UI, upgrades, power-ups, particles, and assets
│   ├── constants.py        # Display and timing constants
│   └── game.py             # Waves, score, collisions, and shared game logic
└── assets/                 # Sprites, animations, fonts, and UI artwork
```

## Development

The game is intentionally built from small, focused modules so new weapons,
enemies, upgrades, and visual effects can be added independently. Most gameplay
configuration lives in `src/constants.py` and `src/game.py`; the main loop and
game-state transitions are in `main.py`.

There is currently no automated test suite. The primary validation workflow is
to launch the game, play through a wave, test the controls, and verify each
menu and upgrade screen.

## Credits

Code, graphics, animations, and sound by **Zain Kanji**.
