import pygame
import random
import math

# Inicialización de Pygame
pygame.init()

# Dimensiones de la ventana
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulador de Rastreo con Evasión de Obstáculos")

# Colores
BACKGROUND_COLOR = (230, 240, 255)  # Color de fondo suave (azul claro)
BUTTON_COLOR = (50, 150, 255)  # Color azul más intenso para el botón
BUTTON_HOVER_COLOR = (30, 120, 230)  # Color azul más oscuro para hover
WHITE = (255, 255, 255)
GREEN = (34, 139, 34)  # Verde más oscuro para el carrito
BLACK = (0, 0, 0)
RED = (255, 69, 0)  # Rojo brillante para el material
BLUE = (0, 0, 139)  # Azul marino para el rastro
GRAY = (169, 169, 169)  # Gris claro para los obstáculos
DARK_BLUE = (70, 130, 180) 

# Fuente
font = pygame.font.Font(None, 36)

# Clase Recolector
class Collector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 30
        self.speed = 100  # Velocidad de movimiento en píxeles por segundo
        self.score = 0
        self.materials_collected = 0  # Contador de materiales recogidos
        self.path = []  # Rastro del camino tomado

    def update(self, dt, materials, obstacles):
        if materials:
            # Obtener el material más cercano
            target = min(materials, key=lambda m: self.distance_to(m))
            # Moverse hacia el objetivo evitando obstáculos
            self.move_towards_with_evasion(target, dt, obstacles)

        # Limitar movimiento dentro de la ventana
        self.x = max(0, min(self.x, WIDTH - self.size))
        self.y = max(0, min(self.y, HEIGHT - self.size))

        # Agregar posición actual al rastro
        self.path.append((self.x, self.y))

    def move_towards_with_evasion(self, target, dt, obstacles):
        dx, dy = target.x - self.x, target.y - self.y
        distance = math.hypot(dx, dy)
        if distance != 0:
            dx, dy = dx / distance, dy / distance  # Normalizar dirección
            new_x = self.x + dx * self.speed * dt
            new_y = self.y + dy * self.speed * dt

            # Comprobar si la nueva posición colisiona con un obstáculo
            if not self.collides_with_obstacles(new_x, new_y, obstacles):
                self.x, self.y = new_x, new_y
            else:
                # Intentar evadir el obstáculo (movimiento vertical u horizontal)
                if not self.collides_with_obstacles(self.x, self.y + dy * self.speed * dt, obstacles):
                    self.y += dy * self.speed * dt  # Mover solo en el eje Y
                elif not self.collides_with_obstacles(self.x + dx * self.speed * dt, self.y, obstacles):
                    self.x += dx * self.speed * dt  # Mover solo en el eje X

    def distance_to(self, material):
        return math.hypot(self.x - material.x, self.y - material.y)

    def collides_with_obstacles(self, new_x, new_y, obstacles):
        for obstacle in obstacles:
            if (new_x < obstacle.x + obstacle.size and
                new_x + self.size > obstacle.x and
                new_y < obstacle.y + obstacle.size and
                new_y + self.size > obstacle.y):
                return True
        return False

    def draw(self, screen):
        # Carrito
        car_length = 40
        car_height = 20
        front = pygame.Rect(self.x - car_length / 2, self.y - car_height / 2, car_length, car_height)
        back = pygame.Rect(self.x - car_length / 2 + 10, self.y - car_height / 2 + 5, car_length - 20, car_height - 10)
        pygame.draw.rect(screen, GREEN, front)  # Cuerpo del carrito
        pygame.draw.rect(screen, BLACK, back)    # Parte trasera del carrito
        pygame.draw.circle(screen, BLACK, (int(self.x - car_length / 2 + 10), int(self.y + car_height / 2)), 5)  # Rueda izquierda
        pygame.draw.circle(screen, BLACK, (int(self.x + car_length / 2 - 10), int(self.y + car_height / 2)), 5) # Rueda derecha

        # Dibujar el rastro
        if len(self.path) > 1:
            pygame.draw.lines(screen, BLUE, False, self.path, 3)

# Clase Material
class Material:
    def __init__(self):
        self.x = random.randint(0, WIDTH - 20)
        self.y = random.randint(0, HEIGHT - 20)
        self.size = 20

    def draw(self, screen):
        pygame.draw.circle(screen, RED, (self.x, self.y), self.size)  # Material

# Clase Obstáculo
class Obstacle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 40

    def draw(self, screen):
        pygame.draw.rect(screen, GRAY, (self.x, self.y, self.size, self.size))  # Obstáculo

