import pygame

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.bg_image = pygame.image.load("assets/main_screen.png")
        self.bg_image = pygame.transform.scale(self.bg_image, self.screen.get_size())
        self.play_img = pygame.image.load("assets/play_button.png")
        self.play_hover_img = pygame.image.load("assets/play_button_hover.png")
        self.watch_img = pygame.image.load("assets/watch_algorithm_button.png")
        self.watch_hover_img = pygame.image.load("assets/watch_algorithm_button_hover.png")
        self.play_pos = (self.screen.get_width() // 2 - self.play_img.get_width() // 2, 300)
        self.watch_pos = (self.screen.get_width() // 2 - self.watch_img.get_width() // 2, 400)
        self.play_rect = self.play_img.get_rect(topleft=self.play_pos)
        self.watch_rect = self.watch_img.get_rect(topleft=self.watch_pos)

    def draw(self):
        self.screen.blit(self.bg_image, (0, 0))
        mouse_pos = pygame.mouse.get_pos()
        if self.play_rect.collidepoint(mouse_pos):
            self.screen.blit(self.play_hover_img, self.play_pos)
        else:
            self.screen.blit(self.play_img, self.play_pos)
        if self.watch_rect.collidepoint(mouse_pos):
            self.screen.blit(self.watch_hover_img, self.watch_pos)
        else:
            self.screen.blit(self.watch_img, self.watch_pos)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if self.play_rect.collidepoint(mouse_pos):
                return "play"
            if self.watch_rect.collidepoint(mouse_pos):
                return "watch"
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "menu"
        return None
