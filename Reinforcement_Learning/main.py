import pygame
import sys

# PyGame initialiseren
pygame.init()

# Venstergrootte
width, height = 600, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Grid World")

# Kleurinstellingen
WHITE = (255, 255, 255)

# Hoofdloop
running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

pygame.quit()
sys.exit()
