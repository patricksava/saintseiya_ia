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
                self.mapMatrix[i][j] = line[j]
                if(line[j] == 'I'):
                    self.startPoint = (i * self.COORD_HEIGHT, j* self.COORD_WIDTH)
                    self.startCoordenate = [i, j]
                if(line[j] == 'O'):
                    self.endPoint = (i * self.COORD_HEIGHT, j* self.COORD_WIDTH)
                    self.endCoordenate = [i, j]

        self.surface = self.prepareSurface()

    def prepareSurface(self):
        surface = pygame.Surface((self.MAP_HEIGHT, self.MAP_WIDTH))
        # prepare map
        for i in range(42):
            for j in range(42):
                rect = ((j*self.COORD_HEIGHT, i*self.COORD_WIDTH), (self.COORD_HEIGHT, self.COORD_WIDTH))
                pygame.draw.rect(surface, self.getColor(i, j), rect)

        return surface

    def render(self, screen):
        screen.blit(self.surface, (0, 0))


    def getColor(self, x, y):
        terrain = self.mapMatrix[x][y]
        if(terrain == '_'):
            return MapColors.MONTAIN
        elif(terrain == 'R'):
            return MapColors.ROCKY
        elif(terrain == 'P'):
            return MapColors.PLAIN
        elif(terrain == 'I'):
            return MapColors.START
        elif(terrain == 'O'):
            return MapColors.OBJECTIVE
        else:
            return MapColors.SANCTUARY



    def debugMatrix(self):
        for i in range(42):
            print self.mapMatrix[i]


class MapColors:
    MONTAIN = (0,0,0)
    ROCKY = (125, 125, 125)
    PLAIN = (200, 200, 200)
    START = (255, 0, 0)
    OBJECTIVE = (0, 255, 0)
    SANCTUARY = (255, 255, 0)