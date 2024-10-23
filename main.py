import pygame
from menu import MainMenu

# Inicialización de Pygame
pygame.init()  # Inicializa todos los módulos de Pygame

# Dimensiones de la ventana
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Menú Principal")

# Función principal
def main():
    menu = MainMenu(screen)  # Pasar la pantalla al menú
    menu.run()
    pygame.quit()

if __name__ == "__main__":
    main()
