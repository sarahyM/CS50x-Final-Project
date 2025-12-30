import pygame

# This is the class that manages the simulator map
class GestorMapa:
    def __init__(self, TILE_SIZE):
        # We pass it tile_size and here basically it loads the background image and the image for the blocks
        self.tile_size = TILE_SIZE
        self.original_background = pygame.image.load('assets/background.png').convert_alpha()
        self.background = pygame.transform.scale(self.original_background, (800, 400))
        self.original_block = pygame.image.load('assets/blocks.png').convert_alpha()
        self.blocks = pygame.transform.scale(self.original_block, (self.tile_size, self.tile_size))

    # Here it loads the map depending on the .txt file where the characters # or e are characters indicating that the robot cannot pass through there
    def cargar_mapa(self, archivo):
        mapa = []
        # We open the file and save its content in the variable mapa
        with open(archivo, 'r') as f:
            for linea in f:
                mapa.append(list(linea.strip()))
        return mapa
    
    # This function is in charge of defining the walls
    def muros (self, mapa_estatico):
        muros = []
        superficie_mapa = self.background.copy()
        for fila_index, fila in enumerate(mapa_estatico):
            for col_index, caracter in enumerate(fila):
                if caracter == '#':
                    nuevo_muro = pygame.Rect(col_index * self.tile_size, fila_index * self.tile_size, self.tile_size, self.tile_size)
                    muros.append(nuevo_muro)
                    superficie_mapa.blit(self.blocks, nuevo_muro)
                elif caracter == 'e':
                    entrada = pygame.Rect(col_index * self.tile_size, fila_index * self.tile_size, self.tile_size, self.tile_size)
                    muros.append(entrada)
        return superficie_mapa, muros
    
    # This function is in charge of handling the goal established by the user mapping it to a tile_size coordinate
    def objetivo(self, mouse, TILE_SIZE):
        tile_x = mouse[0] // self.tile_size
        tile_y = mouse[1] // self.tile_size
        return pygame.math.Vector2(tile_x * self.tile_size + (TILE_SIZE / 2), tile_y * self.tile_size + (TILE_SIZE / 2))
 