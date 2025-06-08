import pygame
import sys

# ==== CONFIGURATIE ====
CELL_SIZE = 80
GRID_WIDTH = 5
GRID_HEIGHT = 5

# Kleuren
WHITE = (255, 255, 255)
GRAY = (220, 220, 220)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Cell types
EMPTY = 0
WALL = 1
HAZARD = 2
GOAL = 3  

# ==== PYGAME INITIALISATIE ====
pygame.init()
screen = pygame.display.set_mode((GRID_WIDTH * CELL_SIZE, GRID_HEIGHT * CELL_SIZE))
pygame.display.set_caption("Grid World RL")
clock = pygame.time.Clock()

class Environment:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = []
        self.agent_pos = [0, 0]
        self.initialize_grid()

    def initialize_grid(self):
        self.grid = [[EMPTY for _ in range(self.width)] for _ in range(self.height)]
        self.grid[4][4] = GOAL
        self.grid[1][1] = WALL
        self.grid[2][2] = WALL
        self.grid[3][3] = HAZARD
        self.agent_pos = [0, 0]

    def reset(self):
        self.agent_pos = [0, 0]
        return self.agent_pos

    def is_valid_move(self, pos):
        x, y = pos
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x] != WALL
        return False

    def move_agent(self, direction):
        x, y = self.agent_pos
        if direction == 'up': new_pos = [x, y - 1]
        elif direction == 'down': new_pos = [x, y + 1]
        elif direction == 'left': new_pos = [x - 1, y]
        elif direction == 'right': new_pos = [x + 1, y]
        else: new_pos = [x, y]

        if self.is_valid_move(new_pos):
            self.agent_pos = new_pos

    def calculate_reward(self, pos):
        x, y = pos
        if self.grid[y][x] == GOAL:
            return 10
        elif self.grid[y][x] == HAZARD:
            return -10
        else:
            return -1

    def render(self):
        screen.fill(WHITE)
        for y in range(self.height):
            for x in range(self.width):
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                if self.grid[y][x] == WALL:
                    pygame.draw.rect(screen, BLACK, rect)
                elif self.grid[y][x] == HAZARD:
                    pygame.draw.rect(screen, BLUE, rect)
                elif self.grid[y][x] == GOAL:
                    pygame.draw.rect(screen, GREEN, rect)
                else:
                    pygame.draw.rect(screen, GRAY, rect, 1)
        ax, ay = self.agent_pos
        pygame.draw.circle(screen, RED, (ax * CELL_SIZE + CELL_SIZE // 2, ay * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 4)
        pygame.display.flip()

# ========== MAIN LOOP ==========
env = Environment(GRID_WIDTH, GRID_HEIGHT)
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                env.reset()
            elif event.key == pygame.K_UP:
                env.move_agent('up')
            elif event.key == pygame.K_DOWN:
                env.move_agent('down')
            elif event.key == pygame.K_LEFT:
                env.move_agent('left')
            elif event.key == pygame.K_RIGHT:
                env.move_agent('right')

    env.render()
    clock.tick(10)

pygame.quit()
sys.exit()