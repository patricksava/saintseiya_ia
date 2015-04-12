import os, sys, csv, time, thread
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


    def MainLoop(self):
        pygame.key.set_repeat(100, 100)
        self.background.render(self.screen)
        self.LoadSprites()
        #self.agentSprites.draw(self.screen)
        pygame.display.flip()
        self.agent.render(self.screen)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYUP and event.key == pygame.K_p:
                    thread.start_new_thread ( self.startPathFinding, ("Thread-1", self) )
                    #if (event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT or
                    #    event.key == pygame.K_UP or event.key == pygame.K_DOWN):
                    #    self.background.render(self.screen)
                    #    self.agent.move(event.key, self.screen)

            #self.background.debugMatrix()

    @staticmethod
    def startPathFinding(threadName, game):
        accCost = 0
        returnedValue = Astar.path_search(game.background.mapMatrix, game.background.startCoordenate, game.background.endCoordenate)
        #print returnedValue
        for step in returnedValue:
            accCost = accCost + game.background.getTerrainCost(game.agent.y, game.agent.x)
            game.background.render(game.screen)
            game.agent.move(step, game.screen)
            pygame.display.update()
            game.fpsClock.tick(game.FPS)
            time.sleep(0.1)

        print "AccCost: " + str(accCost)

    def LoadSprites(self):
        self.agent = Agent(self.background.startCoordenate, self.background.startPoint)
        #self.agentSprites = pygame.sprite.RenderPlain((self.agent))
