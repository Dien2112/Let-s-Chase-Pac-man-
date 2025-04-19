# game.py
import pygame
import threading
import time

from algorithm.dfs import start_dfs_thread, start_dfs_thread_loop
from algorithm.bfs import start_bfs_thread, start_bfs_thread_loop
from algorithm.ucs import start_ucs_thread, start_ucs_thread_loop
from algorithm.astar import start_astar_thread, start_astar_thread_loop
from draw_complex_map import draw_complex_map, redraw
from utils import find_index, swap, complex_map_to_map

TILE_SIZE = 16
FONT_NAME = "freesansbold.ttf"


SPRITE_MAP = {
    '0': "assets/wall.png",
    '1': "assets/path.png",
    '2': "assets/pacman.png",
    'a': "assets/ghost_red.png",
    'b': "assets/ghost_blue.png",
    'c': "assets/ghost_pink.png",
    'd': "assets/ghost_orange.png"
}

def main_thread(self):
        while self.running:
            print(self.running)
            start_astar_thread_loop(self.map,self)        
            start_dfs_thread_loop(self.map,self)
            start_bfs_thread_loop(self.map,self)
            start_ucs_thread_loop(self.map, self)
            time.sleep(0.2)
class Game:
    def __init__(self, screen):
        self.screen = screen
        with open('maze2.txt', 'r') as file:
            self.raw_map = [line.strip().split() for line in file if line.strip()]  
        self.map = complex_map_to_map(self.raw_map)
        self.sprites = {}
        self.player_pos = find_index(self.map, '2')
        self.return_to_menu = False
        self.running = True
        self.lose = False
        self.point = 0
        self.font = pygame.font.Font(FONT_NAME, 48)
        self.load_sprites()
        self.ROW_COUNT = len(self.map)
        self.COL_COUNT = len(self.map[0])

    def load_sprites(self):
        for key, path in SPRITE_MAP.items():
            image = pygame.image.load(path).convert_alpha()
            self.sprites[key] = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))
    def is_valid_move(self, pos):
        return pos[0] >= 0 and pos[1] >=0 and pos[0]< self.ROW_COUNT and pos[1]< self.COL_COUNT and self.map[pos[0]][pos[1]] in ['1', '2']

    def draw(self):
        redraw(self.screen, self.raw_map)
        for row_idx, row in enumerate(self.map):
            for col_idx, cell in enumerate(row):
                if (cell >='a' and cell <= 'd') or (cell=='2') :
                    x = col_idx * TILE_SIZE
                    y = row_idx * TILE_SIZE
                    self.screen.blit(self.sprites[cell], (x, y))

        if self.lose:
            self.display_lose_message()

    def handle_event(self, event):
        print(event, event.type)
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
                    if self.raw_map[new_pos[0]][new_pos[1]] in ['+', '.']:
                        self.raw_map[new_pos[0]][new_pos[1]] = '-'
                        self.point += 1000
                        self.update_score_display(self.screen)

                    if self.raw_map[new_pos[0]][new_pos[1]] == 'P':
                        self.raw_map[new_pos[0]][new_pos[1]] = '-'
                        self.point += 5000
                        self.update_score_display(self.screen)
  
                    self.check_collision()
    def update_score_display(self, screen):
        self.font = pygame.font.Font("assets/fonts/PressStart2P.ttf", 18)
        pygame.draw.rect(screen, (0, 0, 0), (550, 0, 180, 50))  # Clear the score area
        text = self.font.render(f"Score: {self.point}", True, (255, 255, 0))
        screen.blit(text, (630, 10))
        pygame.display.update((550, 0, 180, 50))  # Only update that part of screen


    def check_collision(self):
        r, c = self.player_pos
        if self.map[r][c] in ('a', 'b', 'c', 'd'):
            self.lose = True
            self.running = False

    def display_lose_message(self):
        text = self.font.render("YOU LOSE", True, (255, 0, 0))
        rect = text.get_rect(center=(self.COL_COUNT * TILE_SIZE // 2, self.ROW_COUNT * TILE_SIZE // 2))
        self.screen.blit(text, rect)

    def reset(self):
        self.screen.fill((0,0,0))
        self.player_pos = find_index(self.map, '2')
        self.return_to_menu = False
        self.running = True
        self.lose = False
        draw_complex_map(self.screen, self.raw_map)

        self.start_threads()

    def cleanup(self):
        self.running = False


    def start_threads(self):
        threading.Thread(target=start_dfs_thread, args=(self.map, self), daemon=True).start()
        threading.Thread(target=start_bfs_thread, args=(self.map, self), daemon=True).start()
        threading.Thread(target=start_ucs_thread, args=(self.map, self), daemon=True).start()
        threading.Thread(target=start_astar_thread, args=(self.map, self), daemon=True).start()
        #self.game_thread = threading.Thread(target=main_thread, args = (self,) )
        #self.game_thread.start()
