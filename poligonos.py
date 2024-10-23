import pygame
import math

# Inicialización de Pygame
pygame.init()

# Dimensiones de la ventana
WIDTH, HEIGHT = 800, 600
MARGIN = 20  # Margen para los botones
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulación de Carrito en Polígonos")

# Colores mejorados
BACKGROUND_COLOR = (240, 248, 255)  # Azul claro (AliceBlue)
BUTTON_COLOR = (70, 130, 180)  # Azul acero (SteelBlue)
BUTTON_HOVER_COLOR = (100, 149, 237)  # Azul claro (CornflowerBlue)
TEXT_COLOR = (255, 255, 255)  # Blanco para el texto
DARK_TEXT_COLOR = (30, 30, 30)  # Gris oscuro para el texto
WHEEL_COLOR = (169, 169, 169)  # Color para las ruedas

font = pygame.font.Font(None, 36)

class Car:
    def __init__(self, x, y, size, color, initial_position=0):
        self.x = x
        self.y = y
        self.size = size
        self.color = color  
        self.position = initial_position  # Posición inicial en el recorrido

    def update(self, vertices, speed):
        if vertices:
            self.position += speed
            self.position %= len(vertices)
            
            index = int(self.position)
            next_index = (index + 1) % len(vertices)
            current_vertex = vertices[index]
            next_vertex = vertices[next_index]
            
            t = self.position - index
            self.x = (1 - t) * current_vertex[0] + t * next_vertex[0]
            self.y = (1 - t) * current_vertex[1] + t * next_vertex[1]

    def draw(self, screen):
        car_rect = pygame.Rect(self.x - self.size // 2, self.y - self.size // 2, self.size, self.size // 2)
        pygame.draw.rect(screen, self.color, car_rect, border_radius=5)

        cabin_rect = pygame.Rect(self.x - self.size // 4, self.y - self.size // 2.5, self.size // 2, self.size // 4)
        pygame.draw.rect(screen, TEXT_COLOR, cabin_rect, border_radius=3)

        wheel_radius = self.size // 6
        wheel_offset_x = self.size // 3
        wheel_offset_y = self.size // 4
        pygame.draw.circle(screen, WHEEL_COLOR, (int(self.x - wheel_offset_x), int(self.y + wheel_offset_y)), wheel_radius)
        pygame.draw.circle(screen, WHEEL_COLOR, (int(self.x + wheel_offset_x), int(self.y + wheel_offset_y)), wheel_radius)

class PolygonsSimulation:
    def __init__(self):
        self.cars = []  # Lista de carritos
        self.num_cars = 1  # Número inicial de carritos
        self.vertices = []

    def update_cars(self):
        # Actualizar la cantidad de carritos según el número ingresado y distribuirlos a lo largo del polígono
        if self.vertices:
            # Distribuir las posiciones iniciales de los carritos en el polígono
            positions = [i * len(self.vertices) / self.num_cars for i in range(self.num_cars)]
            self.cars = [Car(WIDTH // 2, HEIGHT // 2, size=40, color=(0, 204, 102), initial_position=pos) for pos in positions]  # Color verde
        else:
            # Si no hay vértices, crear carritos con posición inicial 0
            self.cars = [Car(WIDTH // 2, HEIGHT // 2, size=40, color=(0, 204, 102)) for _ in range(self.num_cars)]

    def run(self):
        clock = pygame.time.Clock()
        input_box = pygame.Rect(WIDTH - 250, 20, 100, 40)  # Caja de entrada para el número de carritos
        active = False  # Para saber si la caja de texto está activa
        user_text = str(self.num_cars)  # Texto ingresado por el usuario
        previous_text = user_text  # Para detectar cambios en el número de carritos
        running = True

        while running:
            screen.fill(BACKGROUND_COLOR)

            # Mostrar botón de volver
            back_button = pygame.Rect(20, 20, 150, 40)
            pygame.draw.rect(screen, BUTTON_COLOR, back_button, border_radius=10)
            back_text = font.render("Volver", True, TEXT_COLOR)
            text_rect = back_text.get_rect(center=back_button.center)
            screen.blit(back_text, text_rect)

            # Texto que indica el número de carritos
            label = font.render("N° carritos:", True, DARK_TEXT_COLOR)
            screen.blit(label, (WIDTH - 380, 30))

            # Caja de entrada para el número de carritos
            pygame.draw.rect(screen, DARK_TEXT_COLOR if active else BUTTON_COLOR, input_box, 2)
            text_surface = font.render(user_text, True, DARK_TEXT_COLOR)
            screen.blit(text_surface, (input_box.x + 5, input_box.y + 5))
            input_box.w = max(100, text_surface.get_width() + 10)

            # Verificar si ha cambiado el texto para actualizar el número de carritos
            if user_text != previous_text and user_text.isdigit():
                self.num_cars = int(user_text)
                self.update_cars()  # Actualizar los carritos al cambiar el número
                previous_text = user_text  # Actualizar el valor previo

            # Actualizar y dibujar los carritos
            if self.vertices:
                speed = 0.05 if len(self.vertices) < 100 else 0.1
                for car in self.cars:
                    car.update(self.vertices, speed)
                    car.draw(screen)
                pygame.draw.polygon(screen, DARK_TEXT_COLOR, self.vertices, 2)

            # Manejar eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if input_box.collidepoint(event.pos):
                        active = True
                    else:
                        active = False
                    if back_button.collidepoint(event.pos):
                        running = False  # Volver al menú
                if event.type == pygame.KEYDOWN:
                    if active:
                        if event.key == pygame.K_BACKSPACE:
                            user_text = user_text[:-1]
                        else:
                            user_text += event.unicode

            # Botones para seleccionar polígonos
            polygon_buttons = [
                ("Triángulo", 3),
                ("Cuadrado", 4),
                ("Círculo", 100),
                ("Pentágono", 5)
            ]

            button_width = 150
            button_height = 50
            total_buttons_width = button_width * len(polygon_buttons) + MARGIN * (len(polygon_buttons) - 1)
            start_x = (WIDTH - total_buttons_width) // 2

            for i, (text, sides) in enumerate(polygon_buttons):
                rect = pygame.Rect(start_x + i * (button_width + MARGIN), HEIGHT - button_height - MARGIN, button_width, button_height)
                pygame.draw.rect(screen, BUTTON_COLOR, rect, border_radius=10)
                button_text = font.render(text, True, TEXT_COLOR)
                text_rect = button_text.get_rect(center=rect.center)
                screen.blit(button_text, text_rect)
                
                # Cambiar color al pasar el mouse
                if rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(screen, BUTTON_HOVER_COLOR, rect, border_radius=10)
                    screen.blit(button_text, text_rect)  # Volver a dibujar el texto encima
                    
                    if pygame.mouse.get_pressed()[0]:  # Al hacer clic
                        # Al seleccionar un polígono, solo se actualizan los vértices y los carritos, pero se conserva el número de carritos actual
                        self.vertices = self.create_polygon_vertices(sides, radius=150, center=(WIDTH // 2, HEIGHT // 2))
                        self.update_cars()  # Actualizar carritos cuando se cambie el polígono

            pygame.display.flip()
            clock.tick(60)

    def create_polygon_vertices(self, sides, radius, center):
        angle = 2 * math.pi / sides
        return [(center[0] + radius * math.cos(i * angle - math.pi / 2), center[1] + radius * math.sin(i * angle - math.pi / 2)) for i in range(sides)]

# Ejecución de la simulación
if __name__ == "__main__":
    simulation = PolygonsSimulation()
    simulation.update_cars()  # Inicializar carritos
    simulation.run()
    pygame.quit()
