import pygame
import sys

# Inicializar Pygame
pygame.init()

# Dimensiones de la pantalla
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Menú de Juego')

# Colores
WHITE = (255, 255, 255)

# Fuentes
font = pygame.font.Font(None, 60)

# Cargar la música de fondo
pygame.mixer.music.load('sonidos/menu.mp3')
pygame.mixer.music.set_volume(0.5)  # Ajustar el volumen (opcional)

# Cargar la imagen de fondo
background_image = pygame.image.load('sprites/imagenmenu.png').convert()
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Cargar las imágenes de los botones
play_button_image = pygame.image.load('sprites/boton_verde.png').convert_alpha()
quit_button_image = pygame.image.load('sprites/boton_verde.png').convert_alpha()

# Escalar las imágenes de los botones al tamaño deseado
play_button_image = pygame.transform.scale(play_button_image, (400, 100))
quit_button_image = pygame.transform.scale(quit_button_image, (400, 100))

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

def launch_game():
    import mapa
    mapa.start()

def main_menu():
    # Reproducir la música de fondo en bucle
    pygame.mixer.music.play(-1)  # El argumento -1 hace que se repita indefinidamente
    
    while True:
        screen.blit(background_image, (0, 0))  # Dibujar la imagen de fondo
        
        draw_text('SpacEscape', font, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)
        
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Botón de Jugar
        play_button_rect = play_button_image.get_rect(center=(SCREEN_WIDTH // 2, 500))
        screen.blit(play_button_image, play_button_rect.topleft)
        draw_text('Jugar', font, WHITE, screen, play_button_rect.centerx, play_button_rect.centery)
        
        # Botón de Salir
        quit_button_rect = quit_button_image.get_rect(center=(SCREEN_WIDTH // 2, 650))
        screen.blit(quit_button_image, quit_button_rect.topleft)
        draw_text('Salir', font, WHITE, screen, quit_button_rect.centerx, quit_button_rect.centery)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if play_button_rect.collidepoint(mouse_x, mouse_y):
                        # Detener la música antes de iniciar el juego
                        pygame.mixer.music.stop()
                        launch_game()  # Llamar a la función para iniciar el juego
                    elif quit_button_rect.collidepoint(mouse_x, mouse_y):
                        pygame.quit()
                        sys.exit()

        pygame.display.update()

if __name__ == '__main__':
    main_menu()
