#librerias que se usaron
import pygame
from pygame.locals import *
import time
import math
import random
import requests
import io
from urllib.request import urlopen
from math import floor

pygame.init()

# Colores elegidos 
black = (0, 0, 0)
gold = (218, 165, 32)
grey = (200, 200, 200)
green = (0, 200, 0)
red = (200, 0, 0)
white = (255, 255, 255)
gold = (255, 215, 0)

# para crear la ventana del juego
ventana_ancho = 500
ventana_alto = 500

size = (ventana_ancho, ventana_alto)  # Tamaño de la ventana
ventana = pygame.display.set_mode(size)  # Establecemos la ventana principal
game = pygame.display.set_mode(size)  
pygame.display.set_caption("Clash Planet")  # Nombre que aparecerá en la parte superior de la ventana

# Creamos un reloj para controlar la velocidad de actualización de la pantalla (FPS)
clock = pygame.time.Clock()

# Cargamos las fuentes para el texto que se verá en el juego
# Primero, cargamos una imagen para usar como fuente
font = pygame.image.load("font.png").convert()

font.set_colorkey((0, 0, 0))  # Establecemos el color negro como transparente para la imagen

# Después, cargamos fuentes TrueType para el texto en el juego
font2 = pygame.font.Font("Tiny5-Regular.ttf", 36) #Titulos
font3 = pygame.font.Font("Tiny5-Regular.ttf", 24)  #Texto general


