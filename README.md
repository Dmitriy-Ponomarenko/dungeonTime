# dungeonTime 2D Dungeon Game

## Overview
dungeonTime is a 2D dungeon game where players can explore, battle enemies, and complete quests. The game features a simple yet engaging gameplay loop, allowing players to immerse themselves in a dungeon-crawling experience.

## Project Structure
```
dungeon_game
├── src
│   ├── main.py          # Entry point of the game
│   ├── characters       # Contains character-related classes
│   │   ├── character.py # Character class definition
│   │   └── enemy.py     # Enemy class definition
│   ├── quests           # Contains quest-related classes
│   │   └── quest.py     # Quest class definition
│   ├── map              # Contains map-related classes
│   │   └── layout.py    # Map layout class definition
│   └── utils            # Utility functions and constants
│       └── __init__.py  # Initialization for utils
├── requirements.txt     # Project dependencies
└── README.md            # Project documentation
```

## Installation
To set up the project, clone the repository and install the required dependencies:

```bash
git clone <repository-url>
cd dungeon_game
pip install -r requirements.txt
```

## Features
- **Character System**: Create and manage characters with health and attack capabilities.
- **Enemy Encounters**: Engage with various enemies that challenge the player.
- **Quest System**: Complete quests to progress through the game.
- **Dynamic Map**: Explore a generated dungeon map with various layouts.

## Usage
Run the game by executing the main script:

```bash
python src/main.py
```

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any suggestions or improvements.