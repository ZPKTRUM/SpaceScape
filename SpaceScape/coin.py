import pygame

class Coin:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 20, 20)  # Ajustar el tamaño del rectángulo de la moneda
        self.collected = False  # Estado de recolección de la moneda
        self.image = pygame.image.load("sprites/coin.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (20, 20))  # Redimensionar la imagen de la moneda

    def draw(self, surface, camera_x, camera_y):
        if not self.collected:
            surface.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))

    def collect(self, player_rect):
        if self.rect.colliderect(player_rect) and not self.collected:
            self.collected = True
            return True
        return False
