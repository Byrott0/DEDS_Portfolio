import pygame as pg
import numpy as np
import random
import sys

#intialiseer de pg library
pg.init()

#maak de class van de maze door de game
class Maze:
    #de maze class maakt de wereld van de maze en je vult de grid en en positionering in
    def __init__(self, size=(10, 10), start=(0, 0), goal=(9, 9)):
        self.size = size # self is net als this in Java. verwijzing naar de object in de class
        self.start = start
        self.goal = goal
        self.state = start
        self.actions = ['up', 'down', 'left', 'right'] #de bewegingen in de maze

        # initialze de posities in de grid met de cellen
        self.grid = np.zeros(size, dtype=int) # in deze grid worden de cellen opgeslagen
        self.grid[goal] = 3 #goal cell is 3

        self._generate_walls() #generate walls in the maze
        self._generate_hazards() #generate hazards in the maze
        self.grid[start] = 0 # start positie blijft vrij

    def _generate_walls(self):
            """genereer random muren in maze"""
            wall_count = int(self.size[0] * self.size[1] * 0.2)
            positions = [(x, y) for x in range(self.size[0]) for y in range(self.size[1])
                         if (x, y) != self.start and (x, y) != self.goal]
            
            wall_positions = random.sample(positions, min(wall_count, len(positions)))
            for x, y in wall_positions:
                self.grid[x, y] = 1
    def _generate_hazards(self):
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
        """Controleer of de positie binnen de grenzen ligt en geen muur is"""
        return (0 <= x < self.size[0] and 
                0 <= y < self.size[1] and 
                self.grid[x, y] != 1) # geen muur
    
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
        else:  
            return self.state, -0.01, False 
        
import pygame as pg
import numpy as np
import random
import sys

#intialiseer de pg library
pg.init()

#maak de class van de maze door de game
class Maze:
    #de maze class maakt de wereld van de maze en je vult de grid en en positionering in
    def __init__(self, size=(10, 10), start=(0, 0), goal=(9, 9)):
        self.size = size # self is net als this in Java. verwijzing naar de object in de class
        self.start = start
        self.goal = goal
        self.state = start
        self.actions = ['up', 'down', 'left', 'right'] #de bewegingen in de maze

        # initialze de posities in de grid met de cellen
        self.grid = np.zeros(size, dtype=int) # in deze grid worden de cellen opgeslagen
        self.grid[goal] = 3 #goal cell is 3

        self._generate_walls() #generate walls in the maze
        self._generate_hazards() #generate hazards in the maze
        self.grid[start] = 0 # start positie blijft vrij

    def _generate_walls(self):
            """genereer random muren in maze"""
            wall_count = int(self.size[0] * self.size[1] * 0.2)
            positions = [(x, y) for x in range(self.size[0]) for y in range(self.size[1])
                         if (x, y) != self.start and (x, y) != self.goal]
            
            wall_positions = random.sample(positions, min(wall_count, len(positions)))
            for x, y in wall_positions:
                self.grid[x, y] = 1
    def _generate_hazards(self):
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
        """Controleer of de positie binnen de grenzen ligt en geen muur is"""
        return (0 <= x < self.size[0] and 
                0 <= y < self.size[1] and 
                self.grid[x, y] != 1) # geen muur
    
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
        else:  
            return self.state, -0.01, False 
        
class QlearningLogic:
    def __init__(self, env, alpha=0.1, gamma=0.9, epsilon=0.1):
        self.env = env
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.q_table = {}

        for x in range(env.size[0]):
            for y in range(env.size[1]):
                self.q_table[(x, y)] = {action: 0.0 for action in env.actions}
    def choose_action(self, state):
        if random.random() < self.epsilon:
            return random.choice(self.env.actions)  # Explore: choose a random action
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

