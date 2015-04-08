__author__ = 'psava'

import os
import pygame
from pygame.locals import *


class Agent(pygame.sprite.Sprite):
    def __init__(self, coord, surfcoord):
        pygame.sprite.Sprite.__init__(self)
        self.x = coord[0]
        self.y = coord[1]
        self.xSurf = surfcoord[0]
        self.ySurf = surfcoord[1]
        self.sheet = pygame.image.load('images/seiya_front_small.png')
        self.rect = Rect(0, 0, self.sheet.get_width(), self.sheet.get_height())
        self.image = pygame.Surface(self.rect.size).convert()
        self.image.blit(self.sheet, (0, 0), self.rect)

    def render(self, surface):
        surface.blit(self.image, (self.xSurf, self.ySurf))

    def move(self, key, surface):
        if(key == 'D'):
            self.xSurf += self.rect.width
            self.x = self.x + 1
        elif(key == 'E'):
            self.xSurf -= self.rect.width
            self.x = self.x - 1
        elif(key == 'N'):
            self.ySurf -= self.rect.height
            self.y = self.y - 1
        elif(key == 'S'):
            self.ySurf += self.rect.height
            self.y = self.y + 1

        if(self.xSurf >= surface.get_width()):
            self.xSurf -= self.rect.width
            self.x = self.x - 1
        elif(self.xSurf < 0):
            self.xSurf += self.rect.width
            self.x = self.x + 1
        elif(self.ySurf < 0):
            self.ySurf += self.rect.height
            self.y = self.y + 1
        elif(self.ySurf >= surface.get_height()):
            self.ySurf -= self.rect.height
            self.y = self.y - 1

        self.render(surface)
