class Board:
    # Import necessary libraries
    import random
    import sys
    import pygame
    
    # Default constructor initializes the board with size and pit_probability
    def __init__(self, size, pit_probability):
        self.size = size
        self.grid = [[None] * size for _ in range(size)] # 2D grid representing the world
        self.createWorld(pit_probability) # Create the world with given pit probability
        
        # Initialize Pygame
        self.pygame.init()

        # Set up the display
        self.cell_size = 100
        self.window_size = (self.size * self.cell_size, self.size * self.cell_size)
        self.screen = self.pygame.display.set_mode(self.window_size)
        self.pygame.display.set_caption('Wumpus World')

        # Load images
        self.images = {
            'tile': self.pygame.image.load('graphics/tile.png'),
            'gold': self.pygame.image.load('graphics/gold.png'),
            'wumpus': self.pygame.image.load('graphics/wumpus.png'),
            'pit': self.pygame.image.load('graphics/pit.png'),
            'player': self.pygame.image.load('graphics/player.png'),
            'wumpus, pit and gold': self.pygame.image.load('graphics/wumpus_pit_gold.png'),
            'wumpus and gold': self.pygame.image.load('graphics/wumpus_gold.png'),
            'wumpus and pit': self.pygame.image.load('graphics/wumpus_pit.png'),
            'pit and gold': self.pygame.image.load('graphics/pit_gold.png')
        }
        
    # Function to create the world with Gold, Wumpus, and Pits
    def createWorld(self, pit_probability):
        def randomCell(first_row = 0, first_col = 0):
            row, col = (0,0)
            while (row, col) in {(0,0), (0,1), (1,0)}:
                row, col = self.random.randint(first_row, self.size - 1), self.random.randint(first_col, self.size - 1)
            return row, col
        
        # Place the Gold
        gold_row, gold_col = randomCell()
        self.grid[gold_row][gold_col] = ['G']
        
        # Place the Wumpus
        wumpus_row, wumpus_col = randomCell()
        if not self.grid[wumpus_row][wumpus_col]:
            self.grid[wumpus_row][wumpus_col] = ['W']
        else:
            self.grid[wumpus_row][wumpus_col].append('W')
                
        # Place the Pits
        for row in range(self.size - 1):
            for col in range(self.size - 1):
                if (row, col) not in {(0,0), (0,1), (1,0)} and self.random.random() <= pit_probability:
                    if not self.grid[row][col]:
                        self.grid[row][col] = ['P']
                    else:
                        self.grid[row][col].append('P') 
                  
        # Print the world
        for row in reversed(self.grid):
            print(row)
      
    # Function to check if a location (x, y) is valid on the board                  
    def checkLocation(self, x, y):
        return 0 <= x < self.size and 0 <= y < self.size   
    
    # Function to display the current state of the board
    def display(self, player):
        for event in self.pygame.event.get():
            if event.type == self.pygame.QUIT:
                self.pygame.quit()
                self.sys.exit()

        # Draw the background tiles
        for y in range(self.size):
            for x in range(self.size):
                tile = self.pygame.transform.scale(self.images['tile'], (self.cell_size, self.cell_size))
                self.screen.blit(tile, (x * self.cell_size, (self.size - y - 1) * self.cell_size))  
        
        # Draw the elements on top of the background tiles
        for y in range(self.size):
            for x in range(self.size):
                cell_content = self.grid[y][x]

                if cell_content:
                    # Check different combinations of elements and select the corresponding image
                    if 'G' in cell_content and 'W' in cell_content and 'P' in cell_content:
                        image = self.pygame.transform.scale(self.images['wumpus, pit and gold'], (self.cell_size, self.cell_size))
                    elif 'G' in cell_content and 'W' in cell_content:
                        image = self.pygame.transform.scale(self.images['wumpus and gold'], (self.cell_size, self.cell_size))
                    elif 'G' in cell_content and 'P' in cell_content:
                        image = self.pygame.transform.scale(self.images['pit and gold'], (self.cell_size, self.cell_size))
                    elif 'W' in cell_content and 'P' in cell_content:
                        image = self.pygame.transform.scale(self.images['wumpus and pit'], (self.cell_size, self.cell_size))
                    elif 'G' in cell_content:
                        image = self.pygame.transform.scale(self.images['gold'], (self.cell_size, self.cell_size))
                    elif 'W' in cell_content:
                        image = self.pygame.transform.scale(self.images['wumpus'], (self.cell_size, self.cell_size))
                    elif 'P' in cell_content:
                        image = self.pygame.transform.scale(self.images['pit'], (self.cell_size, self.cell_size))
                    else:
                        continue
                        
                    # Draw the image at the current cell
                    self.screen.blit(image, (x * self.cell_size, (self.size - y - 1) * self.cell_size))

        # Draw player
        player_image = self.pygame.transform.scale(self.images['player'], (self.cell_size, self.cell_size))
        self.screen.blit(player_image, (player.position[1] * self.cell_size, (self.size - player.position[0] - 1) * self.cell_size))

        self.pygame.display.flip()      
                        
        

