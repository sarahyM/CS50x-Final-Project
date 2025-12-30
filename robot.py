import pygame

# This is the robot class which requires an initial position to spawn
class Robot:
    def __init__(self, posicion_x, posicion_y):
        # Here its position is the vector calculated with position x and y
        self.posicion = pygame.math.Vector2(posicion_x, posicion_y)
        # Here the robot image is loaded
        self.original_robot = pygame.image.load('assets/robot.png').convert_alpha()
        self.robot = pygame.transform.scale(self.original_robot, (25, 25))
        # Start variables are established
        self.angulo = 0
        self.velocidad = 2
        self.rect = pygame.Rect(0, 0, 18, 18)
        self.cont_choques = 0
        
    # This function is in charge of rendering the robot on screen respecting its rotation regarding its center point
    def dibujar(self, superficie, distancia):
        robot_rotado = pygame.transform.rotate(self.robot, -self.angulo)
        rectangulo = robot_rotado.get_rect(center=(self.posicion.x, self.posicion.y))
        superficie.blit(robot_rotado, rectangulo)

        vector_rotado = pygame.math.Vector2(distancia, 0).rotate(self.angulo)


    # This is the function so the robot moves continually depending on its angle which will update its position and move one by one
    def moverse(self):
        direccion = pygame.math.Vector2(1, 0)
        direccion_rotada = direccion.rotate(self.angulo)
        desplazamiento = direccion_rotada * self.velocidad
        self.posicion += desplazamiento


    # This function is to update the robot rect based on its position in x and y
    def actualizarse(self):
        self.rect.center = (self.posicion.x, self.posicion.y)
        
    # This function detects if the robot is crashing into a wall
    def esta_chocando(self, muros):
        for muro in muros:
            if self.rect.colliderect(muro):
                return True
        return False

