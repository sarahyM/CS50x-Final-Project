import pygame

# This is the class that handles the interface the user interacts with
class Interfaz:
    # The interface needs the map where it will be drawn, as well as the window width and height
    def __init__(self, mapa_estatico, ancho_ventana, alto_ventana):
        self.mapa_estatico = mapa_estatico

        # This is the font we will work with as well as its size
        self.font = pygame.freetype.Font('assets/Handjet-Bold.ttf', 24)
        self.ancho_ventana = ancho_ventana
        self.alto_ventana = alto_ventana

        # These are the variables for the buttons
        ancho_b, alto_b, espaciado = 100, 40, 20
        inicio_x = (self.ancho_ventana - 460) // 2
        y_pos = self.alto_ventana - 60

        # This is the interface background
        self.background = pygame.image.load('assets/background_i.png').convert_alpha()

        # Here the buttons and their position are established
        self.btn_iniciar = pygame.Rect(inicio_x, y_pos, ancho_b, alto_b)
        self.btn_reiniciar = pygame.Rect(inicio_x + 120, y_pos, ancho_b, alto_b)
        self.btn_mapa1 = pygame.Rect(inicio_x + 240, y_pos, ancho_b, alto_b)
        self.btn_mapa2 = pygame.Rect(inicio_x + 360, y_pos, ancho_b, alto_b)
    def botones(self, superficie):        
        # We create an iterable list with all the buttons
        botones = [
            (self.btn_iniciar, "Iniciar"),
            (self.btn_reiniciar, "Reiniciar"),
            (self.btn_mapa1, "Mapa 1"),
            (self.btn_mapa2, "Mapa 2"),
        ]

        # We draw the background on the surface
        superficie.blit(self.background, (0, 385))
        for boton, texto in botones:
            # Here we iterate on the buttons list to place both the button and the corresponding text
            pygame.draw.rect(superficie, (92, 103, 144), boton, border_radius=8)
            pygame.draw.rect(superficie, (247, 242, 221), boton, width = 4, border_radius=8)

            text_surface, text_rect = self.font.render(texto, (247, 242, 221))
            text_rect.center = boton.center
            superficie.blit(text_surface, text_rect)

    # This is the message shown when the goal is reached which covers the whole screen
    def meta_alcanzada(self, screen):
        mensaje = "¡Meta alcanzada!"
        pygame.draw.rect(screen, (92, 103, 144), (0, 0, self.ancho_ventana, self.alto_ventana), border_radius=8)
        text_surface, text_rect = self.font.render(mensaje, (247, 242, 221))
        text_rect.center = (self.ancho_ventana // 2, self.alto_ventana // 2)
        screen.blit(text_surface, text_rect)