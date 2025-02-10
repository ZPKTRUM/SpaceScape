import pygame
import random
import time
import sys

# Inicializa pygame
pygame.init()

# Configuración de la pantalla
ANCHO = 1920
ALTO = 1080
MARGEN = 5

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)

# Cargar imágenes
imagen_fondo = pygame.image.load('sprites/fondo2.jpg')
imagen_fondo = pygame.transform.scale(imagen_fondo, (ANCHO, ALTO))
imagen_cuadro = pygame.image.load('sprites/cuadro2.jpg')
imagen_deshacer = pygame.image.load('sprites/boton.png')

# Cargar música y sonidos
pygame.mixer.music.load('sonidos/puzzle.mp3')  # Música de fondo del nivel
sonido_game_over = pygame.mixer.Sound('sonidos/ouch-116112.mp3')  # Sonido de "Game Over"
victorySound = pygame.mixer.Sound('sonidos/victory.mp3')

# Crear la ventana
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Puzzle Deslizante")

# Niveles de dificultad
niveles = [2, 3, 4]
tiempos = [60, 120, 200]  # Tiempos en segundos para cada nivel
nivel_actual = 0

# Palabras por nivel
palabras_por_nivel = [
    ["Print", "('Hola", "Mundo')"],
    ["0(operation)", "1(/)", "2(//)", "3(+)", "4(-)", "5(%)", "6(:)", "7(<>)"],
    ["0(funtion:)", "1(def)", "2(bucles:)", "3(for_in)", "4(while)", "5(entrada:)", "6(input)", "7(salida:)", "8(print)", "9(errores)", "10(try)", "11(except)", "12(booleano)", "13(True)", "14(False)"]
]

def mezclar_puzzle(palabras, nivel):
    movimientos = 100  # Número de movimientos aleatorios para mezclar
    for _ in range(movimientos):
        espacio_vacio = palabras.index(None)
        fila_vacia = espacio_vacio // nivel
        columna_vacia = espacio_vacio % nivel

        # Seleccionar una dirección aleatoria
        direccion = random.choice(['arriba', 'abajo', 'izquierda', 'derecha'])
        if direccion == 'arriba' and fila_vacia < nivel - 1:
            mover_pieza(palabras, espacio_vacio + nivel, nivel, historial_movimientos)
        elif direccion == 'abajo' and fila_vacia > 0:
            mover_pieza(palabras, espacio_vacio - nivel, nivel, historial_movimientos)
        elif direccion == 'izquierda' and columna_vacia < nivel - 1:
            mover_pieza(palabras, espacio_vacio + 1, nivel, historial_movimientos)
        elif direccion == 'derecha' and columna_vacia > 0:
            mover_pieza(palabras, espacio_vacio - 1, nivel, historial_movimientos)

