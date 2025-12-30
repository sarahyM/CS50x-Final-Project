# Here I import the necessary libraries
import pygame, random

# Here I import the classes and necessary configuration
from gestor_mapa import GestorMapa
from robot import Robot
from raycaster import Raycaster
from interfaz import Interfaz
from settings import *

# The simulation class is established so that the main file is cleaner without including low-level logic
class Simulacion:
    def __init__(self):
        # The class starts by initializing pygame, since without it we can't do anything, its height and width parameters and program title are set
        pygame.init()
        self.screen = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
        pygame.display.set_caption("Final Project CS50")

        # The clock for frame updates
        self.clock = pygame.time.Clock()

        # The simulation must load the map before doing anything else, for that we call the map manager which is the class in charge of reading the map txt and rendering them
        self.gestor = GestorMapa(TILE_SIZE)
        # A map_txt is made to store the reading from the cargar_mapa method
        self.mapa_txt = self.gestor.cargar_mapa('map.txt')
        # In static map and in walls, the position of the walls is determined, managed from mapa_txt
        self.mapa_estatico, self.muros = self.gestor.muros(self.mapa_txt)

        # The robot object is created with the initial coordinates established in settings.py
        self.robot = Robot(COORDENADAS_INICIALES_ROBOT[0], COORDENADAS_INICIALES_ROBOT[1])
        # The raycaster object is created, which is in charge of handling the rays coming out of the robot
        self.raycaster = Raycaster(self.robot)
        # Interface is called to load the UI the user interacts with
        self.interfaz = Interfaz(self.mapa_estatico,ANCHO_VENTANA, ALTO_VENTANA)

        # Here necessary start variables for the functions are established
        self.meta = pygame.math.Vector2(400, 200)
        self.estado_juego = "menu"
        self.paused = False
        self.mostrar_meta = False
        self.distancia = 0
        self.meta_time = 0

    # This function allows the robot to move continually as long as the program isn't paused
    def actualizar_movimiento(self):
        # We need to store a safe position where the robot hasn't crashed
        pos_segura = self.robot.posicion.copy()

        if not self.paused:
            # Here the method is called first to cast rays (lanzar_rayos) and second for the robot to find the best route (mejor_ruta)
            self.raycaster.lanzar_rayos(self.muros, RAYS, FOV, self.meta)
            self.raycaster.mejor_ruta(self.muros, RAYS, FOV, self.meta)
            # Here angles are established so the robot heads to the angle belonging to the longest ray
            angulo_ideal = self.raycaster.max_distance_ray_angle
            angulo_actual = self.robot.angulo % 360
            diferencia_angulo = ((angulo_ideal - angulo_actual + 180) % 360) - 180
            # The speed at which the robot turns is established
            velocidad_giro = 5

            if abs(diferencia_angulo) > velocidad_giro:
                self.robot.angulo += velocidad_giro * (1 if diferencia_angulo > 0 else -1)
            else:
                self.robot.angulo = angulo_ideal

            if self.raycaster.rays:
                centro = len(self.raycaster.rays) // 2
                self.distancia = self.raycaster.rays[centro].distancia_detectada
            else:
                self.distancia = 0

        # Here the distance to the goal is established as the distance from the robot's position to the goal
        distancia_meta = self.robot.posicion.distance_to(self.meta)

        # Here collisions are handled a bit, if the game state is in start, and the robot distance to goal is greater than the goal radius and game is not paused, the robot moves, updates its position
        if self.estado_juego == "iniciar" and distancia_meta > RADIO_META and not self.paused:
            self.robot.moverse()
            self.robot.actualizarse()
            # Here the robot has to check if in that new position it is crashing against a wall or not, if the robot is crashing the robot position returns to the previous safe position    
            if self.robot.esta_chocando(self.muros):
                self.robot.posicion = pos_segura
                # An escape angle must be established, relatively random to avoid falling into infinite loops if the same angle value is calculated, it must be a random number not excessively large so as not to lose control too much and its direction must also change if it goes left or right
                angulo_escape = random.randint(25, 50)
                direccion_giro = random.choice([-1, 1])
                self.robot.angulo += angulo_escape * direccion_giro
                # With those escape values the robot is updated
                self.robot.actualizarse()

        # However if we find that the distance to the goal is less than or equal to the goal radius and we are in a start game state we indicate that we have reached the goal
        elif distancia_meta <= RADIO_META and self.estado_juego == "iniciar":
            print("Meta alcanzada!")
            # If show goal is false, we change it to true and get the time when the event happened
            if not self.mostrar_meta:
                self.mostrar_meta = True
                self.meta_time = pygame.time.get_ticks()
            # After reaching the goal we pause the game, and the game state becomes menu
            self.paused = True
            self.estado_juego = "menu"

        self.robot.actualizarse()
        return 

    # This function serves to handle program events
    def manejar_eventos(self):
        
        for event in pygame.event.get():
            # If the detected event is exit, we end the simulation
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            # Here we are going to detect the goal if the user presses the click button
            if event.type == pygame.MOUSEBUTTONDOWN:
                # If we are showing the goal screen, any click closes it and resumes
                if self.mostrar_meta:
                    self.mostrar_meta = False
                    self.paused = False
                    print("Reanudado tras meta (click)")
                    continue

                # Here the buttons for start, restart, map 1 and map 2 are handled
                if self.interfaz.btn_iniciar.collidepoint(event.pos):
                    self.estado_juego = "iniciar"
                    print("Botón Iniciar presionado")
                elif self.interfaz.btn_reiniciar.collidepoint(event.pos):
                    self.estado_juego = "menu"
                    self.mostrar_meta = False
                    self.paused = False
                    self.robot.posicion = pygame.math.Vector2(47, 320)
                    self.robot.angulo = 0
                    self.meta = pygame.math.Vector2(400, 200)
                    print("Botón Reiniciar presionado")
                elif self.interfaz.btn_mapa1.collidepoint(event.pos):
                    self.mapa_txt = self.gestor.cargar_mapa('map.txt')
                    self.mapa_estatico, self.muros = self.gestor.muros(self.mapa_txt)
                    self.interfaz.mapa_estatico = self.mapa_estatico
                    print("Botón Mapa 1 presionado")
                elif self.interfaz.btn_mapa2.collidepoint(event.pos):
                    self.mapa_txt = self.gestor.cargar_mapa('map2.txt')
                    self.mapa_estatico, self.muros = self.gestor.muros(self.mapa_txt)
                    self.interfaz.mapa_estatico = self.mapa_estatico
                    print("Botón Mapa 2 presionado")
                # If none of those buttons have been pressed it's because the user has indicated a goal point, which is handled with gestor.objetivo which converts that coordinate selected by the user into a coordinate based on TILE_SIZE
                else:
                    self.meta = self.gestor.objetivo(event.pos, TILE_SIZE)
                    print(f"Objetivo establecido en: {self.meta}")

    # This function is in charge of drawing rays, robot and interface
    def dibujar(self):
        # First the screen is cleared so as not to accumulate garbage stuff    
        self.screen.fill((0, 0, 0))

        # Here the static map is drawn continually which has no need to change because it's always the same one and this way computer resources are saved
        if isinstance(self.mapa_estatico, pygame.Surface):
            self.screen.blit(self.mapa_estatico, (0, 0))
            
        # Here we draw the rays, the robot and the interface on the screen that updates continually since these drawings are dynamic because they change with the robot movement
        self.raycaster.dibujar(self.screen)
        self.robot.dibujar(self.screen, self.distancia)
        self.interfaz.botones(self.screen)
        
        # This is the circle drawing so the user sees which goal they chose
        pygame.draw.circle(self.screen,(255,0,0), (int(self.meta.x), int(self.meta.y)), 5)

        # Show "Meta alcanzada" message on top of everything for 2 seconds
        if self.mostrar_meta:
            if pygame.time.get_ticks() - self.meta_time < 2000:
                self.interfaz.meta_alcanzada(self.screen)
            else:
                self.mostrar_meta = False