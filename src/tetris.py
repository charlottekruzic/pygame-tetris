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

        self.fall_speeds = [1.000, 0.840,0.706,0.593,0.498,0.418,0.351,0.295,0.248,0.208,0.175,0.147,0.123,0.104,0.087,0.073,0.061,0.052,0.043,0.036]
        self.fall_speed = self.fall_speeds[0]
        self.fall_time = 0
        self.move_time = 0

        self.score = 0
        self.level = 0

        self.total_lines_cleared = 0

        self.game_over = False
        self.is_start = False   

    def game_loop(self):
        initial_delay = 0.2
        repeat_delay = 0.05
        left_time = right_time = down_time = 0

        # Ecran de démarrage
        while not self.is_start:  
            self.print_start_screen()
        
        # Boucle principale
        while self.running:
            
            # Ecran de fin de jeu
            if self.game_over:
                self.print_game_over_screen()
                

            dt = self.clock.tick(60) / 1000
            self.fall_time += dt
            
            # Premiere piece
            if self.current_piece is None:
                self.current_piece = piece.Piece(self.grid)
                self.next_piece = piece.Piece(self.grid)
                self.update_shadow_piece()
                
            if self.fall_time > self.fall_speed:
                self.fall_time = 0
                if not self.current_piece.move("down"):
                    self.grid.add_piece(self.current_piece)
                    self.new_piece()
            
            # Gestion des événements
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    self.running = False
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.current_piece.rotate()
                        self.current_piece.fix_position()
                        self.update_shadow_piece()
                    elif event.key == pygame.K_SPACE:
                        pos_init_y = self.current_piece.position[0]
                        while self.current_piece.move("down"):
                            pass
                        blocks_skip = self.current_piece.position[0] - pos_init_y
                        
                        self.grid.add_piece(self.current_piece)
                        self.new_piece()
                        
                        self.score += blocks_skip
                        self.clear_lines()

            # deplacement continu
            keys = pygame.key.get_pressed()
            
            if keys[pygame.K_LEFT]:
                if left_time == 0 or left_time > initial_delay and (left_time - initial_delay) % repeat_delay < dt:
                    self.current_piece.move("left")
                    self.update_shadow_piece()
                left_time += dt
            else:
                left_time = 0

            if keys[pygame.K_RIGHT]:
                if right_time == 0 or right_time > initial_delay and (right_time - initial_delay) % repeat_delay < dt:
                    self.current_piece.move("right")
                    self.update_shadow_piece()
                right_time += dt
            else:
                right_time = 0

            if keys[pygame.K_DOWN]:
                if down_time == 0 or down_time > initial_delay and (down_time - initial_delay) % repeat_delay < dt:
                    if self.current_piece.move("down"):
                        self.score += 1
                    else:
                        self.grid.add_piece(self.current_piece)
                        self.new_piece()
                        nb_lines = self.clear_lines()
                        self.score += nb_lines * 10
                down_time += dt
            else:
                down_time = 0

            # maj ecran        
            self.draw_game()

        pygame.quit()

    def print_game_over_screen(self):
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))                
        font = pygame.font.Font(None, 50)
        text = font.render("Game Over", True, (255, 255, 255))
        self.screen.blit(text, (WINDOW_WIDTH / 2 - text.get_width() / 2, WINDOW_HEIGHT / 2 - text.get_height() / 2))

        font = pygame.font.Font(None, 30)
        text = font.render("Press SPACE to restart", True, (255, 255, 255))
        self.screen.blit(text, (WINDOW_WIDTH / 2 - text.get_width() / 2, WINDOW_HEIGHT / 2 + text.get_height() * 2))

        pygame.display.flip()

        while self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT :
                    self.running = False
                    self.game_over = False
                    break

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                        self.game_over = False
                        break
                    if event.key == pygame.K_SPACE:
                        self.game_over = False
                        self.score = 0
                        self.level = 0
                        self.total_lines_cleared = 0
                        self.grid = grid.Grid(GRID_WIDTH, GRID_HEIGHT)
                        self.current_piece = None
                        self.next_piece = None
                        self.shadow_piece = None
                        self.fall_speed = self.fall_speeds[0]
                        break
                
            if not self.running:
                break


    def print_start_screen(self):
        self.screen.fill((0, 0, 0))
        title_font = pygame.font.Font(None, 80)
        title_text = title_font.render("Tetris", True, (255, 255, 255))
        self.screen.blit(title_text, (WINDOW_WIDTH / 2 - title_text.get_width() / 2, WINDOW_HEIGHT / 8 - title_text.get_height() / 2))

        rules_font = pygame.font.Font(None, 30)
        rules_text = rules_font.render("R : Open Rules", True, (255, 255, 255))
        self.screen.blit(rules_text, (WINDOW_WIDTH - rules_text.get_width() - 10, WINDOW_HEIGHT - rules_text.get_height() - 10))

        start_font = pygame.font.Font(None, 60)
        start_text = start_font.render("Press SPACE to start", True, (255, 255, 255))
        self.screen.blit(start_text, (WINDOW_WIDTH / 2 - start_text.get_width() / 2, WINDOW_HEIGHT / 1.5 + start_text.get_height() ))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.is_start = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    self.is_start = True
                if event.key == pygame.K_SPACE:
                    self.is_start = True
                
                if event.key == pygame.K_r:
                    self.print_rules_screen()

    def print_rules_screen(self):
        self.screen.fill((0, 0, 0))

        title_font = pygame.font.Font(None, 60)
        title_text = title_font.render("Rules", True, (255, 255, 255))
        self.screen.blit(title_text, (WINDOW_WIDTH / 2 - title_text.get_width() / 2, WINDOW_HEIGHT / 8 - title_text.get_height() / 2))

        rules_font = pygame.font.Font(None, 30)
        
        rules = [
            "> : Move left",
            "< : Move right",
            "^ : Rotate",
            "v : Soft drop",
            "Space : Hard drop",
            "Esc : Quit"
        ]

        start_y = WINDOW_HEIGHT / 2 - len(rules) * rules_font.get_height() / 2
        x_position = WINDOW_WIDTH / 2 - 100

        for i, rule in enumerate(rules):
            rules_text = rules_font.render(rule, True, (255, 255, 255))
            y_position = start_y + i * rules_font.get_height() * 1.5
            self.screen.blit(rules_text, (x_position, y_position))


        rules_font = pygame.font.Font(None, 30)
        rules_text = rules_font.render("R : Close Rules", True, (255, 255, 255))
        self.screen.blit(rules_text, (WINDOW_WIDTH - rules_text.get_width() - 10, WINDOW_HEIGHT - rules_text.get_height() - 10))

        pygame.display.flip()

        pause = True
        while pause:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    self.running = False
                    self.is_start = True
                    pause = False
            
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        pause = False
                        break

    def new_piece(self):
        self.current_piece = self.next_piece
        self.is_game_over()
        self.next_piece = piece.Piece(self.grid)
        self.update_shadow_piece()

    def is_game_over(self):
        if not self.current_piece.is_valid_position(self.current_piece.position[0], self.current_piece.position[1]):
            self.game_over = True
    

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

        if self.level <= len(self.fall_speeds):
            self.fall_speed = self.fall_speeds[self.level]

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
        text = font.render(f"Lines break: {self.total_lines_cleared}", True, (255, 255, 255))
        self.screen.blit(text, (up_left_right_part, 90))
