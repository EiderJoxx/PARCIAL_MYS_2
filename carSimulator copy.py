import pygame 
import math

# Inicialización de Pygame
pygame.init()

# Dimensiones de la ventana
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulador de Móvil con Frenado Gradual")

# Colores
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (173, 216, 230)
DARK_BLUE = (0, 0, 139)

# Fuente
font = pygame.font.Font(None, 36)

# Clase Móvil
class Mobile:
    def __init__(self, x, y, length, mass):
        self.x = x
        self.y = y
        self.angle = 0
        self.length = length
        self.vl = 0  # Velocidad motor izquierdo
        self.vr = 0  # Velocidad motor derecho
        self.mass = mass  # Masa del móvil
        self.mu = 0.15  # Coeficiente de fricción
        self.is_braking = False  # Control de frenado

    def apply_brake(self, dt):
        deceleration = self.mu * 9.81  # Deceleración debido a la fricción

        # Aplicar desaceleración a las velocidades vl y vr directamente
        if self.vl > 0:
            self.vl -= deceleration * dt
            if self.vl < 0:  # Evitar que la velocidad se vuelva negativa
                self.vl = 0
        elif self.vl < 0:
            self.vl += deceleration * dt
            if self.vl > 0:  # Evitar que la velocidad se vuelva positiva
                self.vl = 0

        if self.vr > 0:
            self.vr -= deceleration * dt
            if self.vr < 0:
                self.vr = 0
        elif self.vr < 0:
            self.vr += deceleration * dt
            if self.vr > 0:
                self.vr = 0

    def update(self, dt):
        if self.is_braking:
            self.apply_brake(dt)

        speed = (self.vl + self.vr) / 2

        if self.vl != self.vr:
            self.angle += (self.vr - self.vl) / self.length

        dx = speed * math.cos(self.angle) * dt * 100
        dy = speed * math.sin(self.angle) * dt * 100

        self.x += dx
        self.y += dy

        self.x = max(0, min(self.x, WIDTH))
        self.y = max(0, min(self.y, HEIGHT))

    def draw(self, screen):
        # Carrito
        car_length = 40
        car_height = 20
        front = pygame.Rect(self.x - car_length / 2, self.y - car_height / 2, car_length, car_height)
        back = pygame.Rect(self.x - car_length / 2 + 10, self.y - car_height / 2 + 5, car_length - 20, car_height - 10)
        pygame.draw.rect(screen, GREEN, front)  # Cuerpo del carrito
        pygame.draw.rect(screen, BLACK, back)    # Parte trasera del carrito
        pygame.draw.circle(screen, BLACK, (int(self.x - car_length / 2 + 10), int(self.y + car_height / 2)), 5)  # Rueda izquierda
        pygame.draw.circle(screen, BLACK, (int(self.x + car_length / 2 - 10), int(self.y + car_height / 2)), 5)  # Rueda derecha

# Función principal
def main():
    car = Mobile(WIDTH // 2, HEIGHT // 2, length=60, mass=10.0)

    running = True
    clock = pygame.time.Clock()

    input_box_left = pygame.Rect(WIDTH // 2 - 200, HEIGHT - 150, 140, 32)
    input_box_right = pygame.Rect(WIDTH // 2 + 20, HEIGHT - 150, 140, 32)

    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')

    active_left = False
    active_right = False
    text_left = '0'
    text_right = '0'

    brake_button = pygame.Rect(WIDTH // 2 - 70, HEIGHT - 100, 140, 40)

    while running:
        dt = clock.tick(60) / 1000
        screen.fill(WHITE)

        pygame.draw.rect(screen, BLUE, (0, 0, WIDTH, HEIGHT))

        title_text = font.render("Movimiento en 2D", True, WHITE)
        screen.blit(title_text, (10, 10))

        back_button = pygame.Rect(WIDTH - 170, 20, 150, 40)
        pygame.draw.rect(screen, LIGHT_BLUE, back_button, border_radius=10)
        back_text = font.render("Volver", True, DARK_BLUE)
        text_rect = back_text.get_rect(center=back_button.center)
        screen.blit(back_text, text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box_left.collidepoint(event.pos):
                    active_left = True
                    active_right = False
                elif input_box_right.collidepoint(event.pos):
                    active_right = True
                    active_left = False
                elif brake_button.collidepoint(event.pos):
                    car.is_braking = True  # Activar frenado cuando se presiona el botón
                elif back_button.collidepoint(event.pos):
                    return  # Regresar al menú principal
                else:
                    active_left = False
                    active_right = False

            if event.type == pygame.KEYDOWN:
                if active_left:
                    if event.key == pygame.K_RETURN:
                        active_left = False
                    elif event.key == pygame.K_BACKSPACE:
                        text_left = text_left[:-1]
                    else:
                        text_left += event.unicode
                elif active_right:
                    if event.key == pygame.K_RETURN:
                        active_right = False
                    elif event.key == pygame.K_BACKSPACE:
                        text_right = text_right[:-1]
                    else:
                        text_right += event.unicode

                car.is_braking = False

        if not car.is_braking:
            try:
                car.vl = float(text_left)
                car.vr = float(text_right)
            except ValueError:
                pass

        car.update(dt)
        car.draw(screen)

        txt_surface_left = font.render(text_left, True, BLACK)
        txt_surface_right = font.render(text_right, True, BLACK)
        screen.blit(txt_surface_left, (input_box_left.x + 5, input_box_left.y + 5))
        screen.blit(txt_surface_right, (input_box_right.x + 5, input_box_right.y + 5))

        pygame.draw.rect(screen, color_active if active_left else color_inactive, input_box_left, 2)
        pygame.draw.rect(screen, color_active if active_right else color_inactive, input_box_right, 2)

        pygame.draw.rect(screen, RED, brake_button)
        brake_text = font.render("Frenar", True, WHITE)
        screen.blit(brake_text, (brake_button.x + 20, brake_button.y + 10))

        instruction_left = font.render("V. Izquierdo:", True, BLACK)
        instruction_right = font.render("V. Derecho:", True, BLACK)
        screen.blit(instruction_left, (WIDTH // 2 - 200, HEIGHT - 200))
        screen.blit(instruction_right, (WIDTH // 2 + 20, HEIGHT - 200))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