class MazeGame: 
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
        self.total_width = self.maze_width + self.q_panel_width + 50  # 50px padding
        self.total_height = max(self.maze_height, maze.size[0] * cell_size) + 100  # Extra height for text

        self.screen = pg.display.set_mode((self.total_width, self.total_height))
        pg.display.set_caption("Maze Game Amir")
        self.clock = pg.time.Clock()
        self.path = []
        self.font = pg.font.Font(None, 24)
        self.small_font = pg.font.Font(None, 18)

        # kleuren voor cellen
        self.colors = {
            0: (200, 200, 200),  # White for empty cells
            1: (0, 0, 0),        # Black for walls
            2: (255, 0, 0),      # Red for hazards
            3: (0, 255, 0),       # Green for goal
            4: (0, 0, 255),        # Blue for agent
            5: (100, 100, 255),     # Light blue for path
            6: (255, 255, 255), # White background
            7: (0, 0, 0),           # Black text
            8: (240, 240, 240)  # Light gray for Q-value panel background
        }

    def get_q_value_color(self, q_value):
        """kleur van Q-waarde bepalen"""
        if q_value > 0:
            intensity = min(255, int(255 * (q_value / 10.0)))
            return (0, intensity, 0)
        elif q_value < 0:
            intensity = min(255, int(255 * (-q_value / 5.0)))
            return (intensity, 0, 0)
        else:
            return (128, 128, 128)
        
    def draw_maze(self):
        for x in range(self.maze.size[0]):
            for y in range(self.maze.size[1]):
                rect = pg.Rect(y * self.cell_size, x * self.cell_size, 
                                 self.cell_size, self.cell_size)
                
                #cellen kleuren
                cell_type = self.maze.grid[x, y]
                if cell_type == 1:
                    color = self.colors[1]
                elif cell_type == 2:
                    color = self.colors[2]
                elif cell_type == 3:
                    color = self.colors[3]
                else:
                    color = self.colors[0]
                pg.draw.rect(self.screen, color, rect)
                pg.draw.rect(self.screen, (0, 0, 0), rect, 1)

    def draw_q_value_grid(self):
        panel_x = self.maze.size[1] * self.cell_size + 20


        panel_rect = pg.Rect(panel_x, 0, self.q_panel_width, self.maze_height)
        pg.draw.rect(self.screen, (200, 200, 200), panel_rect)

        all_q_values = []
        for state in self.agent.q_table:
            all_q_values.extend(self.agent.q_table[state].values())

        min_q = min(all_q_values) if all_q_values else 0
        max_q = max(all_q_values) if all_q_values else 0
        
        for x in range(self.maze.size[0]):
            for y in range(self.maze.size[1]):
                rect = pg.Rect(panel_x + y * self.cell_size, 
                                 x * self.cell_size, 
                                 self.cell_size, self.cell_size)
                
                if self.maze.grid[x, y] == 1:  # Wall
                    color = self.colors[1]
                    pg.draw.rect(self.screen, color, rect)
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
                    
                    pg.draw.rect(self.screen, color, rect)
                    
                    # Draw Q-value text if cell is large enough
                    if self.cell_size >= 20:
                        q_text = f"{max_q_value:.2f}"
                        text_surface = self.small_font.render(q_text, True, (0, 0, 0))
                        text_rect = text_surface.get_rect(center=rect.center)
                        self.screen.blit(text_surface, text_rect)
                
                # Draw grid lines
                pg.draw.rect(self.screen, (100, 100, 100), rect, 1)

    def draw_path(self):
        """Draw the agent's path"""
        for i, (x, y) in enumerate(self.path[:-1]):  # Don't draw over current position
            rect = pg.Rect(y * self.cell_size + 5, x * self.cell_size + 5, 
                             self.cell_size - 10, self.cell_size - 10)
            pg.draw.rect(self.screen, self.colors[5], rect)

    def draw_agent(self):
        """Draw the agent at current position"""
        x, y = self.maze.state
        center = (y * self.cell_size + self.cell_size // 2, 
                 x * self.cell_size + self.cell_size // 2)
        pg.draw.circle(self.screen, self.colors[4], center, self.cell_size // 3)

    def draw_legend_and_info(self, total_reward, episode_count):
        """Draw legend and information"""
        y_offset = self.maze_height + 10
        
        # Title for maze
        title1 = self.font.render("Maze Environment", True, self.colors[7])
        self.screen.blit(title1, (10, y_offset))
        
        # Title for Q-values
        title2 = self.font.render("Q-Value Visualization", True, self.colors[7])
        self.screen.blit(title2, (self.maze_width + 30, y_offset))
        
        # Legend
        legend_y = y_offset + 25
        legend_items = [
            ("Black: Walls", self.colors[1]),
            ("Red: Hazards (-1.0)", self.colors[2]),
            ("Green: Goal (+10.0)", self.colors[3]),
            ("Blue: Agent", self.colors[4])
        ]
        
        for i, (text, color) in enumerate(legend_items):
            x_pos = 10 + (i * 150)
            pg.draw.rect(self.screen, color, (x_pos, legend_y, 15, 15))
            text_surface = self.small_font.render(text, True, self.colors[7])
            self.screen.blit(text_surface, (x_pos + 20, legend_y))
        
        # Q-value legend
        q_legend_y = legend_y + 25
        q_legend_text = "Q-Values: Black=Unvisited, White Numbers=Visited (Max Q-value)"
        q_text_surface = self.small_font.render(q_legend_text, True, self.colors[7])
        self.screen.blit(q_text_surface, (10, q_legend_y))
        
        # Current episode info
        info_y = q_legend_y + 20
        info_text = f"Episode: {episode_count} | Total Reward: {total_reward:.2f} | Steps: {len(self.path)}"
        info_surface = self.small_font.render(info_text, True, self.colors[7])
        self.screen.blit(info_surface, (10, info_y))

    def run(self):
        running = True
        state = self.maze.reset()
        self.path = [state]
        total_reward = 0
        episode_count = 1

        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
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
            self.screen.fill(self.colors[(4)])
            self.draw_maze()
            self.draw_q_value_grid()
            self.draw_path()
            self.draw_agent()
            self.draw_legend_and_info(total_reward, episode_count)
            pg.display.flip()

            self.clock.tick(10)  # beheer snelheid van de game

            if done:
                print(f"Episode {episode_count} completed! Reward: {total_reward:.2f}, Steps: {len(self.path)}")
                pg.time.wait(1)  # Wait 1.5 seconds before reset
                state = self.maze.reset()
                self.path = [state]
                total_reward = 0
                episode_count += 1
                
            else:
                state = next_state

        pg.quit()
        sys.exit()

if __name__ == "__main__":
    # Create smaller maze for better Q-value visibility
    maze = Maze(size=(15, 15), start=(0, 0), goal=(14, 14))
    agent = QlearningLogic(maze, alpha=0.1, gamma=0.95, epsilon=0.15)

    
    # Do some initial training
    print("Pre-training agent for 500 episodes...")
    agent.train(episodes=500)
    print("Pre-training completed! Starting visualization...")

    print("Launching Pygame visualization...")
    game = MazeGame(maze, agent)
    game.run()