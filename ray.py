import math, pygame

# This function serves to normalize the angle
def normalizeAngle(angle):
     return angle % 360

# The ray class is defined
class Ray:
    def __init__(self, angulo, robot):
        # The ray needs an angle, needs to know the robot entity, and the distance they detect
        self.rayAngle = normalizeAngle(angulo)
        self.robot = robot
        self.distancia_detectada = 0

    # This is the distance sensor that needs to know the distance between the robot and the wall
    def sensor_distancia(self, muros):
        # Here a direction is established which rotates based on the robot angle
        direccion = pygame.math.Vector2(1, 0).rotate(self.rayAngle)
       
        for d in range (15, 800, 5):
            # Here we handle the ray going from range 15 to 800 and test points since the robot position will change continually as the new direction multiplied by d is added
            punto_prueba = self.robot.posicion + (direccion * d)

            for muro in muros:
                if muro.collidepoint(punto_prueba):
                    # Here if we collide the detected distance will be d
                    self.distancia_detectada = d
                    return d
        self.distancia_detectada = 800
        return 800
