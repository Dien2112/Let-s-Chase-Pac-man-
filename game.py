# game.py
import pygame
import threading
import time

from algorithm.dfs import start_dfs_thread
from algorithm.bfs import start_bfs_thread
from algorithm.ucs import start_ucs_thread
from algorithm.astar import start_astar_thread
from utils import find_index, swap

TILE_SIZE = 40
FONT_NAME = "freesansbold.ttf"

with open('map1.txt', 'r') as file:
    game_map = [line.strip().split() for line in file]

ROW_COUNT = len(game_map)
COL_COUNT = len(game_map[0])
SPRITE_MAP = {
    '0': "assets/wall.png",
    '1': "assets/path.png",
    '2': "assets/pacman.png",
    'a': "assets/ghost_red.png",
    'b': "assets/ghost_blue.png",
    'c': "assets/ghost_pink.png",
    'd': "assets/ghost_orange.png"
}

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.original_map = [row[:] for row in game_map]
        self.map = [row[:] for row in game_map]
        self.sprites = {}
        self.player_pos = find_index(self.map, '2')
        self.return_to_menu = False
        self.running = True
        self.lose = False
        self.font = pygame.font.Font(FONT_NAME, 48)
        self.load_sprites()

    def load_sprites(self):
        for key, path in SPRITE_MAP.items():
            image = pygame.image.load(path).convert_alpha()
            self.sprites[key] = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))

    def draw(self):
        for row_idx, row in enumerate(self.map):
            for col_idx, cell in enumerate(row):
                if cell in self.sprites:
                    x = col_idx * TILE_SIZE
                    y = row_idx * TILE_SIZE
                    self.screen.blit(self.sprites[cell], (x, y))

        if self.lose:
            self.display_lose_message()

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and not self.lose:
            move = None
            if event.key == pygame.K_UP:
                move = (-1, 0)
            elif event.key == pygame.K_DOWN:
                move = (1, 0)
            elif event.key == pygame.K_LEFT:
                move = (0, -1)
            elif event.key == pygame.K_RIGHT:
                move = (0, 1)

            if move:
                new_pos = (self.player_pos[0] + move[0], self.player_pos[1] + move[1])
                if self.is_valid_move(new_pos):
                    swap(self.map, self.player_pos, new_pos)
                    self.player_pos = new_pos
                    self.check_collision()

    def is_valid_move(self, pos):
        (r, c) = pos
        return 0 <= r < ROW_COUNT and 0 <= c < COL_COUNT and self.map[r][c] == '1'

    def check_collision(self):
        r, c = self.player_pos
        if self.map[r][c] in ('a', 'b', 'c', 'd'):
            self.lose = True
            self.running = False

    def display_lose_message(self):
        text = self.font.render("YOU LOSE", True, (255, 0, 0))
        rect = text.get_rect(center=(COL_COUNT * TILE_SIZE // 2, ROW_COUNT * TILE_SIZE // 2))
        self.screen.blit(text, rect)

    def reset(self):
        self.map = [row[:] for row in self.original_map]
        self.player_pos = find_index(self.map, '2')
        self.return_to_menu = False
        self.running = True
        self.lose = False
        self.start_threads()

    def cleanup(self):
        self.running = False

    def start_threads(self):
        print("Starting algorithm threads...")
        threading.Thread(target=start_dfs_thread, args=(self.map, self), daemon=True).start()
        threading.Thread(target=start_bfs_thread, args=(self.map, self), daemon=True).start()
        threading.Thread(target=start_ucs_thread, args=(self.map, self), daemon=True).start()
        threading.Thread(target=start_astar_thread, args=(self.map, self), daemon=True).start()
