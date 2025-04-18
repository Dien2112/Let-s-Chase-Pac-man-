import pygame
from algorithm.dfs import dfs
from algorithm.astar import astar
from algorithm.ucs import ucs
from algorithm.bfs import bfs

# Constants
TILE_SIZE = 64

class Entity:
    def __init__(self, position, image_path, algorithm=None, move_delay=15):
        self.position = list(position)  # (row, col)
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
        self.algorithm = algorithm
        self.path = None
        self.move_delay = move_delay
        self.move_counter = 0

    def can_move(self):
        self.move_counter += 1
        return self.move_counter >= self.move_delay

    def update_position(self, new_position):
        self.position = list(new_position)

    def move(self):
        if self.path and hasattr(self.path, 'position'):
            self.update_position(self.path.position)
            self.path = self.path.children[0] if self.path.children else None
            self.move_counter = 0

class Entities:
    SPRITE_MAP = {
        '0': "assets/wall.jpg",
        '1': "assets/path.jpg",
        '2': "assets/pacman.png",
        'a': "assets/ghost_red.png",
        'b': "assets/ghost_blue.png",
        'c': "assets/ghost_pink.png",
        'd': "assets/ghost_orange.png"
    }

    def __init__(self, game_map):
        self.entities = {}
        # Find positions
        pacman_pos = None
        ghost_positions = {'a': None, 'b': None, 'c': None, 'd': None}
        for i, row in enumerate(game_map):
            for j, cell in enumerate(row):
                if cell == '2':
                    pacman_pos = (i, j)
                elif cell in 'abcd':
                    ghost_positions[cell] = (i, j)

        # Initialize entities
        self.entities['pacman'] = Entity(pacman_pos, self.SPRITE_MAP['2'], move_delay=15)  # ~0.5s at 30 FPS
        self.entities['ghost_red'] = Entity(ghost_positions['a'], self.SPRITE_MAP['a'], algorithm='bfs', move_delay=4)  # ~0.13s
        self.entities['ghost_blue'] = Entity(ghost_positions['b'], self.SPRITE_MAP['b'], algorithm='dfs', move_delay=8)  # ~0.27s
        self.entities['ghost_pink'] = Entity(ghost_positions['c'], self.SPRITE_MAP['c'], algorithm='ucs', move_delay=5)  # ~0.17s
        self.entities['ghost_orange'] = Entity(ghost_positions['d'], self.SPRITE_MAP['d'], algorithm='astar', move_delay=6)  # ~0.2s

    def get_image(self, cell):
        if cell in self.SPRITE_MAP:
            image = pygame.image.load(self.SPRITE_MAP[cell])
            return pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))
        return self.entities['pacman'].image  # Fallback

    def update_ghost_path(self, ghost_name, pacman_pos, game_map):
        ghost = self.entities[ghost_name]
        other_ghosts = [tuple(self.entities[g].position) for g in 
                        ['ghost_red', 'ghost_blue', 'ghost_pink', 'ghost_orange'] if g != ghost_name]
        maze = [[1 if cell != '0' else 0 for cell in row] for row in game_map]
        start = tuple(ghost.position)
        goal = tuple(pacman_pos)
        if ghost.algorithm == 'dfs':
            ghost.path = dfs(maze, start, goal, other_ghosts, ghost.path)
        elif ghost.algorithm == 'astar':
            ghost.path = astar(maze, start, goal, other_ghosts)
        elif ghost.algorithm == 'ucs':
            ghost.path = ucs(maze, start, goal, other_ghosts)
        elif ghost.algorithm == 'bfs':
            ghost.path = bfs(maze, start, goal, other_ghosts)