class Player:
    # Import necessary libraries
    import random
    import pygame
    
    # Default constructor initializes player attributes
    def __init__(self):
        self.position = (0, 0)
        self.orientation = 'right'
        self.arrow = 1
        self.score = 0
        self.action = ''
        self.visited = {} # Dictionary to store visited locations and their perceptions
        self.attempted = set() # Set to store attempted locations
        self.visited_repeat = [] # List to store repeated visited locations
        
    # Function to turn the player left based on the current orientation    
    def turnLeft(self, board):
        directions = ['up', 'left', 'down', 'right']
        self.orientation = directions[(directions.index(self.orientation) - 1) % board.size]
        self.score -= 1

    # Function to turn the player right based on the current orientation
    def turnRight(self, board):
        directions = ['up', 'right', 'down', 'left']
        self.orientation = directions[(directions.index(self.orientation) + 1) % board.size]
        self.score -= 1
        
    # Function to get perceptions of the current location
    def getPerceptions(self, board):
        perceptions = []
        y, x = self.position 
        
        # Check adjacent cells for Wumpus, Pit, or Gold and append corresponding perceptions
        for i, j in [(y+1, x), (y-1, x), (y, x+1), (y, x-1)]:
            if board.checkLocation(i,j) and board.grid[i][j] is not None: # 'if and' breaks if the left condition is false
                for p in board.grid[i][j]:
                    if p == 'W':
                        perceptions.append('Stench')
                    elif p == 'P':
                        perceptions.append('Breeze')
                    else:
                        perceptions.append('Glitter')
        return perceptions
        
    # Function to move the player forward in the current orientation
    def moveForward(self, board):
        y, x = self.position
        if self.orientation == 'right':
            x += 1
        elif self.orientation == 'left':
            x -= 1
        elif self.orientation == 'up':
            y += 1
        elif self.orientation == 'down':
            y -= 1

        # Check if the new position is within the valid board range
        if board.checkLocation(y, x):
            self.position = (y, x)
        else:
            # Agent bumps into a wall
            print('\tBump...') # This print statement never executes because of the .checkLocation condition
            
        y, x = self.position
        current_pos = board.grid[y][x]
        
        # Condition to check wether the player encounters a Pit or Wumpus or wins the game
        if current_pos and any(element in ["P", "W"] for element in current_pos):
            print('------- GAME OVER -------')
            self.score -= 1000
        elif current_pos == ['G']:
            print("\t Gold Found!!! YOU WIN")
            board.grid[y][x] = None
            self.score += 1000
    
    # Function to shoot an arrow in a specified direction
    def shootArrow(self, board, y, x, orientation):
        target = board.grid[y][x] # Get the content of the target cell
        self.orientation = orientation # Set the orientation before shooting
        self.arrow -= 1
        
        if target and 'W' in target:
            # Wumpus is killed
            print("\t!!! S C R E A M !!!")
            self.score -= 10
            self.visited[(self.position[0], self.position[1])] = self.getPerceptions(board)
            
            # Remove wumpus from the board
            if len(target) > 1:
                board.grid[y][x].remove('W')
            else:
                board.grid[y][x] = None
                
    # Function to determine the direction to reach a specific destination
    def returnToDirection(self, destination_y, destination_x, board):
        y, x = self.position
        
        # Check if the destination is in one of the adjacent cells and return the corresponding direction
        if (y+1, x) == (destination_y, destination_x):
            return 'up'
        elif (y-1, x) == (destination_y, destination_x):
            return 'down'
        elif (y, x+1) == (destination_y, destination_x):
            return 'right'
        elif (y, x-1) == (destination_y, destination_x):
            return 'left'
        else:
            # If the coordinates don't match, choose a direction based on visited locations
            posible_directions = [(i, j, orientation) for i, j, orientation in [(y+1, x, 'up'), (y-1, x, 'down'), (y, x+1, 'right'), (y, x-1, 'left')] if board.checkLocation(i,j)]
            directions_visited = [(i, j, orientation) for i, j, orientation in posible_directions if (i,j) in self.visited.keys()]
            direction = directions_visited[self.random.randint(0, len(directions_visited) - 1)][2] if directions_visited else posible_directions[self.random.randint(0, len(posible_directions) - 1)][2] 
            
            return direction
          
    # Function to choose a random direction that hasn't been visited  
    def randomDirection(self, board): # If 'bump' is required, then remove 'if board.checkLocation(i,j)'
        y, x = self.position
        posible_directions = [(i, j, orientation) for i, j, orientation in [(y+1, x, 'up'), (y-1, x, 'down'), (y, x+1, 'right'), (y, x-1, 'left')] if board.checkLocation(i,j)]
        directions_not_visited = [(i, j, orientation) for i, j, orientation in posible_directions if (i,j) not in self.visited.keys()]
        direction = directions_not_visited[self.random.randint(0, len(directions_not_visited) - 1)] if directions_not_visited else posible_directions[self.random.randint(0, len(posible_directions) - 1)] 
        
        return direction
    
    # Function to turn randomly towards a specified direction or choose a random direction
    def turnRandom(self, board, destination=None, return_safe=False):
        if return_safe:
            y, x = destination 
            direction = self.returnToDirection(y, x, board)
        else:
            direction = self.randomDirection(board)[2]
        
        # Turn towards the chosen direction
        if self.orientation != direction:
            directions = ['up', 'right', 'down', 'left']
            clockwise = (directions.index(direction) - directions.index(self.orientation)) % board.size
            counterclockwise = (directions.index(self.orientation) - directions.index(direction)) % board.size

            turn = 'right' if clockwise <= counterclockwise else 'left'
            
            # Repeat until orientation is reached based on most efficient turn, clockwise or counterclockwise
            while self.orientation != direction:
                if turn == 'right':
                    self.turnRight(board)
                else:
                    self.turnLeft(board)
         
    # Function to move to the next safe destination           
    def goToSafe(self, board, clock):
        coincidence = False
        
        # Iterate over visited locations to find the next safe destination
        for key in reversed(self.visited_repeat):
            if (not self.visited[key] or 'Glitter' in self.visited[key]) and key not in self.attempted: 
                self.attempted.add(key)
                destination = key
                coincidence = True
                break

        if coincidence:
            # Move to the tile without bad perceptions
            current_y, current_x = self.position

            while (current_y, current_x) != destination:
                # Turn into an already visited location randomly
                self.turnRandom(board, destination, return_safe=True)
                
                # Display the game board and set delay time
                self.pygame.time.delay(1000)
                clock.tick(30)
                self.moveForward(board)
                board.display(self)

                current_y, current_x = self.position           
  
     

