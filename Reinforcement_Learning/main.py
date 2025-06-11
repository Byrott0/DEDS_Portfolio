import pygame
import numpy as np
import random
import sys

# Initialize pygame immediately after import
pygame.init()

class Maze:
    def __init__(self, size=(20, 20), start=(0, 0), goal=(19, 19)):
        self.size = size
        self.start = start
        self.goal = goal
        self.state = start
        self.actions = ['up', 'down', 'left', 'right']
        
        # Initialize grid with different cell types
        # 0 = empty space, 1 = wall, 2 = hazard, 3 = goal
        self.grid = np.zeros(size, dtype=int)
        
        # Set goal cell
        self.grid[goal] = 3
        
        # Generate walls randomly (about 20% of the grid)
        self._generate_walls()
        
        # Generate hazards randomly (about 10% of the grid)
        self._generate_hazards()
        
        # Ensure start position is always free
        self.grid[start] = 0

    def _generate_walls(self):
        """Generate random walls in the maze"""
        wall_count = int(self.size[0] * self.size[1] * 0.2)
        positions = [(x, y) for x in range(self.size[0]) for y in range(self.size[1]) 
                    if (x, y) != self.start and (x, y) != self.goal]
        
        wall_positions = random.sample(positions, min(wall_count, len(positions)))
        for x, y in wall_positions:
            self.grid[x, y] = 1

    def _generate_hazards(self):
        """Generate random hazards in the maze"""
        hazard_count = int(self.size[0] * self.size[1] * 0.1)
        positions = [(x, y) for x in range(self.size[0]) for y in range(self.size[1]) 
                    if self.grid[x, y] == 0 and (x, y) != self.start and (x, y) != self.goal]
        
        if positions:
            hazard_positions = random.sample(positions, min(hazard_count, len(positions)))
            for x, y in hazard_positions:
                self.grid[x, y] = 2

    def reset(self):
        self.state = self.start
        return self.state

    def is_valid_position(self, x, y):
        """Check if position is within bounds and not a wall"""
        return (0 <= x < self.size[0] and 
                0 <= y < self.size[1] and 
                self.grid[x, y] != 1)  # Not a wall

    def step(self, action):
        x, y = self.state
        new_x, new_y = x, y
        
        if action == 'up':
            new_x = x - 1
        elif action == 'down':
            new_x = x + 1
        elif action == 'left':
            new_y = y - 1
        elif action == 'right':
            new_y = y + 1

        # Check if new position is valid (not out of bounds or a wall)
        if self.is_valid_position(new_x, new_y):
            self.state = (new_x, new_y)
        # If invalid, agent stays in current position

        # Calculate reward based on cell type
        cell_type = self.grid[self.state]
        
        if self.state == self.goal:
            return self.state, 10.0, True  # Large positive reward for reaching goal
        elif cell_type == 2:  # Hazard
            return self.state, -1.0, False  # Penalty for stepping on hazard
        else:  # Empty space
            return self.state, -0.01, False  # Small penalty to encourage shorter paths

class QLearningAgent:
    def __init__(self, env, alpha=0.9, gamma=0.95, epsilon=0.1):
        self.env = env
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.q_table = {}

        # Initialize Q-table for all valid states
        for x in range(env.size[0]):
            for y in range(env.size[1]):
                if env.grid[x, y] != 1:  # Don't initialize Q-values for walls
                    self.q_table[(x, y)] = {action: 0.0 for action in env.actions}

    def choose_action(self, state):
        if random.random() < self.epsilon:
            return random.choice(self.env.actions)
        else:
            if state in self.q_table:
                return max(self.q_table[state], key=self.q_table[state].get)
            else:
                return random.choice(self.env.actions)

    def update_q_value(self, state, action, reward, next_state):
        if state in self.q_table and next_state in self.q_table:
            best_next_action = max(self.q_table[next_state], key=self.q_table[next_state].get)
            target = reward + self.gamma * self.q_table[next_state][best_next_action]
            self.q_table[state][action] += self.alpha * (target - self.q_table[state][action])

    def train(self, episodes=1000):
        for episode in range(episodes):
            state = self.env.reset()
            done = False
            steps = 0
            max_steps = 200  # Prevent infinite episodes

            while not done and steps < max_steps:
                action = self.choose_action(state)
                next_state, reward, done = self.env.step(action)
                self.update_q_value(state, action, reward, next_state)
                state = next_state
                steps += 1

