import pygame
import src.grid as grid
import src.piece as piece

WINDOW_HEIGHT = 600
WINDOW_WIDTH = 800

GRID_HEIGHT = 20
GRID_WIDTH = 10

PIECE_SIZE = 30


class Tetris :

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Tetris")
        self.clock = pygame.time.Clock()
        self.running = True

        self.grid = grid.Grid(GRID_WIDTH, GRID_HEIGHT)

        # Variables pour centrer la grille
        self.grid_x = GRID_WIDTH * PIECE_SIZE
        self.offset_x = WINDOW_WIDTH/2 - self.grid_x / 2

        self.current_piece = None
        self.next_piece = None

        self.shadow_piece = None

        self.fall_speed = 0.5
        self.fall_time = 0

        self.score = 0
        self.level = 0

        self.total_lines_cleared = 0


    def game_loop(self):
       
        while self.running:
            dt = self.clock.tick(60) / 1000
            self.fall_time += dt
            
            if self.current_piece == None:
                self.current_piece = piece.Piece(self.grid)
                self.next_piece = piece.Piece(self.grid)
                self.update_shadow_piece()
                #self.grid.add_piece(self.current_piece)

            if self.fall_time > self.fall_speed:
                self.fall_time = 0
                if not self.current_piece.move("down"):
                    self.grid.add_piece(self.current_piece)
                    self.current_piece = self.next_piece
                    self.next_piece = piece.Piece(self.grid)
                    self.update_shadow_piece()


            
            
            # Gestion evenements
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    self.running = False
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.current_piece.rotate()
                    if event.key == pygame.K_RIGHT:
                        self.current_piece.move("right")
                    if event.key == pygame.K_LEFT:
                        self.current_piece.move("left")
                    if event.key == pygame.K_DOWN:
                        if not self.current_piece.move("down"):
                            self.grid.add_piece(self.current_piece)
                            self.current_piece = self.next_piece
                            self.next_piece = piece.Piece(self.grid)
                        else:
                            self.score += 1
                            nb_lines = self.clear_lines()
                            self.score += nb_lines * 10


                    if event.key == pygame.K_SPACE:
                        pos_init_y = self.current_piece.position[0]
                        while self.current_piece.move("down"):
                            pass

                        block_skip = self.current_piece.position[0] - pos_init_y
                        
                        self.grid.add_piece(self.current_piece)
                        self.current_piece = self.next_piece
                        self.next_piece = piece.Piece(self.grid)

                        

                        self.score += block_skip
                        self.clear_lines()
                        

                    self.update_shadow_piece()


            # maj ecran         
            self.draw_game()


        pygame.quit()

    def clear_lines(self):
        lines_cleared = self.grid.clear_lines()
        self.total_lines_cleared += lines_cleared
        self.update_score(lines_cleared)
        self.update_level()

        return lines_cleared
    

    def update_score(self, lines_cleared):
        factor = self.level + 1
        if lines_cleared == 1:
            self.score += 40 * factor
        elif lines_cleared == 2:
            self.score += 100 * factor
        elif lines_cleared == 3:
            self.score += 300 * factor
        elif lines_cleared == 4:
            self.score += 1200 * factor

    def update_level(self):
        self.level = self.total_lines_cleared // 10

    def update_shadow_piece(self):
        self.shadow_piece = self.current_piece.copy((100, 100, 100))

        while self.shadow_piece.move("down"):
            pass

    def draw_game(self):
        self.screen.fill((0, 0, 0))
        self.draw_grid()
        self.draw_shadow_piece(self.shadow_piece)
        self.draw_piece(self.current_piece) 
        self.draw_next_piece(self.next_piece)

        self.draw_score()

        pygame.display.flip()

    def draw_grid(self):
        for y, row in enumerate(self.grid.grid):
            for x, cell in enumerate(row):
                rect_x = self.offset_x + x * PIECE_SIZE
                rect_y =  y * PIECE_SIZE
                if cell:
                    pygame.draw.rect(self.screen, cell, (rect_x, rect_y, PIECE_SIZE, PIECE_SIZE))
                pygame.draw.rect(self.screen, (255, 255, 255), (rect_x, rect_y, PIECE_SIZE, PIECE_SIZE), 1)

    def draw_piece(self, piece):
        if piece != None:
            for y, row in enumerate(piece.shape):
                for x, cell in enumerate(row):
                    rect_x = self.offset_x + (x + piece.position[1]) * PIECE_SIZE
                    rect_y = (y + piece.position[0]) * PIECE_SIZE
                    if cell:
                        pygame.draw.rect(self.screen, piece.color, (rect_x, rect_y, PIECE_SIZE, PIECE_SIZE))
                        pygame.draw.rect(self.screen, (255, 255, 255), (rect_x, rect_y, PIECE_SIZE, PIECE_SIZE), 1)

    def draw_shadow_piece(self, piece):
        if piece != None:
            for y, row in enumerate(piece.shape):
                for x, cell in enumerate(row):
                    rect_x = self.offset_x + (x + piece.position[1]) * PIECE_SIZE
                    rect_y = (y + piece.position[0]) * PIECE_SIZE
                    if cell:
                        pygame.draw.rect(self.screen, piece.color, (rect_x, rect_y, PIECE_SIZE, PIECE_SIZE))
                        pygame.draw.rect(self.screen, (255, 255, 255), (rect_x, rect_y, PIECE_SIZE, PIECE_SIZE), 1)

    def draw_next_piece(self, piece):
        up_left_right_part = [0, (WINDOW_WIDTH / 2 / PIECE_SIZE  + GRID_WIDTH /2)]

        position = [4, (WINDOW_WIDTH / 2 / PIECE_SIZE  + GRID_WIDTH /2) + 1]
        
        for y, row in enumerate(piece.shape):
            for x, cell in enumerate(row):
                rect_x = (x + position[1]) * PIECE_SIZE
                rect_y = (y + position[0]) * PIECE_SIZE
                if cell:
                    pygame.draw.rect(self.screen, piece.color, (rect_x, rect_y, PIECE_SIZE, PIECE_SIZE))
                    pygame.draw.rect(self.screen, (255, 255, 255), (rect_x, rect_y, PIECE_SIZE, PIECE_SIZE), 1)

    def draw_score(self):
        up_left_right_part = (WINDOW_WIDTH / 2 / PIECE_SIZE  + GRID_WIDTH /2) * PIECE_SIZE + PIECE_SIZE
        font = pygame.font.Font(None, 30)
        text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(text, (up_left_right_part, 10))
        text = font.render(f"Level: {self.level}", True, (255, 255, 255))
        self.screen.blit(text, (up_left_right_part, 50))