class WumpusWorld:
    # Import necessary libraries
    import pygame
    
    # Default constructor initializes the game with a board and a player
    def __init__(self, size = 4, pit_probability = 0.2):
        self.board = Board(size, pit_probability)
        self.player = Player()
        
    # Function to handle dangerous situations (Stench or Breeze)
    def handleDanger(self, perceptions, clock):
        if 'Stench' in perceptions:
            # If Stench is perceived, the player decides whether to shoot or move
            y, x, orientation = self.player.randomDirection(self.board)
            if self.player.arrow > 0:
                # If the player has arrows, shoot the Wumpus
                self.player.action = 'Shoot'
                print("Action:", self.player.action)
                self.player.shootArrow(self.board, y, x, orientation)
            else:
                # If no arrows, attempt to move to a safe location
                if len(self.player.visited) > 1:
                    self.player.goToSafe(self.board, clock)
                self.player.turnRandom(self.board)
                self.player.action = 'MoveForward'
                print("Action:", self.player.action)
                self.player.moveForward(self.board)
        elif 'Breeze' in perceptions:
            # If Breeze is perceived, attempt to move to a safe location
            if len(self.player.visited) > 1:
                self.player.goToSafe(self.board, clock)
            self.player.turnRandom(self.board)
            self.player.action = 'MoveForward'
            print("Action:", self.player.action)
            self.player.moveForward(self.board)
       
    # Function to play the Wumpus World game
    def play(self):
        # Initialize the Pygame clock for controlling the frame rate
        clock = self.pygame.time.Clock()
        
        # The main game loop
        while True: 
            # Get the perceptions of the player based on the current position on the board
            perceptions = self.player.getPerceptions(self.board)
            
            # Display the current state of the game
            self.board.display(self.player)
            
            # Update the information about the visited tiles and perceptions
            current_tile = (self.player.position[0], self.player.position[1])
            self.player.visited[current_tile] = perceptions
            self.player.visited_repeat.append(current_tile)
            
            # Print the current state of the game
            print("\n-----------------\n")
            print("\tCurrent State:")
            print("Player Position:", self.player.position)
            print("Perceptions:", perceptions)
            
            if 'Glitter' in perceptions:
                # If glitter is perceived, check for potential danger before grabbing the gold
                if 'Breeze' in perceptions or 'Stench' in perceptions:
                    self.handleDanger(perceptions, clock)
                # If it's safe, turn randomly and move forward to grab the gold
                else:
                    self.player.turnRandom(self.board)
                    self.action = 'MoveForward'
                    print("Action:", self.action)
                    self.player.moveForward(self.board)
                          
            # Check for dangerous situations (Pit or Wumpus)
            elif 'Breeze' in perceptions or 'Stench' in perceptions:
                self.handleDanger(perceptions, clock)
            # If no danger, move randomly
            else:
                self.player.turnRandom(self.board)
                self.player.action = 'MoveForward'
                print("Action:", self.player.action)
                self.player.moveForward(self.board)
            
            # Print the current orientation and score of the player
            print('Orientation:', self.player.orientation)
            print("Score:", self.player.score)
            
            # Add a delay to visualize the game and cap the frame rate to 30 frames per second
            self.pygame.time.delay(1000)
            clock.tick(30) 
            
            # Check for the end conditions of the game (win or lose)
            if not (900 > self.player.score > -1000):
                # If the game is over, show the final sequence and break out of the loop
                self.board.display(self.player)
                self.pygame.time.delay(2000)  
                break     


# Initialize the game and play                        
world = WumpusWorld()
world.play()