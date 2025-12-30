#Setting for the main program
TILE_SIZE = 32

# The FOV is 180 degrees so that the robot can “see” what is in front of it and to the sides, without looking back.
FOV = 180

#The number of rays to be cast
RAYS = 80

# Here I set the width and height of the window.
ANCHO_VENTANA = 800
ALTO_VENTANA = 480

# Here, the initial coordinates are established where the robot is called for the first time.
COORDENADAS_INICIALES_ROBOT = (47, 320)

#Settings for choque detection
RADIO_META = 5
#Settings for robot behavior
DISTANCIA_MAXIMA_EFECTIVA = 120
PENALIZACION_CHOQUE = -5000
FACTOR_PESO_ANGULO = 10