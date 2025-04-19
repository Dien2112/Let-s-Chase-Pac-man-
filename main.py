import pygame
from menu import Menu
from game import Game
from algorithm_viewer import AlgorithmViewer
from algorithm_viewer_2 import AlgorithmViewer2
from algorithm_viewer_3 import AlgorithmViewer3

# Constants
FPS = 30
SCREEN_TITLE = "Pac-Man Mini Map"

# Load map to determine screen size
with open('map1.txt', 'r') as file:
    game_map = [line.strip().split() for line in file]
TILE_SIZE = 64
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 640

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(SCREEN_TITLE)
    clock = pygame.time.Clock()

    # Initialize game modes
    menu = Menu(screen)
    game = Game(screen)
    algorithm_viewer = AlgorithmViewer(screen)
    algorithm_viewer_2 = None
    algorithm_viewer_3 = None
    game_map = None

    game_state = "menu"

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
                    game.reset()
                elif selected_mode == "watch":
                    game_state = "watch"
                    algorithm_viewer.reset()
            elif game_state == "game":
                game.handle_event(event)
            elif game_state == "watch":
                result, data = algorithm_viewer.handle_event(event)
                print(result, data)
                if result == "choose_map":
                    # Load map based on selected index
                    selected_map = algorithm_viewer.maps[data]
                    with open(selected_map, 'r') as file:
                        game_map = [line.strip().split() for line in file]
                    algorithm_viewer_2 = AlgorithmViewer2(screen, game_map)
                    algorithm_viewer_2.draw()
                    game_state = "watch_2"
            elif game_state == "watch_2":
                result, data = algorithm_viewer_2.handle_event(event)
                print(result, data)
                if result == "choose_pacman_pos":
                    # Proceed to stage 3 with selected algorithm
                    algorithm_viewer_3 = AlgorithmViewer3(screen, game_map, data)
                    print("Algorithm selected:", data)
                    algorithm_viewer_3.draw()
                    game_state = "watch_3"

            elif game_state == "watch_3":
                algorithm_viewer_3.handle_event(event)

            elif result == "quit":
                game_state = "menu"


            # Update and draw
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
    
            pygame.display.flip()
            clock.tick(FPS)

if __name__ == "__main__":
    main()