import pygame
import numpy as np
import random
import sys

pygame.init()

class Maze:
    def __init__(self, size=(20, 20), start=(0, 0), goal=(19, 19)):
        self.size = size
        self.start = start
        self.goal = goal
        self.state = start
        self.actions = ['up', 'down', 'left', 'right']
        

        self.grid = np.zeros(size, dtype=int)
        

        self.grid[goal] = 3
        

        self._generate_walls()
        

        self._generate_hazards()
        

        self.grid[start] = 0

    def _generate_walls(self):
        """Generate random walls in the maze"""
        wall_count = int(self.size[0] * self.size[1] * 0.15)
        positions = [(x, y) for x in range(self.size[0]) for y in range(self.size[1]) 
                    if (x, y) != self.start and (x, y) != self.goal]
        
        wall_positions = random.sample(positions, min(wall_count, len(positions)))
        for x, y in wall_positions:
            self.grid[x, y] = 1

    def _generate_hazards(self):
        """Generate random hazards in the maze"""
        hazard_count = int(self.size[0] * self.size[1] * 0.08)
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
    def __init__(self, env, alpha=0.1, gamma=0.95, epsilon=0.15):
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

    def get_max_q_value(self, state):
        """Get the maximum Q-value for a given state"""
        if state in self.q_table:
            return max(self.q_table[state].values())
        return 0.0

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
    def __init__(self, maze, agent, cell_size=25):
        self.maze = maze
        self.agent = agent
        self.cell_size = cell_size
        
        # Track visited cells
        self.visited_cells = set()
        
        # Calculate dimensions
        self.maze_width = maze.size[1] * cell_size
        self.maze_height = maze.size[0] * cell_size
        self.q_panel_width = maze.size[1] * cell_size
        self.total_width = self.maze_width + self.q_panel_width + 40  # 40px padding
        self.total_height = max(self.maze_height, maze.size[0] * cell_size) + 100  # Extra height for text
        
        self.screen = pygame.display.set_mode((self.total_width, self.total_height))
        pygame.display.set_caption("Q-Learning Maze with Q-Value Visualization")
        self.clock = pygame.time.Clock()
        self.path = []
        
        # Initialize font for text rendering
        self.font = pygame.font.Font(None, 16)
        self.small_font = pygame.font.Font(None, 12)
        
        # Colors for different cell types
        self.colors = {
            'empty': (200, 200, 200),    # Gray for empty spaces
            'wall': (0, 0, 0),           # Black for walls
            'hazard': (255, 0, 0),       # Red for hazards
            'goal': (0, 255, 0),         # Green for goal
            'agent': (0, 0, 255),        # Blue for agent
            'path': (100, 100, 255),     # Light blue for path
            'background': (255, 255, 255), # White background
            'text': (0, 0, 0),           # Black text
            'panel_bg': (240, 240, 240)  # Light gray for Q-value panel background
        }

    def get_q_value_color(self, q_value):
        """Convert Q-value to color for visualization"""
        # Normalize Q-value to color range
        if q_value > 0:
            # Positive values: shades of green (brighter = higher value)
            intensity = min(255, int(255 * (q_value / 10.0)))  # Assuming max Q-value around 10
            return (0, intensity, 0)
        elif q_value < 0:
            # Negative values: shades of red (brighter = more negative)
            intensity = min(255, int(255 * (abs(q_value) / 5.0)))  # Assuming min Q-value around -5
            return (intensity, 0, 0)
        else:
            # Zero values: white
            return (255, 255, 255)

    def draw_maze_grid(self):
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

    def draw_q_value_grid(self):
        """Draw the Q-value visualization panel"""
        panel_x_offset = self.maze_width + 20
        
        # Draw panel background
        panel_rect = pygame.Rect(panel_x_offset, 0, self.q_panel_width, self.maze_height)
        pygame.draw.rect(self.screen, self.colors['panel_bg'], panel_rect)
        
        # Find min and max Q-values for better color scaling
        all_q_values = []
        for state in self.agent.q_table:
            all_q_values.extend(self.agent.q_table[state].values())
        
        min_q = min(all_q_values) if all_q_values else 0
        max_q = max(all_q_values) if all_q_values else 0
        
        for x in range(self.maze.size[0]):
            for y in range(self.maze.size[1]):
                rect = pygame.Rect(panel_x_offset + y * self.cell_size, 
                                 x * self.cell_size, 
                                 self.cell_size, self.cell_size)
                
                if self.maze.grid[x, y] == 1:  # Wall
                    color = self.colors['wall']
                    pygame.draw.rect(self.screen, color, rect)
                else:
                    # Get max Q-value for this state
                    max_q_value = self.agent.get_max_q_value((x, y))
                    
                    # Color based on Q-value
                    if max_q != min_q:  # Avoid division by zero
                        normalized_q = (max_q_value - min_q) / (max_q - min_q)
                    else:
                        normalized_q = 0.5
                    
                    if max_q_value > 0:
                        # Positive values: green gradient
                        green_intensity = int(255 * normalized_q)
                        color = (0, green_intensity, 0)
                    elif max_q_value < 0:
                        # Negative values: red gradient
                        red_intensity = int(255 * (1 - normalized_q))
                        color = (red_intensity, 0, 0)
                    else:
                        # Zero values: white
                        color = (255, 255, 255)
                    
                    pygame.draw.rect(self.screen, color, rect)
                    
                    # Draw Q-value text if cell is large enough
                    if self.cell_size >= 20:
                        q_text = f"{max_q_value:.2f}"
                        text_surface = self.small_font.render(q_text, True, (0, 0, 0))
                        text_rect = text_surface.get_rect(center=rect.center)
                        self.screen.blit(text_surface, text_rect)
                
                # Draw grid lines
                pygame.draw.rect(self.screen, (100, 100, 100), rect, 1)

    def draw_path(self):
        """Draw the agent's path"""
        for i, (x, y) in enumerate(self.path[:-1]):  # Don't draw over current position
            rect = pygame.Rect(y * self.cell_size + 5, x * self.cell_size + 5, 
                             self.cell_size - 10, self.cell_size - 10)
            pygame.draw.rect(self.screen, self.colors['path'], rect)

    def draw_agent(self):
        """Draw the agent at current position"""
        x, y = self.maze.state
        center = (y * self.cell_size + self.cell_size // 2, 
                 x * self.cell_size + self.cell_size // 2)
        pygame.draw.circle(self.screen, self.colors['agent'], center, self.cell_size // 3)

    def draw_legend_and_info(self, total_reward, episode_count):
        """Draw legend and information"""
        y_offset = self.maze_height + 10
        
        # Title for maze
        title1 = self.font.render("Maze Environment", True, self.colors['text'])
        self.screen.blit(title1, (10, y_offset))
        
        # Title for Q-values
        title2 = self.font.render("Q-Value Visualization", True, self.colors['text'])
        self.screen.blit(title2, (self.maze_width + 30, y_offset))
        
        # Legend
        legend_y = y_offset + 25
        legend_items = [
            ("Black: Walls", self.colors['wall']),
            ("Red: Hazards (-1.0)", self.colors['hazard']),
            ("Green: Goal (+10.0)", self.colors['goal']),
            ("Blue: Agent", self.colors['agent'])
        ]
        
        for i, (text, color) in enumerate(legend_items):
            x_pos = 10 + (i * 150)
            pygame.draw.rect(self.screen, color, (x_pos, legend_y, 15, 15))
            text_surface = self.small_font.render(text, True, self.colors['text'])
            self.screen.blit(text_surface, (x_pos + 20, legend_y))
        
        # Q-value legend
        q_legend_y = legend_y + 25
        q_legend_text = "Q-Values: Black=Unvisited, White Numbers=Visited (Max Q-value)"
        q_text_surface = self.small_font.render(q_legend_text, True, self.colors['text'])
        self.screen.blit(q_text_surface, (10, q_legend_y))
        
        # Current episode info
        info_y = q_legend_y + 20
        info_text = f"Episode: {episode_count} | Total Reward: {total_reward:.2f} | Steps: {len(self.path)}"
        info_surface = self.small_font.render(info_text, True, self.colors['text'])
        self.screen.blit(info_surface, (10, info_y))

    def run(self):
        running = True
        state = self.maze.reset()
        self.path = [state]
        total_reward = 0
        episode_count = 1

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            action = self.agent.choose_action(state)
            next_state, reward, done = self.maze.step(action)
            total_reward += reward
            
            # Add current state to visited cells
            self.visited_cells.add(state)
            
            # Update Q-values in real-time
            self.agent.update_q_value(state, action, reward, next_state)
            
            if next_state != state:  # Only add to path if agent actually moved
                self.path.append(next_state)

            # Draw everything
            self.screen.fill(self.colors['background'])
            self.draw_maze_grid()
            self.draw_q_value_grid()
            self.draw_path()
            self.draw_agent()
            self.draw_legend_and_info(total_reward, episode_count)
            pygame.display.flip()

            self.clock.tick(10000)  # Moderate speed for observation

            if done:
                print(f"Episode {episode_count} completed! Reward: {total_reward:.2f}, Steps: {len(self.path)}")
                pygame.time.wait(1)  # Wait 1.5 seconds before reset
                state = self.maze.reset()
                self.path = [state]
                total_reward = 0
                episode_count += 1
                
            else:
                state = next_state

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    # Create smaller maze for better Q-value visibility
    maze = Maze(size=(20, 20), start=(0, 0), goal=(19, 19))
    agent = QLearningAgent(maze, alpha=0.1, gamma=0.95, epsilon=0.15)

    
    # Do some initial training
    print("Pre-training agent for 500 episodes...")
    agent.train(episodes=500)
    print("Pre-training completed! Starting visualization...")

    print("Launching Pygame visualization...")
    game = PygameMaze(maze, agent)
    game.run()