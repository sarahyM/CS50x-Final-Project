# Here I import the pygame library and the simulation class, as well as exit
import pygame
from sys import exit
from simulacion import Simulacion

# Here I start the simulation by creating the simulation object.
simulacion = Simulacion()

while True:
    # First, I have to load all the pygame events, such as starting the game, knowing if the user has reset the program, and interpreting whether they have clicked on the start button, restarting map 1 or map 2, although map 1 is loaded by default here.
    simulacion.manejar_eventos()
    #I need the actualizar_movimiento function that handles all the robot's logic for moving.
    simulacion.actualizar_movimiento()
    # This function is responsible for drawing the interface, the rays, and the robot.
    simulacion.dibujar()

    # Here refresh the window
    pygame.display.update()
    # Here it updates to 60 frames per second.
    simulacion.clock.tick(60)