# Función principal
def main():
    collector = Collector(WIDTH // 2, HEIGHT // 2)
    materials = [Material() for _ in range(5)]  # Crear 5 materiales
    obstacles = []  # Lista de obstáculos
    drop_location = (WIDTH - 100, HEIGHT - 100)  # Ubicación donde dejar materiales
    generate_button = pygame.Rect(10, 80, 150, 40)  # Botón para generar más materiales
    running = True
    clock = pygame.time.Clock()
    placing_obstacles = False  # Controlar si estamos colocando obstáculos
    show_instructions = True  # Controlar si mostrar instrucciones

    while running:
        dt = clock.tick(60) / 1000  # Tiempo desde el último frame
        screen.fill(BACKGROUND_COLOR)
        
        # Boton Volver
        back_button = pygame.Rect(WIDTH - 170, 20, 150, 40)
        pygame.draw.rect(screen, DARK_BLUE, back_button, border_radius=10)  # Botón 'Volver'
        back_text = font.render("Volver", True, WHITE)  # Texto en blanco
        text_rect = back_text.get_rect(center=back_button.center)
        screen.blit(back_text, text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Si se presiona el botón izquierdo del mouse
                    if generate_button.collidepoint(event.pos):  # Si se hace clic en el botón
                        if len(materials) < 10:  # Limitar a un máximo de 10 materiales en pantalla
                            materials.append(Material())  # Generar un nuevo material
                            show_instructions = False  # Ocultar instrucciones al usar la función
                    if back_button.collidepoint(event.pos):
                        return
                    elif placing_obstacles:  # Si estamos en modo de colocar obstáculos
                        x, y = event.pos
                        obstacles.append(Obstacle(x - 20, y - 20))  # Agregar un obstáculo
                        show_instructions = False  # Ocultar instrucciones al usar la función

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_o:  # Al presionar "O", activar modo de colocar obstáculos
                    placing_obstacles = not placing_obstacles
                    show_instructions = False  # Ocultar instrucciones al usar la función

        # Actualizar posición del recolector
        collector.update(dt, materials, obstacles)

        # Verificar colisiones con materiales
        for material in materials[:]:
            if (collector.x < material.x + material.size and
                collector.x + collector.size > material.x and
                collector.y < material.y + material.size and
                collector.y + collector.size > material.y):
                if collector.materials_collected < 5:  # Limitar a 5 materiales recogidos
                    collector.materials_collected += 1  # Incrementar contador de materiales recogidos
                    materials.remove(material)  # Eliminar material recogido

        # Comprobar si el recolector deja materiales en la ubicación designada
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:  # Usar la barra espaciadora para dejar materiales
            if collector.materials_collected > 0:  # Solo dejar si hay materiales recogidos
                collector.score += 1  # Incrementar puntuación al dejar materiales
                collector.materials_collected -= 1  # Disminuir contador de materiales recogidos

        # Dibujar ubicación de dejar materiales
        pygame.draw.rect(screen, BLUE, (drop_location[0], drop_location[1], 20, 20))  # Ubicación para dejar materiales

        # Dibujar el botón de generar más materiales
        if generate_button.collidepoint(pygame.mouse.get_pos()):
            button_color = BUTTON_HOVER_COLOR
        else:
            button_color = BUTTON_COLOR

        pygame.draw.rect(screen, button_color, generate_button)  # Botón
        button_text = font.render("+Materiales", True, WHITE)
        screen.blit(button_text, (generate_button.x + 10, generate_button.y + 5))  # Texto del botón

        collector.draw(screen)  # Dibujar recolector

        # Dibujar materiales
        for material in materials:
            material.draw(screen)

        # Dibujar obstáculos
        for obstacle in obstacles:
            obstacle.draw(screen)

        # Mostrar puntuación y materiales recogidos
        score_text = font.render(f"Puntuación: {collector.score}", True, BLACK)
        materials_text = font.render(f"Materiales Recogidos: {collector.materials_collected}", True, BLACK)
        screen.blit(score_text, (10, 10))
        screen.blit(materials_text, (10, 40))

        # Mostrar instrucciones
        if show_instructions:
            instructions_text = font.render("Presiona 'O' para entrar en modo colocar obstáculos", True, BLACK)
            instructions_text2 = font.render("y Clic Izquierdo para colocar.", True, BLACK)
            screen.blit(instructions_text, (50, 500))
            screen.blit(instructions_text2, (70, 530))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
