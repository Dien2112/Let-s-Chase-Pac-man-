import pygame
from utils import complex_map_to_map
from draw_complex_map import draw_complex_map, redraw
# Constants
TILE_SIZE = 40
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 640
FONT_NAME = "freesansbold.ttf"

class AlgorithmViewer:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(FONT_NAME, 24)
        self.raw_map = None
        self.map = None
        # Load map files
        self.maps = [f"mazes/maze{i}.txt" for i in range(1, 5)]  
        self.selected_map_idx = 0
        self.game_map = self.load_map(self.maps[self.selected_map_idx])
        
        # Load sprites
        self.load_sprites()

    def load_map(self, map_file):
        with open(map_file, 'r') as file:
            self.raw_map = [line.strip().split() for line in file]
        self.draw()
        self.map = complex_map_to_map(self.raw_map)
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                if self.map[i][j] != '0':
                    self.map[i][j] = '1'


    def load_sprites(self):
        """Loads all the sprite images for the map entities."""
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
        """Draws the map and header to the screen."""
        # Draw header
        header_text = self.font.render("Choose the map", True, (255, 255, 255))
        self.screen.blit(header_text, (SCREEN_WIDTH // 2 - header_text.get_width() // 2, 10))

        draw_complex_map(self.screen, self.raw_map)
        
        self.font = pygame.font.SysFont('Consolas', 16)
        header_text = self.font.render("Change map: ←→, Choose map: ENTER, Exit: ESC", True, (255, 255, 255))
        self.screen.blit(header_text, (600, SCREEN_HEIGHT - 20))

    def handle_event(self, event):
        """Handles key events."""
        if event.type == pygame.QUIT:
            return "quit", None

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "menu", None
            elif event.key == pygame.K_RIGHT:
                # Switch to the next map
                self.selected_map_idx = (self.selected_map_idx + 1) % len(self.maps)
                print(self.selected_map_idx, len(self.maps))
                self.load_map(self.maps[self.selected_map_idx])
            elif event.key == pygame.K_LEFT:
                # Switch to the previous map
                self.selected_map_idx = (self.selected_map_idx - 1) % len(self.maps)
                self.load_map(self.maps[self.selected_map_idx])
            elif event.key == pygame.K_RETURN:
                # Return selected map index and map when Enter is pressed
                return "choose_map", self.selected_map_idx
            elif event.key == pygame.K_ESCAPE:
                return "quit", None
        return "continue", None

    def get_selected_map(self):
        """Returns the current selected map."""
        return self.game_map

    def get_sprites(self):
        return self.sprites
    def reset(self):
        self.selected_map_idx = 0
        self.game_map = self.load_map(self.maps[self.selected_map_idx])
    def update(self):
        """Updates the screen with the current map."""
        self.screen.fill((0, 0, 0)) 