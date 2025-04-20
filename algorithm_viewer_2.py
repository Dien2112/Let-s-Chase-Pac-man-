import pygame
from utils import complex_map_to_map
from draw_complex_map import draw_complex_map, redraw_demo
from algorithm.dfs import dfs
from algorithm.bfs import bfs
from algorithm.ucs import ucs
from algorithm.astar import astar

# Constants
TILE_SIZE = 16
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 640
FONT_NAME = "freesansbold.ttf"

class AlgorithmViewer2:
    def __init__(self, screen, game_map):
        self.screen = screen
        self.performance = None
        self.type = "DFS Search"
        self.sprites = {
            '0': pygame.image.load("assets/wall.png").convert_alpha(),
            '1': pygame.image.load("assets/path.png").convert_alpha(),
            '2': pygame.image.load("assets/pacman.png").convert_alpha(),
            'a': pygame.image.load("assets/ghost_red.png").convert_alpha(),
            'b': pygame.image.load("assets/ghost_blue.png").convert_alpha(),
            'c': pygame.image.load("assets/ghost_pink.png").convert_alpha(),
            'd': pygame.image.load("assets/ghost_orange.png").convert_alpha()
        }
        self.font = pygame.font.Font("assets/fonts/PressStart2P.ttf", 20)
        self.raw_map = game_map # Unpack the tuple to get the actual map
        self.game_map = complex_map_to_map(self.raw_map)
        for i in range(len(self.raw_map)):
            for j in range(len(self.raw_map[i])):
                if self.game_map[i][j] != '0':
                    self.game_map[i][j] = '1'

        self.pacman_pos = (5, 7)
        self.ghost_type = 'a'  # Default ghost type
        self.ghost_pos = (4,7)  # Starting position of ghost
        self.reset()
    
    def reset(self):
        self.screen.fill((0,0,0))
        redraw_demo(self.screen, self.raw_map)
        header_text = self.font.render("ALGORITHM SHOW", True, (255, 255, 255))
        self.screen.blit(header_text, (SCREEN_WIDTH // 4 - header_text.get_width() // 2, 10))
        
        self.font = pygame.font.SysFont('Consolas', 16)
        header_text = self.font.render("Pacman move: WASD, Ghost move: ↑←↓→, Ghost change: 1234", True, (255, 255, 255))
        self.screen.blit(header_text, (500, SCREEN_HEIGHT - 20))
        draw_complex_map(self.screen, self.raw_map)

    def draw(self):
        redraw_demo(self.screen, self.raw_map)
        # Draw Pac-Man at the current position
        pac_x = self.pacman_pos[1] * TILE_SIZE
        pac_y = (self.pacman_pos[0]) * TILE_SIZE  # Offset for header
        self.screen.blit(pygame.transform.scale(self.sprites['2'], (TILE_SIZE, TILE_SIZE)), (pac_x, pac_y))
        ghost_x = self.ghost_pos[1] * TILE_SIZE
        ghost_y = (self.ghost_pos[0]) * TILE_SIZE  # Offset for header
        self.screen.blit(pygame.transform.scale(self.sprites[self.ghost_type], (TILE_SIZE, TILE_SIZE)), (ghost_x, ghost_y))

        if hasattr(self, 'ghost_path'):
            for i in range(len(self.ghost_path) - 1):
                start = self.ghost_path[i]
                end = self.ghost_path[i + 1]
        
                start_pos = (start[1] * TILE_SIZE + TILE_SIZE // 2, start[0] * TILE_SIZE + TILE_SIZE // 2)
                end_pos = (end[1] * TILE_SIZE + TILE_SIZE // 2, end[0] * TILE_SIZE + TILE_SIZE // 2)
        
                pygame.draw.line(self.screen, (0, 255, 0), start_pos, end_pos, 3)  # last param is thickness


        self.draw_stats()

    def draw_stats(self):
        pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(700, 20, 300, 300))

        if self.performance:
            print(self.performance.as_dict())
            stats = self.performance.as_dict()
            x = 700
            y = 100
            line = self.font.render(f"{self.type}", True, (255, 255, 255))
            self.screen.blit(line, (x, 60))
            
            for key, value in stats.items():
                line = self.font.render(f"{key}: {value}", True, (255, 255, 255))
                self.screen.blit(line, (x, y))
                y += 40

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            type = None
            if event.key == pygame.K_1:
                # Start DFS algorithm
                path, record = dfs(self.ghost_pos, self.pacman_pos, self.game_map)
                self.ghost_type = 'a' 
                self.type = 'DFS Search'
                self.ghost_path = path
                self.performance = record
            elif event.key == pygame.K_2:
                # Start BFS algorithm
                path, record = bfs(self.ghost_pos, self.pacman_pos, self.game_map)
                self.ghost_type = 'b'
                self.type = 'BFS Search'
                self.ghost_path = path
                self.performance = record
            elif event.key == pygame.K_3:
                # Start UCS algorithm
                path, record = ucs(self.ghost_pos, self.pacman_pos, self.game_map)
                self.ghost_type = 'c'
                self.type = 'UCS Search'
                self.ghost_path = path
                self.performance = record
            elif event.key == pygame.K_4:
                # Start A* algorithm
                path, record = astar(self.ghost_pos, self.pacman_pos, self.game_map)
                self.ghost_type = 'd'
                self.type = 'A* Search'
                self.ghost_path = path
                self.performance = record
            move = True
            if event.key == pygame.K_UP and self.ghost_pos[0] > 0 and self.game_map[self.ghost_pos[0] - 1][self.ghost_pos[1]] == '1':
                self.ghost_pos = (self.ghost_pos[0] - 1, self.ghost_pos[1])
            elif event.key == pygame.K_DOWN and self.ghost_pos[0] < len(self.game_map) - 1 and self.game_map[self.ghost_pos[0] + 1][self.ghost_pos[1]] == '1':
                self.ghost_pos = (self.ghost_pos[0] + 1, self.ghost_pos[1])
            elif event.key == pygame.K_LEFT and self.ghost_pos[1] > 0 and self.game_map[self.ghost_pos[0]][self.ghost_pos[1] - 1] == '1':
                self.ghost_pos = (self.ghost_pos[0], self.ghost_pos[1] - 1)
            elif event.key == pygame.K_RIGHT and self.ghost_pos[1] < len(self.game_map[0]) - 1 and self.game_map[self.ghost_pos[0]][self.ghost_pos[1] + 1] == '1':
                self.ghost_pos = (self.ghost_pos[0], self.ghost_pos[1] + 1)
            elif event.key == pygame.K_w and self.pacman_pos[0] > 0 and self.game_map[self.pacman_pos[0] - 1][self.pacman_pos[1]] == '1':
                self.pacman_pos = (self.pacman_pos[0] - 1, self.pacman_pos[1])
            elif event.key == pygame.K_s and self.pacman_pos[0] < len(self.game_map) - 1 and self.game_map[self.pacman_pos[0] + 1][self.pacman_pos[1]] == '1':
                self.pacman_pos = (self.pacman_pos[0] + 1, self.pacman_pos[1])
            elif event.key == pygame.K_a and self.pacman_pos[1] > 0 and self.game_map[self.pacman_pos[0]][self.pacman_pos[1] - 1] == '1':
                self.pacman_pos = (self.pacman_pos[0], self.pacman_pos[1] - 1)
            elif event.key == pygame.K_d and self.pacman_pos[1] < len(self.game_map[0]) - 1 and self.game_map[self.pacman_pos[0]][self.pacman_pos[1] + 1] == '1':
                self.pacman_pos = (self.pacman_pos[0], self.pacman_pos[1] + 1)
            else:
                move = False
            if move:
                if self.ghost_type == 'a':
                    path, record = dfs(self.ghost_pos, self.pacman_pos, self.game_map)
                elif self.ghost_type == 'b':
                    path, record = bfs(self.ghost_pos, self.pacman_pos, self.game_map)
                elif self.ghost_type == 'c':
                    path, record = ucs(self.ghost_pos, self.pacman_pos, self.game_map)
                elif self.ghost_type == 'd':
                    path, record = astar(self.ghost_pos, self.pacman_pos, self.game_map)
                self.ghost_path = path
                self.performance = record
            



            self.draw()
    def get_pacman_position(self):
        
        return self.pacman_pos
  
