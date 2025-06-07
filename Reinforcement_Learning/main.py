import pygame
import sys

# Instellingen
CELL_SIZE = 80
GRID_SIZE = 5
WIDTH = HEIGHT = CELL_SIZE * GRID_SIZE

# Kleuren
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)


RED = (255, 0, 0)

agent_color = (0, 0, 255)  # Blauwe agent

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
    pygame.draw.rect(screen, agent_color, agent_rect)

    # weergeef de scherminhoud
    pygame.display.flip()

    # Input verwerken van de gebruiker
for event in pygame.event.get():
    if event.type == pygame.QUIT:
        running = False  # Stop de loop en de game

    elif event.type == pygame.KEYDOWN:  # Let op: deze moet op hetzelfde niveau staan als QUIT
        if event.key == pygame.K_UP and agent_y > 0:
            agent_y -= 1
        if event.key == pygame.K_DOWN and agent_y < GRID_SIZE - 1:
            agent_y += 1
        if event.key == pygame.K_LEFT and agent_x > 0:
            agent_x -= 1
        if event.key == pygame.K_RIGHT and agent_x < GRID_SIZE - 1:
            agent_x += 1
        if event.key == pygame.K_RETURN:
            if agent_color == (0, 0, 255):
                agent_color = (255, 0, 0)  # Verander naar rood
            else:
                agent_color = (0, 0, 255)  # Verander terug naar blauw



    clock.tick(10) # Beperk de framerate tot 10 FPS

pygame.quit()
sys.exit()
