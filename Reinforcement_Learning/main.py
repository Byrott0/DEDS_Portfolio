import pygame
import sys

# Instellingen
CELL_SIZE = 80
GRID_SIZE = 5
WIDTH = HEIGHT = CELL_SIZE * GRID_SIZE

# Kleuren
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)

# Startpositie van de agent
agent_x = 0
agent_y = 0

# PyGame starten
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Grid")
clock = pygame.time.Clock()

# Hoofdloop
running = True
while running:
    screen.fill(WHITE)

    # Grid tekenen
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, GRAY, rect, 1)

    # Agent tekenen
    agent_rect = pygame.Rect(agent_x * CELL_SIZE, agent_y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, BLUE, agent_rect)

    # weergeef de scherminhoud
    pygame.display.flip()

    # Input verwerken van de gebruiker
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False # Stop de loop en de game

            # Beweeg de agent met de pijltjestoetsen, de positie van de agent wordt aangepast
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and agent_y > 0:
                agent_y -= 1
            if event.key == pygame.K_DOWN and agent_y < GRID_SIZE - 1:
                agent_y += 1
            if event.key == pygame.K_LEFT and agent_x > 0:
                agent_x -= 1
            if event.key == pygame.K_RIGHT and agent_x < GRID_SIZE - 1:
                agent_x += 1

    clock.tick(10) # Beperk de framerate tot 10 FPS

pygame.quit()
sys.exit()
