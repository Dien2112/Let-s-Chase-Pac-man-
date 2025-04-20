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

def draw_thread(self):
        while self.running:
            print("drawing!")
            self.draw()
            print("Drawed")
            time.sleep(0.2)
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
        self.current_map = 1
        with open(f'mazes/maze{self.current_map}.txt', 'r') as file:
            self.raw_map = [line.strip().split() for line in file if line.strip()]  
        self.map = complex_map_to_map(self.raw_map)
        self.count = sum(row.count(c) for row in self.raw_map for c in ['+', '.',  'P', 'p'])

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
        self.is_pause = False

    def load_sprites(self):
        for key, path in SPRITE_MAP.items():
            image = pygame.image.load(path).convert_alpha()
            self.sprites[key] = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))
    def is_valid_move(self, pos):
        return pos[0] >= 0 and pos[1] >=0 and pos[0]< self.ROW_COUNT and pos[1]< self.COL_COUNT and self.map[pos[0]][pos[1]] in ['1', '2']

    def draw(self):
        if self.is_pause or not self.running:
            return
        redraw(self.screen, self.raw_map)
        for row_idx, row in enumerate(self.map):
            for col_idx, cell in enumerate(row):
                if (cell >='a' and cell <= 'd') or (cell=='2') :
                    x = col_idx * TILE_SIZE
                    y = row_idx * TILE_SIZE
                    self.screen.blit(self.sprites[cell], (x, y))
        
        if self.lose:
            text = self.font.render("YOU LOSE", True, (255, 0, 0))
            rect = text.get_rect(center=(self.COL_COUNT * TILE_SIZE // 2, self.ROW_COUNT * TILE_SIZE // 2))
            self.screen.blit(text, rect)
        
    def handle_press(self):
        if self.is_pause:
            return
        keys = pygame.key.get_pressed()
        move = None

        if keys[pygame.K_UP]:
            move = (-1, 0)
        elif keys[pygame.K_DOWN]:
            move = (1, 0)
        elif keys[pygame.K_LEFT]:
            move = (0, -1)
        elif keys[pygame.K_RIGHT]:
            move = (0, 1)
        print(move)
        if move:
            self.moving(move)
            
    def handle_event(self, event):
        print(event, event.type)
        if (event.type == pygame.KEYDOWN):
            if  event.key == pygame.K_ESCAPE:
                if self.is_pause == False:
                    self.running = False
                    self.is_pause = True
                    self.draw_pause_screen()
                else:
                    return "menu"
                    
            elif self.is_pause and event.key == pygame.K_RETURN:
                self.running = True
                self.is_pause = False
                self.reset()

    def draw_pause_screen(self):
        overlay = pygame.Surface((1000,640))
        overlay.set_alpha(180)  # semi-transparent overlay
        overlay.fill((0, 0, 0))  # black background

        font = pygame.font.SysFont("Consolas", 32)
        text1 = font.render("Paused", True, (255, 255, 255))
        text2 = font.render("Press Enter to continue", True, (200, 200, 200))
        text3 = font.render("Press Esc to return to menu", True, (200, 200, 200))

        # Draw a solid rectangle behind the text (not transparent)
        box_width = 600
        box_height = 200
        box_x = 1000 // 2 - box_width // 2
        box_y = 180
        pygame.draw.rect(overlay, (30, 30, 30), (box_x, box_y, box_width, box_height), border_radius=12)

        # Blit overlay first
        self.screen.blit(overlay, (0, 0))

        # Then draw text on top of the solid box
        self.screen.blit(text1, (1000 // 2 - text1.get_width() // 2, 200))
        self.screen.blit(text2, (1000 // 2 - text2.get_width() // 2, 260))
        self.screen.blit(text3, (1000 // 2 - text3.get_width() // 2, 310))

   
    def moving(self, move):
        new_pos = (self.player_pos[0] + move[0], self.player_pos[1] + move[1])
        if self.is_valid_move(new_pos):
            swap(self.map, self.player_pos, new_pos)
            self.player_pos = new_pos
            cell = self.raw_map[new_pos[0]][new_pos[1]]

            if cell in ['+', '.']:
                self.raw_map[new_pos[0]][new_pos[1]] = '-'
                self.point += 1000
                self.count -= 1

            if cell in ['P', 'p']:
                self.raw_map[new_pos[0]][new_pos[1]] = '-'
                self.point += 5000
                self.count -= 1

            self.update_score_display(self.screen)
            self.check_collision()

            # Check for win condition
            if self.count == 0:
                self.handle_win()

    def update_score_display(self, screen):
        pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(630, 10, 300, 200))

        self.font = pygame.font.Font("assets/fonts/PressStart2P.ttf", 18)
        pygame.draw.rect(screen, (0, 0, 0), (200, 0, 180, 50))  # Clear the score area
        text = self.font.render(f"Score: {self.point}", True, (255, 255, 0))
        screen.blit(text, (630, 10))
        pygame.display.update((200, 0, 180, 50))  # Only update that part of screen


    def check_collision(self):
        r, c = self.player_pos
        if self.map[r][c] in ('a', 'b', 'c', 'd'):
            self.display_lose_message()
            

    def display_lose_message(self):
        self.lose = True
        self.running = False
        text = self.font.render("YOU LOSE", True, (255, 0, 0))
        rect = text.get_rect(center=(self.COL_COUNT * TILE_SIZE // 2, self.ROW_COUNT * TILE_SIZE // 2))
        self.screen.blit(text, rect)
        waiting = True

        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    print("YES")
                    self.reinit()
                    self.reset()
                    waiting = False
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            pygame.display.flip()

    def reinit(self):
        with open(f'mazes/maze{self.current_map}.txt', 'r') as file:
            self.raw_map = [line.strip().split() for line in file if line.strip()]  
        self.count = sum(row.count(c) for row in self.raw_map for c in ['+', '-', 'P', 'p'])

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
        self.is_pause = False
    def reset(self):
        self.screen.fill((0,0,0))
        self.player_pos = find_index(self.map, '2')
        self.return_to_menu = False
        self.running = True
        self.lose = False
        draw_complex_map(self.screen, self.raw_map)
        self.font = pygame.font.SysFont('Consolas', 16)
        header_text = self.font.render("Pacman move: ↑←↓→, Pause: ESC, Exit: ESC", True, (255, 255, 255))
        self.screen.blit(header_text, (640, 640 - 20))
        self.update_score_display(self.screen)
        self.start_threads()

    def cleanup(self):
        self.running = False
    
    def handle_win(self):
        self.running = False
        font = pygame.font.SysFont("Consolas", 48)
        win_text = font.render("You Win! Press any key to continue...", True, (255, 255, 0))
        
        overlay = pygame.Surface(self.screen.get_size())
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        self.screen.blit(win_text, (self.screen.get_width() // 2 - win_text.get_width() // 2, self.screen.get_height() // 2))
        pygame.display.flip()
        self.current_map = (self.current_map) %4 + 1
    
        # Wait for any key
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    waiting = False
                    self.reinit()
                    self.reset()
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    exit()


    

    def start_threads(self):
        threading.Thread(target=start_dfs_thread, args=(self.map, self,), daemon=True).start()
        threading.Thread(target=start_bfs_thread, args=(self.map, self,), daemon=True).start()
        threading.Thread(target=start_ucs_thread, args=(self.map, self,), daemon=True).start()
        threading.Thread(target=start_astar_thread, args=(self.map, self,), daemon=True).start()
        #threading.Thread(target=draw_thread, args=(self,),).start()
        #self.game_thread = threading.Thread(target=main_thread, args = (self,) )
        #self.game_thread.start()
