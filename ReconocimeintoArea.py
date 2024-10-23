import pygame
import math
import random

# Colores
WHITE = (240, 248, 255)  # Azul claro para el fondo
LIGHT_BLUE = (173, 216, 230)  # Azul claro para el botón
DARK_BLUE = (0, 0, 139)  # Azul oscuro para el texto
GREEN = (34, 139, 34)  # Verde para el carrito
BLACK = (0, 0, 0)
RED = (255, 69, 0)  # Naranja brillante para los obstáculos
BLUE = (30, 144, 255)  # Azul para la huella que deja el carrito

# Inicialización de Pygame
pygame.init()

# Dimensiones de la ventana
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulador de Movimiento Automático")

# Fuente
font = pygame.font.Font(None, 36)

# Clase Móvil
class Mobile:
    def __init__(self, x, y, length, mass):
        self.x = x
        self.y = y
        self.length = length
        self.angle = random.uniform(0, 2 * math.pi)  # Ángulo inicial aleatorio
        self.radius = 1
        self.trail = [(x, y)]  # Inicializar la huella con la posición de inicio

    def update(self, obstacles):
        # Movimiento
        speed = 2  # Velocidad del carrito
        new_x = self.x + speed * math.cos(self.angle)
        new_y = self.y + speed * math.sin(self.angle)

        # Verificar colisión con obstáculos
        for obs in obstacles:
            if obs.collidepoint(new_x, new_y):
                # Si hay una colisión, cambiar la dirección aleatoriamente
                self.angle += random.uniform(math.pi / 4, math.pi / 2)
                return  # No mover hasta que se resuelva la colisión

        # Verificar colisión con los bordes de la pantalla y rebotar
        if new_x <= 0 or new_x >= WIDTH:
            self.angle = math.pi - self.angle  # Rebote horizontal
        if new_y <= 0 or new_y >= HEIGHT:
            self.angle = -self.angle  # Rebote vertical

        # Actualizar la posición si no hubo colisión con los bordes
        self.x = max(0, min(WIDTH, new_x))
        self.y = max(0, min(HEIGHT, new_y))

        # Añadir la nueva posición a la huella
        self.trail.append((self.x, self.y))

    def draw(self, screen):
        # Pintar la huella que deja el carrito
        if len(self.trail) > 1:
            pygame.draw.lines(screen, BLUE, False, self.trail, 3)  # Dibujar la línea por donde pasó

        # Carrito
        car_length = 40
        car_height = 20
        front = pygame.Rect(self.x - car_length / 2, self.y - car_height / 2, car_length, car_height)
        back = pygame.Rect(self.x - car_length / 2 + 10, self.y - car_height / 2 + 5, car_length - 20, car_height - 10)
        pygame.draw.rect(screen, GREEN, front)  # Carrito principal
        pygame.draw.rect(screen, BLACK, back)   # Parte trasera
        pygame.draw.circle(screen, BLACK, (int(self.x - car_length / 2 + 10), int(self.y + car_height / 2)), 5)  # Rueda izquierda
        pygame.draw.circle(screen, BLACK, (int(self.x + car_length / 2 - 10), int(self.y + car_height / 2)), 5)  # Rueda derecha

# Función para crear obstáculos aleatorios
def create_obstacles(num_obstacles, width, height):
    obstacles = []
    for _ in range(num_obstacles):
        obs_width = random.randint(20, 80)
        obs_height = random.randint(20, 80)
        x = random.randint(0, width - obs_width)
        y = random.randint(0, height - obs_height)
        obstacles.append(pygame.Rect(x, y, obs_width, obs_height))
    return obstacles

# Función principal
def main():
    input_active = True
    user_text = ''
    cars = []
    obstacles = []

    clock = pygame.time.Clock()

    while input_active:
        screen.fill(WHITE)
        text_surface = font.render(f"Ingrese la cantidad de carritos: {user_text}", True, DARK_BLUE)
        screen.blit(text_surface, (50, 50))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                input_active = False
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if user_text.isdigit():
                        n_carritos = int(user_text)
                        cars = [Mobile(random.randint(0, WIDTH), random.randint(0, HEIGHT), length=60, mass=10.0) for _ in range(n_carritos)]
                        obstacles = create_obstacles(10, WIDTH, HEIGHT)  # Crear obstáculos
                        input_active = False  # Salir de la pantalla de ingreso
                    user_text = ''
                elif event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                else:
                    user_text += event.unicode

        pygame.display.flip()
        clock.tick(60)

    # Comenzar simulación con los carritos
    running = True
    while running:
        dt = clock.tick(60) / 1000
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(event.pos):
                    return

        # Actualizar y dibujar todos los carritos
        for car in cars:
            car.update(obstacles)
            car.draw(screen)

        # Dibujar obstáculos
        for obs in obstacles:
            pygame.draw.rect(screen, RED, obs)
        
        back_button = pygame.Rect(20, 20, 150, 40)
        pygame.draw.rect(screen, LIGHT_BLUE, back_button, border_radius=10)
        back_text = font.render("Volver", True, DARK_BLUE)
        text_rect = back_text.get_rect(center=back_button.center)
        screen.blit(back_text, text_rect)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
