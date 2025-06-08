import pygame
import sys

# ==== CONFIGURATIE ====
CELL_SIZE = 80
GRID_WIDTH = 5  # Of vraag dit aan de gebruiker
GRID_HEIGHT = 5

# Kleuren
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
agent_color = (128, 0, 128)  # Paars voor de agent wanneer die het einde bereikt

# ==== PYGAME INITIALISATIE ====
pygame.init()
WINDOW_WIDTH = CELL_SIZE * GRID_WIDTH
WINDOW_HEIGHT = CELL_SIZE * GRID_HEIGHT
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Grid World RL")
clock = pygame.time.Clock()

# ==== KLASSEN ====
class CellType:
    EMPTY = 0
    OBSTACLE = 1
    GOAL = 2

class Environment:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[CellType.EMPTY for _ in range(width)] for _ in range(height)]
        self.agent_pos = [0, 0]
        self.goal_pos = [width - 1, height - 1]
        self.grid[self.goal_pos[1]][self.goal_pos[0]] = CellType.GOAL
        self.obstacles = [(1, 1), (2, 2), (3, 1)]
        for x, y in self.obstacles:
            self.grid[y][x] = CellType.OBSTACLE

    def reset(self):
        self.agent_pos = [0, 0]
        return self.agent_pos

    def move(self, direction):
        x, y = self.agent_pos
        dx, dy = 0, 0
        if direction == 'up': dy = -1
        elif direction == 'down': dy = 1
        elif direction == 'left': dx = -1
        elif direction == 'right': dx = 1
        nx, ny = x + dx, y + dy
        if 0 <= nx < self.width and 0 <= ny < self.height and self.grid[ny][nx] != CellType.OBSTACLE:
            self.agent_pos = [nx, ny]

    def reached_goal(self):
        return self.agent_pos == self.goal_pos

    def draw(self):
        screen.fill(WHITE)
        for y in range(self.height):
            for x in range(self.width):
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                if self.grid[y][x] == CellType.OBSTACLE:
                    pygame.draw.rect(screen, BLACK, rect)
                elif self.grid[y][x] == CellType.GOAL:
                    pygame.draw.rect(screen, GREEN, rect)
                else:
                    pygame.draw.rect(screen, GRAY, rect, 1)
        # Agent tekenen
        ax, ay = self.agent_pos
        pygame.draw.circle(screen, RED, (ax * CELL_SIZE + CELL_SIZE // 2, ay * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 4)
        pygame.display.flip()

# ==== MAIN LOOP (MANUELE CONTROLE) ====
env = Environment(GRID_WIDTH, GRID_HEIGHT)
running = True
training_mode = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                env.reset()
            if event.key == pygame.K_t:
                training_mode = not training_mode  # Hier komt je eigen Q-learning loop
            if not training_mode:
                if event.key == pygame.K_UP: env.move('up')
                elif event.key == pygame.K_DOWN: env.move('down')
                elif event.key == pygame.K_LEFT: env.move('left')
                elif event.key == pygame.K_RIGHT: env.move('right')

    env.draw()
    clock.tick(10)

pygame.quit()
sys.exit()
