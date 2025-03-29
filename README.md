# Turn-Based Fighter Game

This is a Python-based turn-based combat game where players control a team of characters to battle against enemies. Each character and enemy has unique abilities, stats, and conditions that influence the outcome of the fight. Plan your moves carefully to outsmart your opponents and achieve victory.

## Features

- **Turn-Based Combat**: Engage in strategic battles where every decision matters.
- **Unique Abilities**: Characters and enemies can use special abilities with varying damage and mana costs.
- **Dynamic Conditions**: Characters can be stunned, weakened, or set on fire, adding layers of strategy to the gameplay.
- **Customizable Teams**: Choose your team of characters and enemies from JSON-defined files.
- **Randomized Enemy Actions**: Enemies act unpredictably, keeping the gameplay challenging.

## How to Play

1. **Select Your Team**: Choose three characters from the available options.
2. **Select Your Opponents**: Choose three enemies to battle against.
3. **Take Turns**: On your turn, select a character and choose an action:
   - Perform a standard attack.
   - Use one of the character's special abilities.
4. **Manage Resources**: Keep track of health and mana to ensure your characters can continue fighting.
5. **Win or Lose**: Defeat all enemies to win, or lose if all your characters are defeated.

## Directory Structure

- **`main.py`**: The main game logic and entry point.
- **`ability/`**: Contains JSON files defining the abilities available in the game.
- **`characters/`**: Contains JSON files defining the playable characters.
- **`enemy/`**: Contains JSON files defining the enemies you will encounter.

## Key Mechanics

- **Abilities**: Each character and enemy has up to three special abilities, defined in JSON files. Abilities have damage values and mana costs.
- **Conditions**:
  - **Stunned**: The character cannot act during their turn.
  - **On Fire**: The character takes damage at the start of their turn.
  - **Weakened**: The character's attack damage is reduced.
- **Resource Management**: Players must manage health and mana to maximize their effectiveness in battle.

## Example Gameplay

1. The game will prompt you to select characters and enemies from the available JSON files.
2. During your turn, choose a character and an action (standard attack or special ability).
3. Target an enemy and execute your move.
4. Enemies will take their turn, attacking your team with random abilities.
5. The game continues until one side is completely defeated.

## Contributing

Contributions are welcome! If you'd like to improve the game, feel free to fork the repository and submit a pull request.
