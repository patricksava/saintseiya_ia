import os, sys, csv, time, thread
import pygame
import utils

from Agent import Agent
from BackgroundMap import BackgroundMap
from Astar import Astar
from Astar_fight import AstarFight


class GameMain:

    def __init__(self, width=630, height=630):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Os Cavaleiros do Zodiaco - Busca (heuristica) pelo Santuario")
        self.FPS = 30
        self.fpsClock = pygame.time.Clock()
        self.background = BackgroundMap()
        self.knights = []
        self.houses = []
        self.semaphore = False
        self.accCost = 0


    def MainLoop(self):
        pygame.key.set_repeat(100, 100)
        self.background.render(self.screen)
        self.LoadSprites()
        pygame.display.flip()
        self.agent.render(self.screen)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYUP and event.key == pygame.K_p:
                    thread.start_new_thread ( self.startPathFinding, ("Thread-1", self) )
                    self.semaphore = True #Semaphore UP
                    while(self.semaphore):
                        time.sleep(0.3) #Semaphore Lock

                    self.endingScreen(self.accCost) #Show ending screen

    @staticmethod
    def startPathFinding(threadName, game):
        pygame.mixer.music.load("soundtrack/pegasus_fantasy_basic.mp3")
        pygame.mixer.music.play(-1)

        initial_knights = utils.get_knights()
        knights_list = []

        for kn in initial_knights:
            knights_list.append(AstarFight.Knight(kn))

        houses_list = utils.get_houses()

        fightingPlan = AstarFight.path_search(knights_list,houses_list)
        i = 1
        for knight_comb in fightingPlan:
            print i
            for knight_in_comb in knight_comb:
                print knight_in_comb
            i+=1


        returnedValue = Astar.path_search(game.background, game.background.startCoordenate, game.background.endCoordenate)
        print returnedValue
        for step in returnedValue:
            game.accCost += game.background.getTerrainCost(game.agent.y, game.agent.x)
            game.background.render(game.screen)
            game.agent.move(step, game.screen)
            pygame.display.update()
            game.fpsClock.tick(game.FPS)
            time.sleep(0.1)

        print "AccCost: " + str(game.accCost)
        game.semaphore = False #Semaphore DOWN

    def LoadSprites(self):
        self.agent = Agent(self.background.startCoordenate, self.background.startPoint)
        #self.agentSprites = pygame.sprite.RenderPlain((self.agent))

    def endingScreen(self, accCost):
        my_font = pygame.font.SysFont("Times New Roman", 15)
        end_screen = pygame.display.set_mode((600,500))
        end_background = pygame.image.load('images/final.jpg')
        end_background = pygame.transform.scale(end_background, (600, 500))
        end_screen.blit(end_background,(0,0))
        label = my_font.render(" CUSTO: " + str(accCost), 1, (255,255,255))
        label2 = my_font.render(" COMPONENTES", 1, (255,255,255))
        label3 = my_font.render(" Eric Gristein", 1, (255,255,255))
        label4 = my_font.render(" Maria Beatriz", 1, (255,255,255))
        label5 = my_font.render(" Patrick Sava", 1, (255,255,255))
        end_screen.blit(label2, (5, 5))
        end_screen.blit(label3, (5, 30))
        end_screen.blit(label4, (5, 45))
        end_screen.blit(label5, (5, 60))
        end_screen.blit(label, (5, 90))
        pygame.display.flip()
