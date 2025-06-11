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
            """Generate random walls in the maze"""
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
        """Check if position is within bounds and not a wall"""
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
        else:  # Empty space
            return self.state, -0.01, False 


    
