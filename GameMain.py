import os, sys, csv, time
import pygame

from Agent import Agent
from BackgroundMap import BackgroundMap
from Astar import Astar

class GameMain:

    def __init__(self, width=630, height=630):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.FPS = 30
        self.fpsClock = pygame.time.Clock()
        self.background = BackgroundMap()
	self.knights = []
	self.houses = []
	with open('config/knights.csv') as knights_file:
    	    knights = csv.DictReader(knights_file)
	    for knight in knights:
		self.knights.append(knight)
	with open('config/houses.csv') as houses_file:
    	    houses = csv.DictReader(houses_file)
	    for house in houses:
		self.houses.append(house)
  
  	''' DEBUG 
	for knight in self.knights:
	    print knight['name'],knight['lives'],knight['cosmic-power']
	for house in self.houses:
	    print house['sign'],house['difficulty'],house['number']
	    DEBUG'''
    

    def MainLoop(self):
        pygame.key.set_repeat(100, 100)
        self.background.render(self.screen)
        self.LoadSprites()
        #self.agentSprites.draw(self.screen)
        pygame.display.flip()
        self.agent.render(self.screen)
        returnedValue = Astar.path_search(self.background.mapMatrix, self.background.startCoordenate, self.background.endCoordenate)
        print returnedValue
        '''
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT or
                        event.key == pygame.K_UP or event.key == pygame.K_DOWN):
                        self.background.render(self.screen)
                        self.agent.move(event.key, self.screen)
        '''
        #self.background.debugMatrix()
        for step in returnedValue:
            self.background.render(self.screen)
            self.agent.move(step, self.screen)
            pygame.display.update()
            self.fpsClock.tick(self.FPS)
            time.sleep(0.2)


    def LoadSprites(self):
        self.agent = Agent(self.background.startCoordenate, self.background.startPoint)
        #self.agentSprites = pygame.sprite.RenderPlain((self.agent))
