import pygame
from utils import complex_map_to_map
from draw_complex_map import draw_complex_map, redraw_demo
# Constants
TILE_SIZE = 16
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 620
FONT_NAME = "freesansbold.ttf"

class AlgorithmViewer2:
    def __init__(self, screen, game_map):
        self.screen = screen
        self.sprites = {
            '0': pygame.image.load("assets/wall.png").convert_alpha(),
            '1': pygame.image.load("assets/path.png").convert_alpha(),
            '2': pygame.image.load("assets/pacman.png").convert_alpha(),
            'a': pygame.image.load("assets/ghost_red.png").convert_alpha(),
            'b': pygame.image.load("assets/ghost_blue.png").convert_alpha(),
            'c': pygame.image.load("assets/ghost_pink.png").convert_alpha(),
            'd': pygame.image.load("assets/ghost_orange.png").convert_alpha()
        }
        self.font = pygame.font.Font("assets/fonts/PressStart2P.ttf", 18)
        self.raw_map = game_map # Unpack the tuple to get the actual map
        print("RAW", self.raw_map)
        self.game_map = complex_map_to_map(self.raw_map)
        for i in range(len(self.raw_map)):
            for j in range(len(self.raw_map[i])):
                if self.game_map[i][j] != '0':
                    self.game_map[i][j] = '1'

        self.pacman_pos = (5, 7)
        self.reset()
    
    def reset(self):
        self.screen.fill((0,0,0))
        redraw_demo(self.screen, self.raw_map)
        header_text = self.font.render("Choose Pac-Man Position", True, (255, 255, 255))
        self.screen.blit(header_text, (SCREEN_WIDTH // 2 - header_text.get_width() // 2, 10))
        draw_complex_map(self.screen, self.raw_map)

    def draw(self):
        redraw_demo(self.screen, self.raw_map)
        
        # Draw Pac-Man at the current position
        pac_x = self.pacman_pos[1] * TILE_SIZE
        pac_y = (self.pacman_pos[0]) * TILE_SIZE  # Offset for header
        print(self.raw_map[self.pacman_pos[0]][self.pacman_pos[1]])
        self.screen.blit(pygame.transform.scale(self.sprites['2'], (TILE_SIZE, TILE_SIZE)), (pac_x, pac_y))

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            return "quit", None

        if event.type == pygame.KEYDOWN:
            row, col = self.pacman_pos
            if event.key == pygame.K_UP and row > 0 and self.game_map[row - 1][col] == '1':
                self.pacman_pos = (row - 1, col)
            elif event.key == pygame.K_DOWN and row < len(self.game_map) - 1 and self.game_map[row + 1][col] == '1':
                self.pacman_pos = (row + 1, col)
            elif event.key == pygame.K_LEFT and col > 0 and self.game_map[row][col - 1] == '1':
                self.pacman_pos = (row, col - 1)
            elif event.key == pygame.K_RIGHT and col < len(self.game_map[0]) - 1 and self.game_map[row][col + 1] == '1':
                self.pacman_pos = (row, col + 1)
            elif event.key == pygame.K_RETURN:
                return "choose_pacman_pos", self.pacman_pos
            elif event.key == pygame.K_ESCAPE:
                return "quit", None
            print(event.key)
            print("Come to this")
            self.draw()
        return "continue", None  # <== Make sure this is always the default return

    def get_pacman_position(self):
        
        return self.pacman_pos
  
