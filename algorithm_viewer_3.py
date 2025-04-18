# algorithm_viewer_3.py
from algorithm.dfs import dfs
from algorithm.bfs import bfs
from algorithm.ucs import ucs
from algorithm.astar import astar
import pygame
import time
# Constants
TILE_SIZE = 40
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 640
FONT_NAME = "freesansbold.ttf"
class AlgorithmViewer3:
    def __init__(self, screen, game_map, position):
        self.screen = screen
        self.game_map = game_map
        self.font = pygame.font.Font(FONT_NAME, 24)
        self.performance = None
        self.pacman_pos = position
        self.ghost_type = 'a'  # Default ghost type
        self.ghost_position = (1,2)  # Starting position of ghost
        for i in range(len(self.game_map)):
            for j in range(len(self.game_map[i])):
                if self.game_map[i][j] != '0':
                    self.game_map[i][j] = '1'
                if i == self.pacman_pos[0] and j == self.pacman_pos[1]:
                    self.game_map[i][j] = '2'
                if i == self.ghost_position[0] and j == self.ghost_position[1]:
                    self.game_map[i][j] = self.ghost_type

        self.sprites = {
            '0': pygame.image.load("assets/wall.png").convert_alpha(),
            '1': pygame.image.load("assets/path.png").convert_alpha(),
            '2': pygame.image.load("assets/pacman.png").convert_alpha(),
            'a': pygame.image.load("assets/ghost_red.png").convert_alpha(),
            'b': pygame.image.load("assets/ghost_blue.png").convert_alpha(),
            'c': pygame.image.load("assets/ghost_pink.png").convert_alpha(),
            'd': pygame.image.load("assets/ghost_orange.png").convert_alpha()
        }
    def draw(self):
        self.screen.fill((0, 0, 0))

        # Drawing the game map and ghost
        header_text = self.font.render("Choose Ghost", True, (255, 255, 255))
        self.screen.blit(header_text, (SCREEN_WIDTH // 2 - header_text.get_width() // 2, 10))

        for row_idx, row in enumerate(self.game_map):
            for col_idx, cell in enumerate(row):
                x = col_idx * TILE_SIZE
                y = (row_idx + 1) * TILE_SIZE  # Offset by one row for header space
                if cell in self.sprites:
                    self.screen.blit(pygame.transform.scale(self.sprites[cell], (TILE_SIZE, TILE_SIZE)), (x, y))

        # Draw the ghost's path
        if hasattr(self, 'ghost_path'):
            for step in self.ghost_path[1:-1]:
                x = step[1] * TILE_SIZE
                y = (step[0] + 1) * TILE_SIZE
                green_tile = pygame.Surface((TILE_SIZE, TILE_SIZE))
                green_tile.fill((0, 255, 0))  # RGB for green
                self.screen.blit(green_tile, (x, y))
        
        # Display stats
        self.draw_stats()
    
    

    def draw_stats(self):
        if self.performance:
            print(self.performance.as_dict())
            stats = self.performance.as_dict()
            x = SCREEN_WIDTH - 300
            y = 20
            for key, value in stats.items():
                line = self.font.render(f"{key}: {value}", True, (255, 255, 255))
                self.screen.blit(line, (x, y))
                y += 40

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                # Start DFS algorithm
                path, record = dfs(self.ghost_position, self.pacman_pos, self.game_map)
                self.ghost_path = path
                self.performance = record
                self.ghost_type = 'a'  # Set ghost type to 'a' for DFS
            elif event.key == pygame.K_2:
                # Start BFS algorithm
                path, record = bfs(self.ghost_position, self.pacman_pos, self.game_map)
                self.ghost_path = path
                self.performance = record
                self.ghost_type = 'b'
            elif event.key == pygame.K_3:
                # Start UCS algorithm
                path, record = ucs(self.ghost_position, self.pacman_pos, self.game_map)
                self.ghost_path = path
                self.performance = record
                self.ghost_type = 'c'
            elif event.key == pygame.K_4:
                # Start A* algorithm
                path, record = astar(self.ghost_position, self.pacman_pos, self.game_map)
                self.ghost_path = path
                self.performance = record
                self.ghost_type = 'd'
            self.draw()
