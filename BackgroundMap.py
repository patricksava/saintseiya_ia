__author__ = 'psava'

import pygame

class BackgroundMap:

    MAP_HEIGHT = 630
    MAP_WIDTH  = 630

    COORD_HEIGHT = 15
    COORD_WIDTH  = 15

    def __init__(self):
        mapfile = open('config/map.txt', 'r')
        self.mapMatrix = [[0 for x in range(42)] for x in range(42)]
        for i in range(42):
            line = mapfile.readline()
            for j in range(42):
                self.mapMatrix[j][i] = line[j]
                if(line[j] == 'I'):
                    self.startPoint = (j * self.COORD_HEIGHT, i* self.COORD_WIDTH)
                    self.startCoordenate = [j, i]
                if(line[j] == 'O'):
                    self.endPoint = (j * self.COORD_HEIGHT, i* self.COORD_WIDTH)
                    self.endCoordenate = [j, i]

        self.surface = self.prepareSurface()

    def prepareSurface(self):
        surface = pygame.Surface((self.MAP_HEIGHT, self.MAP_WIDTH))
        # prepare map
        for i in range(42):
            for j in range(42):
                rect = ((i*self.COORD_HEIGHT, j*self.COORD_WIDTH), (self.COORD_HEIGHT, self.COORD_WIDTH))
                surface.blit(self.getTerrain(j, i), (i*self.COORD_HEIGHT, j*self.COORD_WIDTH))

        return surface

    def render(self, screen):
        screen.blit(self.surface, (0, 0))


    def getTerrain(self, x, y):
        terrain = self.mapMatrix[y][x]
        terrainImage = None
        if(terrain == '_'):
            terrainImage = MapColors.MOUNTAIN
        elif(terrain == 'R'):
            terrainImage = MapColors.ROCKY
        elif(terrain == 'P'):
            terrainImage = MapColors.PLAIN
        elif(terrain == 'I'):
            terrainImage = MapColors.START
        elif(terrain == 'O'):
            terrainImage = MapColors.OBJECTIVE
        else:
            terrainImage = MapColors.SANCTUARY

        rect = pygame.Rect(0, 0, terrainImage.get_width(), terrainImage.get_height())
        image = pygame.Surface(rect.size).convert_alpha()
        image.blit(terrainImage, (0,0))
        return image


    def debugMatrix(self):
        for i in range(42):
            print self.mapMatrix[i]

    def getTerrainCost(self, x, y):
        terrain = self.mapMatrix[y][x]
        if(terrain == '_'):
            return 200
        if(terrain == 'P'):
            return 1
        if(terrain == 'R'):
            return 5

        return 1

class MapColors:
    MOUNTAIN = pygame.image.load('images/mountain_path.jpg')
    ROCKY = pygame.image.load('images/rock_path.jpg')
    PLAIN = pygame.image.load('images/plain_path.jpg')
    START = pygame.image.load('images/start_point.jpg')#(255, 0, 0)
    OBJECTIVE = pygame.image.load('images/end_point.jpg')#(0, 255, 0)
    SANCTUARY = pygame.image.load('images/sanctuary.jpg')#(255, 255, 0)