class PygameMaze:
    def __init__(self, maze, agent, cell_size=30):
        self.maze = maze
        self.agent = agent
        self.cell_size = cell_size
        self.width = maze.size[1] * cell_size
        self.height = maze.size[0] * cell_size
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Q-Learning Maze with Walls and Hazards")
        self.clock = pygame.time.Clock()
        self.path = []
        
        # Colors for different cell types
        self.colors = {
            'empty': (200, 200, 200),    # Gray for empty spaces
            'wall': (0, 0, 0),           # Black for walls
            'hazard': (255, 0, 0),       # Red for hazards
            'goal': (0, 255, 0),         # Green for goal
            'agent': (0, 0, 255),        # Blue for agent
            'path': (100, 100, 255)      # Light blue for path
        }

    def draw_grid(self):
        """Draw the maze grid with different cell types"""
        for x in range(self.maze.size[0]):
            for y in range(self.maze.size[1]):
                rect = pygame.Rect(y * self.cell_size, x * self.cell_size, 
                                 self.cell_size, self.cell_size)
                
                # Choose color based on cell type
                cell_type = self.maze.grid[x, y]
                if cell_type == 1:  # Wall
                    color = self.colors['wall']
                elif cell_type == 2:  # Hazard
                    color = self.colors['hazard']
                elif cell_type == 3:  # Goal
                    color = self.colors['goal']
                else:  # Empty space
                    color = self.colors['empty']
                
                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, (100, 100, 100), rect, 1)  # Grid lines

    def draw_path(self):
        """Draw the agent's path"""
        for i, (x, y) in enumerate(self.path[:-1]):  # Don't draw over current position
            rect = pygame.Rect(y * self.cell_size + 5, x * self.cell_size + 5, 
                             self.cell_size - 10, self.cell_size - 10)
            pygame.draw.rect(self.screen, self.colors['path'], rect)

    def draw_agent(self):
        """Draw the agent at current position"""
        x, y = self.maze.state
        rect = pygame.Rect(y * self.cell_size + 3, x * self.cell_size + 3, 
                         self.cell_size - 6, self.cell_size - 6)
        pygame.draw.rect(self.screen, self.colors['agent'], rect)

    def run(self):
        running = True
        state = self.maze.reset()
        self.path = [state]
        total_reward = 0

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            action = self.agent.choose_action(state)
            next_state, reward, done = self.maze.step(action)
            total_reward += reward
            
            if next_state != state:  # Only add to path if agent actually moved
                self.path.append(next_state)

            # Draw everything
            self.screen.fill((255, 255, 255))  # White background
            self.draw_grid()
            self.draw_path()
            self.draw_agent()
            pygame.display.flip()

            self.clock.tick(10)  # Slightly faster visualization

            if done:
                print(f"Goal reached! Total reward: {total_reward:.2f}, Steps: {len(self.path)}")
                pygame.time.wait(2000)  # Wait 2 seconds before reset
                state = self.maze.reset()
                self.path = [state]
                total_reward = 0
            else:
                state = next_state

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    # Create maze with random walls and hazards
    maze = Maze(size=(15, 15), start=(0, 0), goal=(14, 14))
    agent = QLearningAgent(maze, alpha=0.1, gamma=0.95, epsilon=0.1)

    print("Training Q-learning agent...")
    print("Grid legend:")
    print("- Black squares: Walls (impassable)")
    print("- Red squares: Hazards (penalty: -1.0)")
    print("- Green square: Goal (reward: +10.0)")
    print("- Gray squares: Empty spaces (penalty: -0.01)")
    print("- Blue circle: Agent")
    print("- Light blue trail: Agent's path")
    
    agent.train(episodes=2000)
    print("Training completed!")

    print("Launching Pygame visualization...")
    game = PygameMaze(maze, agent)
    game.run()