#para el font 1
order = ["`", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "+", "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "_", "=", "{", "}", "[", "]", "|", "/", ":", ";", '"', "'", "<", ",", ">", ".", "?", "/", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]

# Para cuando se imprima
# espacios entre las letras
spacing = 6
# Tamaño de las letras en pixeles
charsize = 8
# cuántos caracteres pueden caber en una línea antes de que el texto se "salte" a la siguiente línea
widthlmt = 16
# es un contador o índice que se utiliza para realizar un seguimiento de qué carácter del texto se está procesando y mostrando en ese momento
index = 0

# Función para cargar una parte específica de una imagen (spritesheet)
# Recibe la imagen original y un "crop" que define la sección de la imagen a cortar
# Devuelve una nueva imagen con esa sección
def load_spritesheet(image, crop):
	new_image = image.subsurface(crop[0] * crop[2], crop[1] * crop[3], crop[2], crop[3])

	return new_image
    
# Función para renderizar el texto en la pantalla
# Recibe el texto a mostrar y la posición en la que se va a dibujar el texto

def rendertext(text, pos):
	# posición inicial [0, 0]
	charpos = [0, 0]

	# calcula cuantos caracters cabe en la hoja 
	sheetwidth = (font.get_width() / charsize)
		
	# Recorremos cada carácter en el texto que queremos mostrar
	for char in text:	
		if char in order: # Si el carácter está en nuestra lista de caracteres válidos
			# calcular la posición del carácter
			surf = load_spritesheet(font, (order.index(char) % sheetwidth, floor(order.index(char) / sheetwidth), charsize, charsize))
			
			#renderiza la imagen del carácter en cierta posición
			game.blit(surf, (charpos[0] + pos[0], charpos[1] + pos[1]))
			charpos[0] += spacing

		# si el carácter es un espcaio, se va a mover la posición actual
		if char == " ":
			charpos[0] += spacing

		# comprobar si el texto llegó al limite del espacio disponible, si es asi, salta una linea 
		if charpos[0] / spacing > widthlmt and char == " ":
			charpos[0] = 0
			charpos[1] += charsize + 2

# variables de texto
delaytimer = 0
delayedtext = ""
done = False
index = 0

# Función que renderiza el texto con un tipo de efecto, mostrando un carácter a la vez con un retraso
# Entrada:
#   - text (str): El texto que se desea mostrar en la pantalla.
#   - pos (list): Lista con las coordenadas [x, y] de la posición donde se dibujará el texto.
#   - delay (int): Retraso entre cada carácter en el texto (en frames).
# Salida: None

def rendertexttype(text, pos, delay):
	# variables
	global delaytimer, delayedtext, done, index
	#incrementa el contador cada vez que se llama la funcion
	delaytimer += 1
	if not done:
		if delay < delaytimer:
			if index < len(text):
				#reinicia el temporizador 
				delaytimer = 0
                #agrega el caracter que sigue
				delayedtext = delayedtext + text[index]
				index += 1
			else:
				done = True

	#dibuja el texto en la ventana
	rendertext(delayedtext, pos)

# por fuera del bucle principal del juego para que se muestre como la "historia"
# Función para mostrar la introducción del juego en pantalla
#No recibe argumentos y tampoco los retorna 

def mostrar_intro():
    musica("Ruins.mp3")
    tiempo_inicio = pygame.time.get_ticks()  # Captura el tiempo inicial
    duracion_intro = 25000 # Duración de la introducción en milisegundos (5000 ms = 5 segundos)
    
    # Para correr la pantalla
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:   # Si el jugador cierra la ventana
                run = False
                
        # Calcula el tiempo transcurrido desde que comenzó la introducción
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual -tiempo_inicio >= duracion_intro:
            run = False
        # Para actualizar la pantalla
        game.fill((0, 0, 20))

        rendertexttype('"El ser humano por naturaleza es avaricios" lleno de armas a la Tierra y la mando a atacar a todos los planetas con el objetivo de poder usar los materiales que ofrecian los otros planetas, tal y como lo hicieron con la Tierra."', [100, 50], 5)  
        clock.tick(60) # Limita a 60 cuadros por segundo
        
        pygame.display.update()

# Función para dibujar texto en la pantalla con una fuente específica y color
# Entrada:
#   - texto (str): El texto que se desea mostrar en la pantalla.
#   - fuente (pygame.font.Font): La fuente utilizada para renderizar el texto.
#   - color (tuple): Color del texto en formato (R, G, B).
#   - superficie (pygame.Surface): Superficie donde se dibujará el texto.
#   - x (int): Posición horizontal (x) donde se dibujará el texto.
#   - y (int): Posición vertical (y) donde se dibujará el texto.
# Salida: None

def dibujar_texto(texto, fuente, color, superficie, x, y):
    texto_renderizado = fuente.render(texto, True, color)
    superficie.blit(texto_renderizado, (x, y))
    
# Función para dibujar botones con bordes en la pantalla
# Entrada:
#   - surface (pygame.Surface): La superficie donde se dibujará el botón.
#   - boton (pygame.Rect): Un objeto Rect que define las dimensiones y posición del botón.
#   - color_fondo (tuple): El color de fondo del botón en formato (R, G, B).
#   - color_borde (tuple): El color del borde del botón en formato (R, G, B).
#   - grosor_borde (int): El grosor del borde del botón.
# Salida: None

def dibujar_boton(surface, boton, color_fondo, color_borde, grosor_borde):
    # Dibujar el fondo negro del botón
    pygame.draw.rect(surface, color_fondo, boton)
    # Dibujar el borde blanco
    pygame.draw.rect(surface, color_borde, boton, grosor_borde)
    
# Función que muestra el menú inicial del juego con botones para jugar o salir

def menu():
    # Texto que aparecerá en el menú
    texto = "Clash Planet"
    # Posición en la que se dibujará el texto en la pantalla
    pos_texto = [ventana_ancho / 2 -100, ventana_alto / 2- 220]

    # Definición de los botones (rectángulos) para jugar y salir
    boton_jugar = pygame.Rect(ventana_ancho / 2 - 100, ventana_alto / 2 - 50, 200, 50)
    boton_salir = pygame.Rect(ventana_ancho / 2 - 100, ventana_alto / 2 + 50, 200, 50)
    
    # Reproduce la música del menú
    musica("menu.mp3")

    # Bucle principal del menú
    bg= pygame.image.load("background.png")
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Si se cierra la ventana
                run = False

            # Detecta clics en los botones
            if event.type == MOUSEBUTTONDOWN:
                # Si el clic es dentro del botón "Jugar"
                if boton_jugar.collidepoint(event.pos):
                    print("Iniciar juego...")
                    game_loop()  # Llama a la función para iniciar el juego

                    return  # Sale del menú y comienza el juego
                    
                # Si el clic es dentro del botón "Salir"
                elif boton_salir.collidepoint(event.pos):
                    print("Salir del juego...")
                    pygame.quit()  # Cierra la ventana de Pygame
                    exit()  # Sale del juego

        ventana.blit(bg , [0,0])  # Limpia la ventana con el color negro

        dibujar_texto(texto, font2, white, ventana, pos_texto[0], pos_texto[1])

        # Dibujar botones
        dibujar_boton(ventana, boton_jugar, black, white,2)
        dibujar_boton(ventana, boton_salir, black, white, 2)

        # Dibujar texto en los botones
        dibujar_texto("Jugar", font2, white, ventana, ventana_ancho / 2 - 40, ventana_alto / 2 - 40)
        dibujar_texto("Salir", font2, white, ventana, ventana_ancho / 2 - 40, ventana_alto / 2 + 60)

        pygame.display.update()
        clock.tick(60)
        
# Clase que representa un tipo de ataque en el juego.
# Entrada:
#   - name (str): Nombre del tipo de ataque (por ejemplo, fuego, agua, etc.)
#   - fuerte (list, opcional): Lista de tipos de ataques que son más fuertes contra este tipo.
#   - debil (list, opcional): Lista de tipos de ataques que son débiles contra este tipo.
# Salida: None

class MoveType():
    def __init__(self, name, fuerte=None, debil=None):
        # nombre del tipo de ataque
        self.name = []
        # ataques que son más fuertes
        self.fuerte = []
        # ataques que son más débil 
        self.debil = []
# Método que verifica si este tipo de ataque es efectivo contra otro tipo.
# Entrada:
#    - other_type (MoveType): El tipo de ataque del objetivo.
# Salida:
#    - bool: Devuelve True si el ataque es fuerte contra el otro tipo, False en caso contrario.            
    def is_effective_against(self, other_type):
        return other_type in self.fuerte # ve si es fuerte contra el otro tipo

# Método que verifica si este tipo de ataque es débil contra otro tipo.
# Entrada:
#   - other_type (MoveType): El tipo de ataque del objetivo.
# Salida:
#   - bool: Devuelve True si el ataque es débil contra el otro tipo, False en caso contrario.             
    def is_weak_against(self, other_type):
        return other_type in self.debil  # ve si es debil
        
#-----------------------------------------------------------
# Clase que representa un ataque específico en el juego.
# Entrada:
#   - name (str): Nombre del ataque (por ejemplo, "Lanzallamas").
#   - power (int): El poder del ataque (cuánto daño hace).
#   - move_type (MoveType): El tipo de ataque (por ejemplo, fuego, agua, etc.).
# Salida:
#   - None

class Move:
    def __init__(self, name, power, move_type):
        #nombre del ataque
        self.name = name
        # daño que hace
        self.power = power
        # tipo de ataque
        self.type = move_type

# Método que calcula el daño de un ataque en función del tipo de objetivo.
# Entrada:
#   - target_type (MoveType): El tipo de ataque del objetivo.
# Salida:
#   - int: El daño calculado que se hace al objetivo.

    def calculate_damage(self, target_type):
        if self.type.is_effective_against(target_type):
            return self.power * 2  # Doble de daño si es efectivo
        elif self.type.is_weak_against(target_type):
            return self.power / 2  # Mitad de daño si es débil
        else:
            return self.power  # Daño normal
            
# Método que ejecuta el ataque sobre un objetivo.
# Entrada:
#   - atacante (objeto): El objeto que realiza el ataque (jugador o un enemigo).
#   - objetivo (objeto): El objeto que recibe el ataque.
# Salida:
#   - None   
    def ejecutar(self, atacante, objetivo):
        objetivo.recibir_daño(self.calculate_damage(objetivo)) 
        
#---------------------------------------------------
# Clase que represeenta a la Tierra como personaje del juego.
#   - x (int): Posición horizontal inicial de la Tierra.
#   - y (int): Posición vertical inicial de la Tierra.
#   - image (str): Ruta de la imagen para representar a la Tierra.
#   - vida (int): Vida inicial de la Tierra.
#   - daño_base (int): Daño base que realiza la Tierra.
#   - level (int): Nivel inicial de la Tierra.
#   - nombre (str): Nombre del personaje (en este caso, "Tierra").
#   -Move (list): Lista de movimientos o habilidades disponibles.
# Salida:
#   - None 
class Tierra(pygame.sprite.Sprite):
    def __init__(self, x, y, image, vida,daño_base,level, nombre, Move):
        super().__init__()
        self.x = x  # Posición horizontal.
        self.y = y  # Posición vertical.
        self.image = pygame.image.load(image).convert_alpha()  # Carga y convierte la imagen.
        self.image = pygame.transform.scale(self.image, (80, 80))  # Escala la imagen a un tamaño fijo.
        self.rect = self.image.get_rect(center=(x, y))  # Define el rectángulo para la posición.
        self.vida = vida  # Vida actual de la Tierra.
        self.vida_max = vida  # Vida máxima de la Tierra.
        self.daño_base = daño_base  # Daño base de la Tierra.
        self.defensa_activa = False  # Indica si la defensa está activa.
        self.exito=1.0
        self.habilidades = []  # Lista de habilidades desbloqueadas.
        self.experiencia = 0  # Experiencia acumulada.
        self.level = level  # Nivel actual.
        self.nombre = nombre  # Nombre del personaje.
        self.Move = Move  # Lista de movimientos o habilidades.

 # Método que permite a la Tierra subir de nivel.
    def subir_nivel(self):
        #son 8 niveles
        if self.level<8:
            self.level+=1
            #cada vez que suba de nivel, se va a ganar una habilidad
            self.ganar_habilidad()
        else:
            print("No puedes subir de nivel, estas en el máximo")
            
    # Método que otorga una habilidad nueva basada en el nivel actual.          
    def ganar_habilidad(self):
        habilidades_por_nivel = {
            2: ataque_rapido,
            3: defensa_termica,
            4: tormenta_polvo,
            5: gravedad_aumentada,
            6: anillos_defensas,
            7: viento_solar,
            8: tormenta_neptuno,
        }
        habilidad_nueva = habilidades_por_nivel.get(self.level)
        #agregar la habilidad
        if habilidad_nueva:
            #controlar que solo haya cuatro movimientos
            if len(self.Move)>=4:
                #elimina el primer movimiento
                self.Move.pop(0)
            #añade la habilidad como movimiento
            self.Move.append(habilidad_nueva)
            print(f"Se ha desbloqueado la habilidad {habilidad_nueva.name}")

# Método para realizar un ataque al objetivo
# recibe: objetivo (objeto): Personaje que recibirá el daño
#		  daño extra (int): Cuanto daño adicional comete
    def atacar(self, objetivo, daño_extra=0):
        #calcular el daño total
        daño_total = self.daño_base + daño_extra
        if objetivo.defensa_activa:  # Aplica reducción de daño si la defensa está activa
            daño_total *= 0.8
            objetivo.defensa_activa = False
        objetivo.vida -= daño_total
        if objetivo.vida <= 0:
            print(f"{objetivo.nombre} ha sido derrotado.")
    # Método para recibir daño
    def recibir_daño(self, daño):
        self.vida -= daño
        if self.vida < 0:
            self.vida = 0 
    # Método para usar una habilidad
    def usar_habilidad(self, indice, objetivo, ronda=None):
        if 0 <= indice < len(self.habilidades):
            self.habilidades[indice].activar(self, objetivo, ronda)
        else:
            print(f"No existe la habilidad en el índice {indice}.")
# Método para dibujar al personaje en la superficie de juego
    def dibujar_personaje(self, surface, scale_factor=1):
        if scale_factor != 1:
            imagen = pygame.transform.scale(self.image, (int(self.rect.width * scale_factor), int(self.rect.height * scale_factor)))
            surface.blit(imagen, self.rect)
        else:
            # si no se da un factor se dibujala imagen sin cambiar su tamaño
            surface.blit(self.image, self.rect)

# Método para la barra de vida en la superficie de juego
    def dibujar_hp(self, surface):
        pygame.draw.rect(surface, red, (self.x - 40, self.y - 60, 80, 10))
        vida_actual = (self.vida / self.vida_max) * 80
        pygame.draw.rect(surface, gold, (self.x - 40, self.y - 60, vida_actual, 10))

#------------------------------------------------------------
# Clase Enemy representa un enemigo en el juego. Contiene atributos como vida, daño base, nivel y habilidades.
class Enemy(pygame.sprite.Sprite):
# crea al enemigo con posición, imagen, estadísticas y movimientos.
# Entrada: 
# - x, y (int): Coordenadas del enemigo.
# - image (str): Ruta a la imagen del enemigo.
# - vida, daño_base (int): Estadísticas del enemigo.
# - level (int): Nivel del enemigo.
# - nombre (str): Nombre del enemigo.
# - Move (list): Lista de movimientos del enemigo (opcional).
# Salida: None

    def __init__(self, x, y, image, vida,daño_base,level,nombre, Move=None):
        super().__init__()
        self.x = x
        self.y = y
        self.image = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale(self.image, (80, 80)) 
        self.rect = self.image.get_rect(center=(x, y))
        self.vida = vida
        self.daño_base=daño_base
        self.defensa_activa = False
        self.exito=1.0
        self.habilidades = []
        self.level=level
        self.nombre = nombre
        self.vida_max = vida
        self.Move = Move if Move else []
# Agrega una habilidad al enemigo y la asocia con un tipo de ataque.
        # Entrada:
        # - habilidad (object): Objeto de habilidad a asociar.
        # - tipo_ataque (str): Tipo de ataque relacionado con la habilidad.
        # Salida: None
    def agregar_habilidad(self, habilidad, tipo_ataque):
        habilidad.tipo_ataque = tipo_ataque
        self.habilidades.append(habilidad)
 # Realiza un ataque contra el objetivo, considerando daño base y adicional.
        # Entrada:
        # - objetivo (object): Objeto del objetivo que recibirá el daño.
        # - daño_extra (int): Cantidad de daño adicional.
        # Salida: None
    def atacar(self, objetivo, daño_extra=0):
        daño_total = self.daño_base + daño_extra
        if objetivo.defensa_activa:
            daño_total *= 0.8
            objetivo.defensa_activa = False
        objetivo.vida -= daño_total
        print(f"{self.nombre} ataca a {objetivo.nombre}, causando {daño_total} de daño.")
        if objetivo.vida <= 0:
            print(f"{objetivo.nombre} ha sido derrotado.")

 # Reduce la vida del enemigo al recibir daño. Ajusta la vida si es menor a 0.
        # Entrada:
        # - daño (float): Cantidad de daño recibido.
        # Salida: None
    def recibir_daño(self, daño):
        self.vida -= daño
        if self.vida < 0:
            self.vida = 0 
    
        print(f"{self.nombre} recibió {daño:.2f} de daño. Vida restante: {self.vida:.2f}")
#------------------------------------------------------
# Permite al personaje usar una habilidad desde su lista de habilidades en el índice especificado.
# Entrada:
# - indice (int): Índice de la habilidad en la lista de habilidades.
# - objetivo (object): El objetivo sobre el cual se aplicará la habilidad.
# - ronda (int): Número de ronda.
# Salida: None
    def usar_habilidad(self, indice, objetivo, ronda=None):
        if 0 <= indice < len(self.habilidades):
            self.habilidades[indice].activar(self, objetivo, ronda)
        else:
            print(f"No existe la habilidad en el índice {indice}.")
     # Dibuja la imagen del personaje sobre la superficie proporcionada, con opción de redimensionarla.
        # Entrada:
        # - surface (object): Superficie de Pygame sobre la cual se dibuja el personaje.
        # - scale_factor (float): Factor de escala para redimensionar la imagen (por defecto es 1).
        # Salida: None
    def dibujar_personaje(self, surface, scale_factor=1):
            # Si se proporciona un factor de escala, redimensionamos la imagen
        if scale_factor != 1:
            imagen = pygame.transform.scale(self.image, (int(self.rect.width * scale_factor), int(self.rect.height * scale_factor)))
            surface.blit(imagen, self.rect)
        else:
            # Si no se da  el factor, se dibuja la imagen sin cambiar su tamaño
            surface.blit(self.image, self.rect)
 # Dibuja la barra de vida del personaje sobre la superficie.
 # Entrada:
 # - surface (object): Superficie de Pygame sobre la cual se dibuja la barra de vida.
 # Salida: None
    def dibujar_hp(self, surface):
        # fondo de barra
        pygame.draw.rect(surface, red,(self.x - 40, self.y - 60, 80, 10)) #fondo de la barra
        vida_actual = (self.vida / self.vida_max) * 80  # Calcula la vida actual en proporción a la barra
        pygame.draw.rect(surface, gold, (self.x - 40, self.y - 60, vida_actual, 10)) #barra
        

#--------------------------------------------------------------------
#mas funciones que se usan en el loop principal
# Función que crea un botón en la pantalla y detecta si el jugador hace clic en él.
# Entrada:
# - screen (object): Superficie de Pygame donde se dibujará el botón.
# - font (object): Fuente utilizada para mostrar el texto en el botón.
# - color (tuple): Color del botón cuando el mouse no está sobre él (RGB).
# - hover_color (tuple): Color del botón cuando el mouse pasa por encima (RGB).
# - width (int): Ancho del botón.
# - height (int): Alto del botón.
# - left (int): Coordenada x del borde izquierdo del botón.
# - top (int): Coordenada y del borde superior del botón.
# - text_color (tuple): Color del texto en el botón (RGB).
# - label (str): Texto que se mostrará en el botón.
# Salida:
# - (bool): True si el jugador hace clic en el botón, False en caso contrario.
def create_button(screen, font, color, hover_color, width, height, left, top, text_color, label):
    # Se obtiene la posición del cursor del ratón
    mouse_cursor = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    button = pygame.Rect(left, top, width, height) #rectángulo que representa la posición y el tamaño del botón
    if button.collidepoint(mouse_cursor): # Verifica si el mouse está sobre el botón
        pygame.draw.rect(screen, hover_color, button)
        if click[0]:
            # Si el jugador hace clic, devuelve True
            return True
    else:
        # Si el mouse no está sobre el botón, se dibuja con el color normal
        pygame.draw.rect(screen, color, button)

    # Renderiza el texto y lo coloca en el centro del botón
    text = font3.render(label, True, text_color)
    text_rect = text.get_rect(center=button.center)
    screen.blit(text, text_rect)

    # Retorna False si no se hizo clic en el botón
    return False
#----------------------
 # Función que muestra un mensaje en la pantalla.
# Entrada:
# - message (str): El mensaje que se mostrará en la pantalla.
# Salida: Ninguna
def display_message(message):
    # Dibuja un cuadro de fondo para el mensaje
    pygame.draw.rect(game, white, (10, 350, 480, 140))
    pygame.draw.rect(game, white, (10, 350, 480, 140), 3)

    # Renderiza el mensaje y lo coloca en la pantalla
    text = font3.render(message, True, white)
    text_rect = text.get_rect()
    text_rect.x = 30
    text_rect.y = 410
    game.blit(text, text_rect)

    # Actualiza la pantalla para mostrar el mensaje
    pygame.display.update()
#------------------------
# Función que muestra un mensaje cuando el jugador sube de nivel.
def mostrar_nivel_subido():
    ventana.fill(green)  # Llena la ventana de color negro.
    
    # Crea un texto que dice que el jugador subió de nivel
    texto = f"¡Has subido de nivel! Ahora eres nivel {tierra.level}"
    
    # Calcula el tamaño del texto para centrarlo
    texto_width, texto_height = font3.size(texto)
    texto_x = (ventana_ancho - texto_width) // 2  # Centra el texto en el eje X.
    texto_y = 200  # Margen superior.
    
    # Dibuja el texto en la pantalla
    dibujar_texto(texto, font3, white, ventana, texto_x, texto_y)
    
    # Configura las dimensiones de los botones
    button_width, button_height = 150, 40
    margen_x = (ventana_ancho - button_width* 2-20) // 2  # Centra los botones horizontalmente
    margen_y = ventana_alto - 250  # Ajusta la posición vertical de los botones
    spacing_x = 20  # Espacio entre los botones

    # Define las posiciones de los botones
    button_positions = [
        (margen_x, margen_y),  # Botón "Seguir jugando"
        (margen_x + button_width + spacing_x, margen_y)  # Botón "Salir"
    ]
    
    # Dibuja los botones y maneja las interacciones
    for i, (pos_x, pos_y) in enumerate(button_positions):
        if create_button(ventana, font3, white, grey, button_width, button_height, pos_x, pos_y, black, ["Seguir jugando", "Salir"][i]):
            # Si el jugador hace clic en "Seguir jugando", retorna "continue"
            if i == 0:
                return "continue"
            # Si hace clic en "Salir", retorna "exit"
            elif i == 1:
                return "exit"

    # Actualiza la pantalla para reflejar los cambios
    pygame.display.update()
    clock.tick(60)

#------------------------------------

# Pantalla para cuando se termina la batalla
# Esta función muestra la pantalla de "Game Over" y ofrece las opciones para continuar o salir.
# Entrada: Ninguna
# Salida: Devuelve "continue" si se elige seguir jugando, "exit" si se elige salir.
def mostrar_game_over():
    # cambia el fondo a rojo oscuro
    ventana.fill(((139, 0, 0))) 
    # Dibuja "Game Over" centrado en la pantalla
    texto = "Game Over"
    texto_width, texto_height = font2.size(texto)
    texto_x = (ventana_ancho - texto_width) // 2  # Centra el texto en el eje x (horizontal)
    texto_y = (ventana_alto - texto_height) // 2 - 50  # Centra el texto en el eje y (vertical) con un margen 
    dibujar_texto(texto, font2, white, ventana, texto_x, texto_y)  # Dibuja el texto "Game Over" en la ventana
    button_width, button_height = 150, 40  # Tamaño de los botones "Seguir intentándolo" y "Salir"
    margen_x = (ventana_ancho - button_width * 2 - 20) // 2  # Calcula la posición x para centrar los botones
    margen_y = ventana_alto - 250  # Posición y de los botones, colocados en la parte inferior de la pantalla
    spacing_x = 20  # Espaciado horizontal entre los botones

    # Posición de los botones
    button_positions = [
        (margen_x, margen_y),  # Botón de "Seguir intentándolo"
        (margen_x + button_width + spacing_x, margen_y)  # Botón para "Salir"
    ]


    # para que los botones estén centrados
    for i, (pos_x, pos_y) in enumerate(button_positions):
        if create_button(ventana, font3, white, grey, button_width, button_height, pos_x, pos_y, black, ["Seguir", "Salir"][i]):
            if i == 0:  # "Seguir intendandolo"
                return "continue2"
            elif i == 1:  # "Salir"
                return "exit"
                
    # Actualiza la pantalla
    pygame.display.update()
    # Limita la tasa de refresco de la pantalla
    clock.tick(60)

#------------------------------------

# Esta función permite detener la música actual, cargar una nueva pista, 
# establecer el volumen y reproducirla en un bucle determinado.
# Entrada:
#   - ruta (str): La ruta del archivo de música.
#   - loop (int): El número de repeticiones de la música (-1 significa que se repetirá infinitamente).
#   - volumen (float): El volumen de la música (de 0.0 a 1.0).
# Salida: Ninguna
def musica(ruta, loop=-1, volumen=0.5):
    pygame.mixer.music.stop()  # Detener la música actual
    pygame.mixer.music.load(ruta)   # Cargar la nueva música
    pygame.mixer.music.set_volume(volumen)    # Establecer el volumen
    pygame.mixer.music.play(loop)  # Reproducir la música en bucle
# --------------------------------------------------------------
# Crear tipos de movimiento para los ataques
ataq_normal = MoveType(name="normal")  # Tipo de ataque normal
ataq_habilidad = MoveType(name="habilidad")  # Tipo de ataque con habilidad especial

# Establecer las relaciones de fortalezas y debilidades entre los tipos de ataques
# Los ataques "normales" no tienen ventaja sobre nada, pero son débiles contra "habilidad".
ataq_normal.fuerte = []  
ataq_normal.debil = [ataq_habilidad]  

# Los ataques "habilidad" son fuertes contra los "normales", pero no tienen debilidades específicas.
ataq_habilidad.fuerte = [ataq_normal]  
ataq_habilidad.debil = []  

# dos tipos de ataques = normal y habilidades
# ataques normales y predeterminados
golpe_terrestre = Move("Golpe Terrestre", 15, ataq_normal)
golpe_mar = Move("Lluvia marina", 5, ataq_normal)
rafaga_piedra = Move("Ráfaga de Piedra", 12, ataq_normal)
golpe_contaminacion = Move("Golpe CO2",8, ataq_normal)
movimientos = [golpe_terrestre,rafaga_piedra, golpe_mar, golpe_contaminacion]

# Se definen las habilidades:
# Crear habilidades como movimientos
ataque_rapido = Move("Ataque Rápido", 20, ataq_habilidad)
defensa_termica = Move("Defensa Térmica", 15, ataq_habilidad)  
tormenta_polvo = Move("Tormenta de Polvo", 30, ataq_habilidad)
gravedad_aumentada = Move("Gravedad Aumentada", 15, ataq_habilidad)
anillos_defensas = Move("Anillos Defensivos", 20, ataq_habilidad)
viento_solar = Move("Viento Solar", 35, ataq_habilidad)
tormenta_neptuno = Move("Tormenta de Neptuno", 40, ataq_habilidad)
#-------------------------------------------------------------------
# Crear objetos
# Personaje principal, tierra
tierra = Tierra(400,500, "tierra.png",vida=100,daño_base=10,level=1,nombre="tierra",Move=movimientos)
# Enemigos
enemys = [
    Enemy(400, 150, "mercurio.png", vida=50, daño_base=8, level=1, nombre="mercurio", Move=[ataque_rapido]),
    
    Enemy(400, 150, "venus.png", vida=70, daño_base=10, level=2, nombre="venus", Move=[defensa_termica]),
    
    Enemy(400, 150, "marte.png", vida=90, daño_base=10, level=3, nombre="marte", Move=[tormenta_polvo]),
    
    Enemy(400, 150, "jupiter.png", vida=95, daño_base=12, level=4, nombre="jupiter", Move=[gravedad_aumentada]),
    
    Enemy(400, 150, "saturno.png", vida=105, daño_base=15, level=5, nombre="saturno", Move=[anillos_defensas]),
    
    Enemy(400, 150, "urano.png", vida=100, daño_base=15, level=6, nombre="urano", Move=[viento_solar]),
    
    Enemy(400, 150, "neptuno.png", vida=95, daño_base=15, level=7, nombre="neptuno", Move=[tormenta_neptuno]),
    
    Enemy(400, 150, "sol.png", vida=115, daño_base=30, level=8, nombre="sol", Move=[tormenta_neptuno]),
]


#determinar los enemigos    
mercurio = enemys[0]
venus = enemys[1]
marte = enemys[2]
jupiter = enemys[3]
saturno = enemys[4]
urano = enemys[5]
neptuno = enemys[6]
sol = enemys[7]
# -----------------------------------------------------------------
#se asignan habilidades
mercurio.agregar_habilidad(ataque_rapido, ataq_habilidad)
venus.agregar_habilidad(defensa_termica, ataq_habilidad)
marte.agregar_habilidad(tormenta_polvo, ataq_habilidad)
jupiter.agregar_habilidad(gravedad_aumentada, ataq_habilidad)
saturno.agregar_habilidad(anillos_defensas, ataq_habilidad)
urano.agregar_habilidad(viento_solar, ataq_habilidad)
neptuno.agregar_habilidad(tormenta_neptuno,ataq_habilidad)
#asignar ataques y habilidades
for enemy, habilidad in zip(enemys, [ataque_rapido, defensa_termica, tormenta_polvo, gravedad_aumentada, anillos_defensas, viento_solar,tormenta_neptuno]):
    #agregar habilidad
    enemy.agregar_habilidad(habilidad, ataq_habilidad) 
    #seleccionar 2 ataques normales
    enemy.Move = random.sample(tierra.Move[:4], 2)  
    enemy.Move.append(habilidad)
#-------------------------------------
# Función principal del juego que controla la lógica de selección de enemigos y batallas.

pygame.mixer.init()

dañosound = pygame.mixer.Sound("Punchis.mp3")
fightsound = pygame.mixer.Sound("Fightsound.mp3")
exitosound = pygame.mixer.Sound("exitosound.mp3")
bg2= pygame.image.load("fightbg.png")

def game_loop():
    global tierra, enemys  # Variables globales que contienen la información del jugador y los enemigos.
    print("Iniciando el juego...")  # Mensaje que indica que el juego está comenzando.
    game_status = 'select rival'  # Estado inicial del juego (jugador debe elegir enemigo)
    selected_enemy = None  # Al principio no hay enemigo seleccionado.
    running = True  # Variable que controla si el bucle principal sigue ejecutándose.
    
    # El bucle principal del juego.
    while running:
        for event in pygame.event.get():  # Detecta los eventos que ocurren en el juego (ejemplo: los clics)
            if event.type == QUIT:  # Si el jugador cierra la ventana del juego.
                running = False  # Detiene el bucle principal y cierra el juego.
            
            # Detecta si se ha hecho clic izquierdo en la pantalla.
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  
                mouse_pos = pygame.mouse.get_pos()  # Obtiene la posición del cursor del mouse.
                
                for enemy in enemigos_disponibles:  # Itera sobre los enemigos disponibles para seleccionar uno.
                    # Si el jugador hace clic en un enemigo y ese enemigo tiene vida.
                    if enemy.rect.collidepoint(mouse_pos) and enemy.vida > 0:
                        fightsound.play()
                        selected_enemy = enemy  # Asigna el enemigo seleccionado.
                        game_status = 'battle'  # Cambia el estado del juego a "battle" para comenzar la batalla.

        # Limpia la pantalla y la rellena con el color negro.
        ventana.fill(black)

        # Si el estado del juego es "select rival", muestra los enemigos que el jugador puede seleccionar.
        if game_status == 'select rival':
            # Filtra los enemigos para mostrar solo aquellos cuyo nivel es menor o igual al nivel de la Tierra.
            enemigos_disponibles = [enemy for enemy in enemys if enemy.level <= tierra.level]
            #indica al jugador que seleccione un enemigo con un nivel menor o igual al de la Tierra.
            dibujar_texto(f"Selecciona un enemigo (Nivel <= {tierra.level})", font3, white, ventana, 80, 30)

            # Dibuja los enemigos en la pantalla, organizados en una cuadrícula.
            for idx, enemy in enumerate(enemys):
                row = idx // 3  # Calcula la fila en la que se debe mostrar el enemigo.
                col = idx % 3   # Calcula la columna en la que se debe mostrar el enemigo.
              
                enemy.x = 95 + col * 150  # Ajusta la posición X para las columnas.
                if row == 0: 
                    enemy.y = 150  # Primera fila.
                elif row == 1:  
                    enemy.y = 300  # Segunda fila.
                else:  
                    enemy.y = 450  # Tercera fila.
                
                enemy.rect.center = (enemy.x, enemy.y)  # Establece el centro del rectángulo del enemigo.
                enemy.dibujar_personaje(ventana)  # Dibuja la imagen del enemigo en la pantalla.
                
                # Muestra el nivel del enemigo debajo de su imagen.
                dibujar_texto(f"Nivel: {enemy.level}", font3, white, ventana, enemy.x-10, enemy.y + 10)
                
        # Si el estado del juego es "battle", comienza la batalla entre la Tierra y el enemigo seleccionado.
        elif game_status == 'battle' and selected_enemy is not None:
            # Cambia la música de fondo según el nivel de la Tierra.
            if tierra.level ==  1:
                musica("batalla1.mp3")  
            elif tierra.level == 2:
                musica("Bring.mp3")
            elif tierra.level == 3:
                musica("batalla3.mp3")
            elif tierra.level == 4:
                musica("Metal_Crusher.mp3")
            elif tierra.level == 5:
                musica("Spider_Dance.mp3")
            elif tierra.level == 6:
                musica("ASGORE.mp3") 
            elif tierra.level == 7:
                musica("batalla2.mp3") 
            else:
                musica("Hopes_And_Dreams.mp3")

            # Configura la posición de los personajes en la pantalla.
            tierra.x = 100  # Ubica a la Tierra en el lado derecho de la pantalla.
            tierra.y = 230  # Centra verticalmente a la Tierra.
            tierra.rect.center = (tierra.x, tierra.y)  # Establece el centro de la Tierra.
            tierra.dibujar_personaje(ventana, scale_factor=2)  # Dibuja la imagen de la Tierra

            # Configura la posición del enemigo en la pantalla.
            selected_enemy.x = 350  # Ubica al enemigo en el lado izquierdo de la pantalla.
            selected_enemy.y = 150  # Centra verticalmente al enemigo.
            selected_enemy.rect.center = (selected_enemy.x, selected_enemy.y)  # Establece el centro del enemigo.
            selected_enemy.dibujar_personaje(ventana, scale_factor=2)  # Dibuja la imagen del enemigo 

            # Dibuja las barras de vida tanto de la Tierra como del enemigo.
            tierra.dibujar_hp(ventana)  # Dibuja la barra de vida de la Tierra.
            selected_enemy.dibujar_hp(ventana)  # Dibuja la barra de vida del enemigo.

            pygame.display.update()  # Actualiza la pantalla para ver los cambios de vida

            # Cambia el estado del juego a "player turn", indicando que es el turno del jugador 
            game_status = "player turn"
#----------------

        #turno del jugador
        elif game_status == "player turn":
            #fondo negro
            ventana.blit(bg2, [0,0])  
            #indicamos con quien estamos luchando
            dibujar_texto(f"Batalla contra {selected_enemy.nombre}", font2, white, ventana,70,30)
            
# Dibuja los personajes en la pantalla (Tierra y el enemigo)
            tierra.dibujar_personaje(ventana,scale_factor=3)
            selected_enemy.dibujar_personaje(ventana, scale_factor=2)
            tierra.dibujar_hp(ventana)
            selected_enemy.dibujar_hp(ventana)
            # losprimeros 4 movimientos de la Tierra
            ataques = tierra.Move[:4]
            
            # configuración para la cuadrícula de botones
            button_width, button_height = 200, 50
            margen_x = 50
            margen_y = ventana_alto - 150 
            spacing_x = 20 # espacio entre botones
            button_positions = [
                (margen_x, margen_y),  # boton fila superior izquierda
                (margen_x + button_width + spacing_x, margen_y),  # boton fila superior derecha
                (margen_x, margen_y + button_height + 10),  # boton fila inferior izquierda
                (margen_x + button_width + spacing_x, margen_y + button_height + 10)  # boton fila inferior derecha
            ]
            # dibuja los botones de ataque 
            for i, (pos_x, pos_y) in enumerate(button_positions):
                #solo se muestra si hay movimiento disponibles
                if i < len(ataques):  
                    ataque = ataques[i]
                    if create_button(ventana, font3, white, grey, button_width, button_height, pos_x, pos_y, black, ataque.name):
                    # Calcula el daño del ataque y lo aplica al enemigo
                        dañosound.play()
                        daño = ataque.calculate_damage(selected_enemy)
                        selected_enemy.recibir_daño(daño)
                        print(f"{tierra.nombre} usa {ataque.name}")
                        # Cambia el estado del juego a "turno del rival" después de que el jugador ataque
                        game_status = "rival turn"

                        # verifica si se derrotó al enemigo
                        if selected_enemy.vida <= 0:
                            musica("menu.mp3")
                            selected_enemy.vida = 0  # se asegura que la vida no sea negativa
                            #se llama a lafuncion de la clase Tierra para subir de nivel
                            tierra.subir_nivel()
                            exitosound.play()
                            game_status = "level up"  # Cambiar a la fase de nivelación}
                            selected_enemy=None 
   # Actualiza la pantalla con los cambios
            pygame.display.update()
            clock.tick(60)  # Controla la velocidad de actualización de la pantalla (60 FPS)
            #---------------------------
        #turno del enemigo
        elif game_status == "rival turn":
            ventana.blit(bg2, [0,0])
            # Dibuja los personajes y barra de vida en la pantalla
            tierra.dibujar_personaje(ventana,scale_factor=3)
            selected_enemy.dibujar_personaje(ventana,scale_factor=2)
            tierra.dibujar_hp(ventana)
            selected_enemy.dibujar_hp(ventana)
            ataque = random.choice(selected_enemy.Move)  # Elegir un ataque aleatorio del enemigo
            dibujar_texto(f"{selected_enemy.nombre} ataca causando {daño} de daño.",font3, white, ventana, 60, 30)
            display_message("El enemigo está atacando...")

            time.sleep(2)  # Pausa de 2 segundos para la animación del ataque del enemigo
            # Selecciona un ataque aleatorio del enemigo

            if isinstance(ataque, Move):  # Si es un ataque normal
                daño = ataque.calculate_damage(tierra) # ataca a la tierra
                tierra.recibir_daño(daño)

            elif isinstance(ataque):  # Si es una habilidad
                ataque.activar(selected_enemy, tierra)
                
                

            #pygame.display.update()
            #si la tierra se queda sin vida, se acaba el juego 
            if tierra.vida <= 0:
                musica("game_over.mp3")
                game_status = "game over"
            #si sigue con vida, es turno del jugador 
            else:
                game_status = "player turn"
            pygame.display.update()
            
        

        #subir nivel
        elif game_status == "level up":
            resultado = mostrar_nivel_subido()
            tierra.vida = tierra.vida_max # Restaura la vida de la Tierra
            # cuando se derrota a un enemigo el enemigo "muere" por lo que no se puede volver a jugar su nivel
            if resultado == "exit":  # Si el jugador elige salir del juego
                #salir del juego 
                running = False 
            #seguir jugando
            elif resultado == "continue":
                tierra.vida = tierra.vida_max
                game_status = "select rival" 
                
        #si el juevo finaliza 
        elif game_status == "game over":
            #llama  a la funcion que dibuja que se terminó el juego
            resultado = mostrar_game_over() 
            tierra.vida = tierra.vida_max 
            enemy.vida = enemy.vida_max
            if resultado == "exit":
                #salir del juego
                running = False  
            #continuar jugando, se reinicia todo
            elif resultado == "continue2":
                tierra.vida = tierra.vida_max  #reinicia la vida
                #resetea el nivel
                game_status = "select rival"
                
        pygame.display.update()
        clock.tick(60)
        
# script, para mostrar el juego
#llamamos a las funciones
def main():
    mostrar_intro()
    menu()
    pygame.quit()
    exit()  # Esto asegura que el juego termine correctamente 

if __name__ == "__main__":
    main()  # Luego pasa al juego principal
pygame.quit()