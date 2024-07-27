import pygame

class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[0 for x in range(self.width)] for y in range(self.height)]

    def add_piece(self, piece):
       
        for y, row in enumerate(piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    if 0 <= y + piece.position[0] < self.height and 0 <= x + piece.position[1] < self.width:
                        self.grid[y + piece.position[0]][x + piece.position[1]] = piece.color


