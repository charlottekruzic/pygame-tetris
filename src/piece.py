import random

shapes = [
    {"shape" : [[0,0,0,0],[1, 1, 1, 1],[0,0,0,0],[0,0,0,0]], "color" : (0, 255, 255)}, # I : cyan
    {"shape" : [[1, 1], [1, 1]], "color" : (255, 255, 0)}, # O : yellow
    {"shape" : [[0,0,0],[1, 1, 1], [0,1,0]], "color" : (255, 0, 255)}, # T : purple
    {"shape" : [[1, 1, 0], [0,1,1],[0,0,0]], "color" : (255, 0,0)},    # Z : red
    {"shape" : [[0, 1,1],[1, 1, 0], [0,0,0]], "color" : (0,255, 0)}, # S : green
    {"shape" : [[1, 0, 0], [1, 1, 1],[0,0,0]], "color" : (0, 0, 255)}, # J : blue
    {"shape" : [[0, 0, 1], [1, 1, 1],[0,0,0]], "color" : (255, 155, 0)} # L : orange
]



class Piece:
    def __init__ (self, grid, shape=None):
        if shape==None:
            new_shape = random.choice(shapes)
            self.shape = new_shape.get("shape")
            self.color = new_shape.get("color")
            self.orientation = random.randint(0, 3)
        else:
            self.shape = shape.get("shape")
            self.color = shape.get("color")
            self.orientation = 0
        
        self.grid = grid
        self.rotate(self.orientation)

        deplacement = 0
        while self.shape and not any(self.shape[deplacement]):
            deplacement+=1

        self.position = [0-deplacement, self.grid.width // 2 - len(self.shape[0]) // 2]

        
        
    def set_position(self, position):
        self.position = position


    def rotate(self, number=1):
        for _ in range(number):
            self.shape = [list(row) for row in zip(*self.shape[::-1])]
        


    def move(self, direction):
        if direction == 'left':
            if self.is_valid_position(self.position[0], self.position[1] - 1):
                self.position[1] -= 1
        elif direction == 'right':
            if self.is_valid_position(self.position[0], self.position[1] + 1):
                self.position[1] += 1
        elif direction == 'down':
            if self.is_valid_position(self.position[0]+1, self.position[1]):
                self.position[0] += 1
                return True
            return False
    
    def fix_position(self):
        if self.position[1] < 0:
            self.position[1] = 0
        elif self.position[1] + len(self.shape[0]) > self.grid.width:
            self.position[1] = self.grid.width - len(self.shape[0])

    def is_valid_position(self, row, col):
        
        for y, r in enumerate(self.shape):
            for x, value in enumerate(r):
                if value:
                     if value:
                        if (row + y >= self.grid.height or col + x < 0 or col + x >= self.grid.width or self.grid.grid[row + y][col + x]):
                            return False
        return True 
    
    def copy(self, color=None):
        if color == None:
            color = self.color
        new_piece = Piece(self.grid, shape={"shape": self.shape, "color": color}) 
        new_piece.position = self.position.copy()
        return new_piece
    

