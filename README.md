# Wumpus World Game

## Introduction

This implementation of the classic Wumpus World game, a text-based adventure game, features an intelligent agent designed to optimize and automate gameplay. The agent utilizes various strategies to navigate the grid-based world, make informed decisions, and achieve the game's objectives while avoiding dangers. 

In this game, the agent navigates through a grid-based world containing hazards such as pits and the dangerous Wumpus. The goal is to explore the world, avoid dangers, and collect the gold without getting killed.

## Game Mechanics

### Board

The game world is represented as a grid, and each cell in the grid may contain:

- **Gold (G):** The player's objective is to collect the gold.
- **Wumpus (W):** A dangerous creature that can kill the player.
- **Pit (P):** A hazardous pit that can also be fatal.
  
### Player

The player starts at the bottom-left corner of the grid and can perform the following actions:

- **Move:** The player can move one cell at a time in the four cardinal directions (up, down, left, right).
- **Turn:** The player can turn left or right.
- **Shoot Arrow:** If the player hasn't used their single arrow, they can shoot in the direction they are facing, potentially killing the Wumpus.

### Game Flow

1. The player explores the world, encountering different cells with perceptions.
2. The player decides actions based on perceptions and goals (e.g., shooting the Wumpus, moving to avoid hazards).
3. The game continues until the player collects the gold, gets killed, or reaches a specific score threshold.
4. The player's actions, perceptions, and game state are displayed for each turn.

## Intelligent Agent Features

### Sensory Perception

The agent uses sensory perception to gather information about its surroundings. It can detect:

- **Stench:** Indicates the presence of the Wumpus nearby.
- **Breeze:** Indicates the presence of a pit nearby.
- **Glitter:** Indicates the presence of gold nearby.

### Strategies

1. **Random Movements:** The agent makes random movements to explore the world efficiently, discovering safe paths and avoiding dangers.

2. **Safe Return:** If the agent encounters danger, it employs a strategy to return to a previously visited safe location before continuing exploration.

3. **Optimal Arrow Usage:** The agent strategically uses arrows to eliminate the Wumpus, maximizing its chances of survival.

### Game Automation

The agent automates gameplay by making decisions based on perceptions, current state, and predefined strategies. It aims to optimize its movements, ensuring a higher likelihood of success and minimizing the risk of losing points.

## Classes and Functions Overview

### 1. **Board Class**

#### Attributes:

- `size`: Size of the square grid.
- `grid`: 2D grid representing the world.
- `pygame`: Pygame module for visualization.
- `cell_size`: Size of each cell in the visualization.
- `window_size`: Size of the window.
- `screen`: Pygame display screen.
- `images`: Dictionary containing loaded images for various elements.

#### Methods:

1. `__init__(self, size, pit_probability)`: Constructor to initialize the board with size and pit probability.

2. `createWorld(self, pit_probability)`: Creates the world with gold, wumpus, and pits.

3. `checkLocation(self, x, y)`: Checks if a location (x, y) is valid on the board.

4. `display(self, player)`: Displays the current state of the board.

### 2. **Player Class**

#### Attributes:

- `position`: Current position of the player.
- `orientation`: Current orientation of the player (up, down, left, right).
- `arrow`: Number of arrows the player has.
- `score`: Player's score.
- `action`: Last action performed by the player.
- `visited`: Dictionary to store visited locations and their perceptions.
- `attempted`: Set to store attempted locations.
- `visited_repeat`: List to store repeated visited locations.

#### Methods:

1. `__init__(self)`: Default constructor to initialize player attributes.

2. `turnLeft(self, board)`: Turns the player left based on the current orientation.

3. `turnRight(self, board)`: Turns the player right based on the current orientation.

4. `getPerceptions(self, board)`: Gets perceptions of the current location.

5. `moveForward(self, board)`: Moves the player forward in the current orientation.

6. `shootArrow(self, board, y, x, orientation)`: Shoots an arrow in a specified direction.

7. `returnToDirection(self, destination_y, destination_x, board)`: Determines the direction to reach a specific destination.

8. `randomDirection(self, board)`: Chooses a random direction that hasn't been visited.

9. `turnRandom(self, board, destination=None, return_safe=False)`: Turns randomly towards a specified direction or chooses a random direction.

10. `goToSafe(self, board, clock)`: Moves to the next safe destination.

### 3. **WumpusWorld Class**

#### Attributes:

- `board`: Board object representing the game world.
- `player`: Player object representing the game player.

#### Methods:

1. `__init__(self, size=4, pit_probability=0.2)`: Constructor to initialize the game with a board and a player.

2. `handleDanger(self, perceptions, clock)`: Handles dangerous situations (Stench or Breeze).

3. `play(self)`: Plays the Wumpus World game.

## Object-Oriented Programming Concepts Employed:

1. **Encapsulation:** Each class encapsulates related attributes and methods, ensuring a clear separation of concerns.

2. **Abstraction:** The classes abstract away the complexity of the game mechanics, providing a high-level interface for the user.

## How to Run

Ensure you have Python installed. Run the provided code in a Python environment. The Pygame, Sys and Random libraries are required for visualization and implementation.

```bash
pip install pygame
pip install sys
pip install random
python wumpus_game.py
```


## Enjoy the Game
Watch as the intelligent agent efficiently navigates the Wumpus World, making strategic decisions to achieve its objectives. Enjoy the automated and optimized gameplay experience!