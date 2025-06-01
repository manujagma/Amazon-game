# Space Shooter Game

A 2D space shooter game with two game modes built using Pygame.

## Requirements

- Python 3.x
- Pygame library

To install Pygame:
```
pip install pygame
```

## How to Play

1. Run the game:
```
python main.py
```

2. Select a game mode from the main menu:
   - **Classic Mode**: Complete the game by destroying the final boss
   - **Unlimited Mode**: Play endlessly to achieve a high score

3. Controls:
   - Arrow keys: Move your spaceship
   - Spacebar: Shoot
   - R: Restart after game over
   - M: Return to main menu after game over

## Game Features

### Classic Mode
- Regular enemies appear from the top
- Mother ship appears at score 150 (fires single bullets)
- Advanced ship appears at score 300 (fires triple bullets)
- Big mother ship appears at score 500 (fires splitting bullets)
- Win by destroying the big mother ship

### Unlimited Mode
- Regular enemies appear continuously
- Mother ship appears at score 50
- Advanced ship appears at score 100
- Play until you lose

## Files
- `main.py`: Main menu and game launcher
- `classic_mode.py`: Classic game mode implementation
- `unlimited_mode.py`: Unlimited game mode implementation