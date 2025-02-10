import pygame


# Inicializa Pygame
pygame.init()

# Configuración de la pantalla
screen_width, screen_height = 1920, 1080
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("SpaceEscape - Créditos")

# Colores
black = (0, 0, 0)
white = (255, 255, 255)

# Configuración de la fuente
font = pygame.font.Font(None, 74)

# Mensajes de los créditos
credits = [
    "SpaceEscape",
    "Videojuego creado por: Azul Alanya",
    "Videojuego creado por: Aylin Herrera",
    "Videojuego creado por: Sergio Villegas",
    "Gracias por jugar"
]

# Función para mostrar un mensaje en la pantalla
def show_message(screen, message, font, color, delay):
    screen.fill(black)
    text = font.render(message, True, color)
    text_rect = text.get_rect(center=(screen_width / 2, screen_height / 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.wait(delay)

# Loop principal
def main():
    # Inicializar el mezclador de sonido
    pygame.mixer.init()

    # Cargar y reproducir la música
    pygame.mixer.music.load("sonidos/Supernova.mp3")
    pygame.mixer.music.play(-1)  # -1 para que la música se repita indefinidamente

    for message in credits:
        show_message(screen, message, font, white, 3150)

    # Esperar un poco antes de salir
    pygame.time.wait(2000)

    # Detener la música
    pygame.mixer.music.stop()

    # Salir del juego
    import menu
    menu.main_menu()

if __name__ == "__main__":
    main()