def crear_puzzle(nivel):
    palabras = palabras_por_nivel[nivel - 2][:nivel * nivel]
    random.shuffle(palabras)
    # Asegurar que el puzzle de 2x2 sea resoluble
    if nivel == 2:
        while not es_resoluble(palabras, nivel):
            random.shuffle(palabras)
    if (nivel == 3) or (nivel == 4):
        while not es_resoluble2(palabras, nivel):
            random.shuffle(palabras)
    palabras.append(None)
    
    # Mezclar el puzzle después de verificar que es resoluble
    mezclar_puzzle(palabras, nivel)

    return palabras, min(ANCHO // nivel, ALTO // nivel)

# Función para verificar si el puzzle es resoluble
def es_resoluble(palabras, nivel):
    inversiones = 0
    for i in range(len(palabras)):
        if palabras[i] is None:
            continue
        for j in range(i + 1, len(palabras)):
            if palabras[j] is not None and palabras[i] > palabras[j]:
                inversiones += 1
    return inversiones % 2 == 0

# Función para verificar si el puzzle es resoluble
def es_resoluble2(palabras, nivel):
    inversiones = 0
    for i in range(len(palabras)):
        if palabras[i] is None:
            continue
        for j in range(i + 1, len(palabras)):
            if palabras[j] is not None and palabras[i] > palabras[j]:
                inversiones += 1
    tamaño_cuadrado = len(palabras) ** 0.5
    tamaño_cuadrado = int(tamaño_cuadrado)
    fila_vacia = nivel - (inversiones // tamaño_cuadrado)
    return fila_vacia % 2 == 0

# Función para dibujar la cuadrícula
def dibujar_cuadricula(palabras, tamaño_cuadro, nivel):
    pantalla.blit(imagen_fondo, (0, 0))
    margen_x = (ANCHO - nivel * (tamaño_cuadro + MARGEN)) // 2
    margen_y = (ALTO - nivel * (tamaño_cuadro + MARGEN)) // 2
    tamaño_imagen_cuadro = (tamaño_cuadro, tamaño_cuadro)  # Nuevo tamaño de la imagen del cuadro

    for i in range(nivel):
        for j in range(nivel):
            indice = i * nivel + j
            if indice < len(palabras):
                palabra = palabras[indice]
                if palabra is not None:  # Solo dibujar el cuadro si hay una palabra
                    x = margen_x + j * (tamaño_cuadro + MARGEN)
                    y = margen_y + i * (tamaño_cuadro + MARGEN)
                    # Escalar la imagen del cuadro al tamaño del cuadro actual
                    imagen_cuadro_scaled = pygame.transform.scale(imagen_cuadro, tamaño_imagen_cuadro)
                    pantalla.blit(imagen_cuadro_scaled, (x, y))
                    
                    fuente = pygame.font.Font(None, 48)
                    texto = fuente.render(palabra, True, BLANCO)
                    texto_rect = texto.get_rect(center=(x + tamaño_cuadro // 2, y + tamaño_cuadro // 2))
                    pantalla.blit(texto, texto_rect.topleft)



# Función para mover una pieza
def mover_pieza(palabras, indice, nivel, historial_movimientos):
    fila_vacia = palabras.index(None) // nivel
    columna_vacia = palabras.index(None) % nivel
    fila, columna = indice // nivel, indice % nivel
    if (fila == fila_vacia and abs(columna - columna_vacia) == 1) or (columna == columna_vacia and abs(fila - fila_vacia) == 1):
        historial_movimientos.append({'indice': indice, 'nuevo_indice': palabras.index(None)})
        palabras[palabras.index(None)], palabras[indice] = palabras[indice], palabras[palabras.index(None)]

# Función para verificar si el puzzle está resuelto
def puzzle_resuelto(palabras, nivel):
    return palabras[:-1] == palabras_por_nivel[nivel - 2][:nivel * nivel]

# Función para mostrar el temporizador
def mostrar_tiempo(tiempo_restante):
    minutos = tiempo_restante // 60
    segundos = tiempo_restante % 60
    tiempo_texto = f"{minutos:02}:{segundos:02}"
    fuente = pygame.font.Font(None, 74)
    texto = fuente.render(tiempo_texto, True, ROJO)
    pantalla.blit(texto, (ANCHO // 2 - 50, ALTO - 75))

# Función para mostrar el mensaje de "Ganaste" por 5 segundos
def mostrar_ganaste():
    pantalla.fill(NEGRO)
    pygame.mixer.music.stop()
    victorySound.play()
    fuente = pygame.font.Font(None, 72)
    texto = fuente.render("¡Ganaste!", True, VERDE)
    texto_rect = texto.get_rect(center=(ANCHO // 2, ALTO // 2))
    pantalla.blit(texto, texto_rect)
    pygame.display.flip()
    time.sleep(5)  # Mostrar el mensaje por 5 segundos
    import mapa2
    mapa2.start()

# Función para mostrar "Game Over"
def mostrar_perdiste():
    pantalla.fill(NEGRO)
    fuente = pygame.font.Font(None, 72)
    font_small = pygame.font.Font(None, 36)
    texto = fuente.render("Game Over", True, ROJO)
    texto_rect = texto.get_rect(center=(ANCHO // 2, ALTO // 2))
    pantalla.blit(texto, texto_rect)
    pygame.display.flip()
    pygame.mixer.music.stop()  # Detener la música
    sonido_game_over.play()
    time.sleep(2)
    
    # Ajusta las posiciones Y para que estén un poco más abajo
    restart_surface = font_small.render("Presiona 'R' para reiniciar", True, BLANCO)
    restart_rect = restart_surface.get_rect(center=(ANCHO // 2, ALTO // 2 + 100))  # Moved down 100 pixels
    quit_surface = font_small.render("Presiona 'Q' para salir", True, BLANCO)
    quit_rect = quit_surface.get_rect(center=(ANCHO // 2, ALTO // 2 + 150))  # Moved down 150 pixels
    
    # Esperar la tecla correcta
    tecla_correcta = False
    while not tecla_correcta:
        pantalla.fill(NEGRO)
        pantalla.blit(texto, texto_rect)
        pantalla.blit(restart_surface, restart_rect)
        pantalla.blit(quit_surface, quit_rect)
        pygame.display.flip()  # Actualiza la pantalla en cada iteración
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Reiniciar juego con la tecla "R"
                    reiniciar_juego()
                    tecla_correcta = True
                elif event.key == pygame.K_q:  # Salir del juego con la tecla "Q"
                    pygame.quit()
                    sys.exit()
                    tecla_correcta = True
    
    # Esperar la tecla correcta
    tecla_correcta = False
    while not tecla_correcta:
        pantalla.fill(NEGRO)
        pantalla.blit(texto, texto_rect)
        pantalla.blit(restart_surface, restart_rect)
        pantalla.blit(quit_surface, quit_rect)
        pygame.display.flip()  # Actualiza la pantalla en cada iteración
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Reiniciar juego con la tecla "R"
                    reiniciar_juego()
                    tecla_correcta = True
                elif event.key == pygame.K_q:  # Salir del juego con la tecla "Q"
                    pygame.quit()
                    sys.exit()
                    tecla_correcta = True
# Definir una función para deshacer el movimiento
def deshacer_movimiento(palabras, historial_movimientos):
    if historial_movimientos:
        ultimo_movimiento = historial_movimientos.pop()
        palabras[ultimo_movimiento['indice']], palabras[ultimo_movimiento['nuevo_indice']] = palabras[ultimo_movimiento['nuevo_indice']], palabras[ultimo_movimiento['indice']]

# Lista para almacenar el historial de movimientos
historial_movimientos = []

# Reiniciar el juego con las nuevas funciones
def reiniciar_juego():
    global nivel_actual, palabras, tamaño_cuadro, tiempo_inicio, tiempo_limite, ejecutando, historial_movimientos

    nivel_actual = 0
    ejecutando = True
    historial_movimientos = []
    palabras, tamaño_cuadro = crear_puzzle(niveles[nivel_actual])
    tiempo_inicio = time.time()
    tiempo_limite = tiempos[nivel_actual]
    pygame.mixer.music.play(-1)  # Reproducir la música en bucle

# Inicializar el juego con las nuevas funciones
palabras, tamaño_cuadro = crear_puzzle(niveles[nivel_actual])
        
# Esperar a que se presione una tecla
def esperar_tecla():
    esperando = True
    while esperando:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                esperando = False
        pygame.time.wait(10)  # Añadir un pequeño retraso entre eventos

# Función para pasar al siguiente nivel
def siguiente_nivel():
    global nivel_actual, palabras, tamaño_cuadro, tiempo_inicio, tiempo_limite, historial_movimientos

    nivel_actual += 1
    historial_movimientos = []
    if nivel_actual < len(niveles):
        palabras, tamaño_cuadro = crear_puzzle(niveles[nivel_actual])
        tiempo_inicio = time.time()
        tiempo_limite = tiempos[nivel_actual]
    else:
        mostrar_ganaste()


def dibujar_botones():
    fuente = pygame.font.Font(None, 36)

    # Botón Deshacer
    texto_deshacer = fuente.render("Deshacer", True, BLANCO)
    texto_rect_deshacer = texto_deshacer.get_rect()
    ancho_deshacer = texto_rect_deshacer.width + 20  # Ancho del botón es el ancho del texto + 20 píxeles de margen
    rect_deshacer = pygame.Rect(ANCHO - ancho_deshacer - 20, 10, ancho_deshacer, 50)

    # Dibujar imagen del botón
    pantalla.blit(imagen_deshacer, (rect_deshacer.x, rect_deshacer.y))

    # Dibujar texto sobre la imagen
    pantalla.blit(texto_deshacer, (rect_deshacer.x + 10, rect_deshacer.y + 10))  # Ajustar posición del texto

    return rect_deshacer



    

# Inicializar el juego
palabras, tamaño_cuadro = crear_puzzle(niveles[nivel_actual])
tiempo_inicio = time.time()
tiempo_limite = tiempos[nivel_actual]
ejecutando = True
pygame.mixer.music.play(-1)  # Reproducir la música en bucle

# Bucle principal del juego
while ejecutando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ejecutando = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:  # Reiniciar juego con la tecla "R"
                reiniciar_juego()
            elif event.key == pygame.K_s:  # Salir del juego con la tecla "S"
                ejecutando = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            margen_x = (ANCHO - niveles[nivel_actual] * (tamaño_cuadro + MARGEN)) // 2
            margen_y = (ALTO - niveles[nivel_actual] * (tamaño_cuadro + MARGEN)) // 2
            columna = (x - margen_x) // (tamaño_cuadro + MARGEN)
            fila = (y - margen_y) // (tamaño_cuadro + MARGEN)
            indice = fila * niveles[nivel_actual] + columna
            if 0 <= columna < niveles[nivel_actual] and 0 <= fila < niveles[nivel_actual]:
                mover_pieza(palabras, indice, niveles[nivel_actual], historial_movimientos)
            
            # Verificar clic en el botón "Deshacer" (ampliado)
            if (ANCHO - 250) <= x <= (ANCHO - 50) and 10 <= y <= 60:
                deshacer_movimiento(palabras, historial_movimientos)


    # Calcular el tiempo restante
    tiempo_actual = time.time()
    tiempo_transcurrido = tiempo_actual - tiempo_inicio
    tiempo_restante = int(tiempo_limite - tiempo_transcurrido)

    # Dibujar la cuadrícula y el temporizador
    dibujar_cuadricula(palabras, tamaño_cuadro, niveles[nivel_actual])
    mostrar_tiempo(tiempo_restante)
    dibujar_botones()
    pygame.display.flip()
    
    # Verificar si el puzzle está resuelto
    if puzzle_resuelto(palabras, niveles[nivel_actual]):
        # Si se resuelve el puzzle del nivel actual, pasar al siguiente nivel
        nivel_actual += 1
        # Verificar si se completaron todos los niveles
        if nivel_actual == len(niveles):
            mostrar_ganaste()  # Mostrar "¡Ganaste!" después de completar todos los niveles
            ejecutando = False
            break
        else:
            palabras, tamaño_cuadro = crear_puzzle(niveles[nivel_actual])
            tiempo_inicio = time.time()
            tiempo_limite = tiempos[nivel_actual]

    # Verificar si el tiempo se ha agotado
    if tiempo_restante <= 0:
        mostrar_perdiste()
        reiniciar_juego()

# Salir del juego
pygame.quit()
