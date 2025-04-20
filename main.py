import threading
import time
import pygame
from menu import Menu
from game import Game
from algorithm_viewer import AlgorithmViewer
from algorithm_viewer_2 import AlgorithmViewer2

# Constants
FPS = 30
SCREEN_TITLE = "Pac-Man Mini Map"
TILE_SIZE = 64
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 640

# Globals
menu = None
game = None
algorithm_viewer = None
algorithm_viewer_2 = None
game_map = None
game_state = None
isRunning = True

# Background update thread
def Update():
    global game_state, isRunning, menu, game, algorithm_viewer
    while isRunning:
        if game_state == "menu":
            menu.draw()
        elif game_state == "game":
            game.draw()
            if game.return_to_menu:
                game_state = "menu"
                game.cleanup()
        elif game_state == "watch":
            algorithm_viewer.update()
            algorithm_viewer.draw()
        time.sleep(0.2)

def main():
    global game_state, game, menu, algorithm_viewer, algorithm_viewer_2, algorithm_viewer_3, game_map

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(SCREEN_TITLE)
    clock = pygame.time.Clock()

    game_state = "menu"
    menu = Menu(screen)
    game = Game(screen)
    algorithm_viewer = AlgorithmViewer(screen)

    # Start update thread
    threading.Thread(target=Update, daemon=True).start()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.cleanup()
                pygame.quit()
                return

            if game_state == "menu":
                selected_mode = menu.handle_event(event)
                if selected_mode == "play":
                    game_state = "game"
                    game.reinit()
                    game.reset()
                elif selected_mode == "watch":
                    game_state = "watch"
                    algorithm_viewer.reset()

            elif game_state == "game":
                result = game.handle_event(event)
                if result == "menu":
                    game_state = "menu"
                    menu.draw()

            elif game_state == "watch":
                result, data = algorithm_viewer.handle_event(event)
                if result == "choose_map":
                    with open(algorithm_viewer.maps[data], 'r') as file:
                        game_map = [line.strip().split() for line in file]
                    algorithm_viewer_2 = AlgorithmViewer2(screen, game_map)
                    algorithm_viewer_2.draw()
                    game_state = "watch_2"
                elif result =="menu":
                    game_state = "menu"
                    menu.draw()

            elif game_state == "watch_2":
                result = algorithm_viewer_2.handle_event(event)
                if result == "viewer":
                    game_state = "watch"
                    algorithm_viewer.reset()
               
        if game_state == "menu":
            menu.draw()
        elif game_state == "game":
            time.sleep(0.1)
            game.handle_press()
            game.draw()
        elif game_state == "watch":
            algorithm_viewer.draw()
        elif game_state == "watch_2":
            algorithm_viewer_2.draw()

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
