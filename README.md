# Tetris game
[![License: MIT](https://img.shields.io/badge/License-MIT-lightgrey.svg)](https://opensource.org/licenses/MIT)
## 🔍 Overview
This project is a complete implementation of the classic Tetris game using Python and the Pygame library. The game features all the standard Tetris mechanics including piece rotation, movement, hard and soft drops, line clearing, and increasing difficulty levels.

## 🧩 Features
- Complete Tetris gameplay mechanics
- Piece shadow to help with placement
- Score system with level progression
- Next piece preview
- Game over and restart functionality
- Start screen with game rules

## 🎮 Controls

- `Left Arrow`: Move piece left
- `Right Arrow`: Move piece right
- `Up Arrow`: Rotate piece
- `Down Arrow`: Soft drop (accelerate piece downward)
- `Space`: Hard drop (instantly drop piece to bottom)
- `Escape`: Quit game
- `R`: View rules (on start screen)

## 🏆 Scoring system

- **Single line clear**: 40 × level
- **Double line clear**: 100 × level
- **Triple line clear**: 300 × level
- **Tetris (four lines)**: 1200 × level
- **Soft drop**: 1 point per cell
- **Hard drop**: Points equal to the number of cells the piece drops

The game level increases after every 10 lines cleared. As the level increases, pieces fall faster, making the game more challenging.

## 🛠️ Installation
### Prerequisites
- Python 3.x
- Pygame library

### Setup
1. Clone the repository:
   ```
   git clone https://github.com/charlottekruzic/pygame-tetris.git
   cd tetris
   ```
2. Install the required dependencies:
   ```
   pip install pygame
   ```
3. Run the game:
   ```
   python main.py
   ```

## 📐 Project structure
- `main.py`: Entry point for the game
- `src/tetris.py`: Main game class containing the game loop and rendering functions
- `src/grid.py`: Grid class for managing the game board
- `src/piece.py`: Piece class for handling Tetris pieces and their movements
