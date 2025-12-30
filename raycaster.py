import pygame, math
from ray import Ray


# This is the raycaster class where it calculates all the rays coming out of the robot and manages a scoring system

class Raycaster:
    def __init__(self, robot):
        # We set up an empty list that will be in charge of storing all the rays
        self.rays = []
        self.robot = robot

    # To cast the rays, it depends on the walls and the constants RAYS and FOV
    def lanzar_rayos(self, muros, RAYS, FOV, meta):
        # The ray angle will be calculated based on half the FOV
        rayAngle = (self.robot.angulo - (FOV/2))
        self.rays = []
        self.max_distance_ray = 0
        self.max_distance_ray_angle = self.robot.angulo
        
        for _  in range(RAYS):
            ray = Ray(rayAngle, self.robot)
            ray.sensor_distancia(muros)
            self.rays.append(ray)

            rayAngle += FOV / RAYS

    # This function serves to determine which is the best route
    def mejor_ruta(self, muros, RAYS, FOV, meta):
        ancho_ventana = 5
        # Just to see the distance between the robot and the goal
        distancia_robot_meta = self.robot.posicion.distance_to(meta)
        angulo_meta = math.degrees(math.atan2(meta.y - self.robot.posicion.y, meta.x - self.robot.posicion.x))

        # camino_directo = False
        mejor_rayo_meta = None
        menor_diferencia_meta = float('inf')

        # Here we are iterating the list of rays and calculating the difference between the goal angle and the ray angle        
        for ray in self.rays:
            diff = abs(((angulo_meta - ray.rayAngle + 180) % 360) - 180)

            #If we see that the difference is smaller than the goal angle, well, the smallest difference will be the difference, and the best ray will be that ray we are evaluating because what matters is that the difference is very small since that means the angle of that ray points to the goal            
            if diff < menor_diferencia_meta:
                menor_diferencia_meta = diff
                mejor_rayo_meta = ray
        
        # Here we see if the mejor_rayo_meta we established before and the menor_diferencia_meta are smaller than half the FOV, basically having a reasonable angle, and also fulfilling that the detected distance is greater than the distance between the robot and the goal, we simply adjust the angle of the longest ray to be that goal angle because the path is clear        
        if mejor_rayo_meta and menor_diferencia_meta < (FOV / 2):
            if mejor_rayo_meta.distancia_detectada > distancia_robot_meta:
                self.max_distance_ray_angle = angulo_meta
                return 

        # If there is no direct path we have to handle things with a scoring system, starting with an infinitely low score
        mejor_puntuacion = -float('inf')

        # Here we are going to iterate on the length of our list of rays but in batches established by the window width        
        for i in range(len(self.rays) - ancho_ventana):
            ventana = self.rays[i : i + ancho_ventana]
            
            # Here we need an average to avoid robot noise and make it a bit smoother            
            distancia_minima_ventana = min(r.distancia_detectada for r in ventana)
            angulo_ventana = ventana[ancho_ventana // 2].rayAngle
            
            # Angle difference regarding the goal
            diferencia_angulo = ((angulo_ventana - angulo_meta + 180) % 360) - 180

            # Here we establish a rule that says if there is more than 120 px of open space, the effective distance is 120, no more, this way we prevent the robot from loving to go through open paths when the goal is in complicated environments            
            distancia_efectiva = min(distancia_minima_ventana, 120)
            
            # Here a penalty is created for getting close to walls depending on how close the robot is            
            penalizacion_pared = 0
            if distancia_minima_ventana < 30:
                penalizacion_pared = -5000 # Massive penalty
            elif distancia_minima_ventana < 60:
                penalizacion_pared = -1000 # Moderate penalty

            # Here the angle score is more important than distance, so the robot is a bit braver to follow the goal and not avoid so much, that's why it's also multiplied by 10            
            puntuacion_angulo = (180 - abs(diferencia_angulo)) * 10
            
            # The distance score only matters to prevent the robot from crashing, but it shouldn't be more important than the goal angle because otherwise the robot stops going to the goal and prioritizes avoiding walls            
            puntuacion_distancia = distancia_efectiva * 2 

            # Here the score calculation is made according to the conditions established before
            puntuacion = puntuacion_angulo + puntuacion_distancia + penalizacion_pared

            if puntuacion > mejor_puntuacion:
                mejor_puntuacion = puntuacion
                self.max_distance_ray_angle = angulo_ventana

    # This is the function to draw the rays, which are drawn with a small "light" effect
    def dibujar(self, screen):
        for ray in self.rays:
            distancia = ray.distancia_detectada
            inicio = self.robot.posicion
            direccion = pygame.math.Vector2(1, 0).rotate(ray.rayAngle)
            # Here a surface is created for the ray with transparency support
            surf_rayo = pygame.Surface((distancia, 4), pygame.SRCALPHA)
            
            # Here a line with some gradient is drawn
            for i in range(int(distancia)):
                alpha = max(0, 255 - int((i / distancia) * 255))
                pygame.draw.line(surf_rayo, (255, 182, 193, alpha), (i, 2), (i + 1, 2), 2)

            # Here we have to rotate the surface so it matches the rotations the robot makes
            surf_rotada = pygame.transform.rotate(surf_rayo, -ray.rayAngle)
            
            # Here is a Blit with position adjustment so it comes out from the robot
            rect_rotado = surf_rotada.get_rect(center=inicio + (direccion * distancia / 2))
            screen.blit(surf_rotada, rect_rotado)