import pygame

class Enemigo:
    def __init__(self, x, y, velocidad, sprite_sheet, frame_count, animation_speed, sprite_size=64):
        self.sprite_size = sprite_size
        self.rect = pygame.Rect(x, y, sprite_size, sprite_size)
        self.velocidad = velocidad
        self.sprite_sheet = sprite_sheet
        self.frame_count = frame_count
        self.animation_speed = animation_speed
        self.current_frame = 0
        self.current_direction = 'down'
        self.directions = {
            'down': 0,
            'left': 1,
            'right': 2,
            'up': 3
        }

    def mover(self, jugador_pos):
        # Movimiento básico del enemigo hacia el jugador
        if self.rect.x < jugador_pos.x:
            self.rect.x += self.velocidad
            self.current_direction = 'right'
        elif self.rect.x > jugador_pos.x:
            self.rect.x -= self.velocidad
            self.current_direction = 'left'

        if self.rect.y < jugador_pos.y:
            self.rect.y += self.velocidad
            self.current_direction = 'down'
        elif self.rect.y > jugador_pos.y:
            self.rect.y -= self.velocidad
            self.current_direction = 'up'

        self.current_frame += self.animation_speed
        if self.current_frame >= self.frame_count:
            self.current_frame = 0

    def dibujar(self, pantalla, camara_x, camara_y):
        row = self.directions[self.current_direction]
        col = int(self.current_frame) % self.frame_count
        sprite = self.sprite_sheet.subsurface(pygame.Rect(col * self.sprite_size, row * self.sprite_size, self.sprite_size, self.sprite_size))
        pantalla.blit(sprite, (self.rect.x - camara_x, self.rect.y - camara_y))
