import os, sys, time, thread
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
        self.battleCost = 0
        self.fightingPlan = None


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
                    print "Trigger activated!"
                    thread.start_new_thread ( self.startPathFinding, ("Thread-1", self) )
                    self.semaphore = True #Semaphore UP
                    while(self.semaphore):
                        time.sleep(0.3) #Semaphore Lock

                    self.endingScreen(self.accCost, self.battleCost) #Show ending screen

    @staticmethod
    def startPathFinding(threadName, game):
        pygame.mixer.music.load(os.path.normcase("soundtrack/pegasus_fantasy_basic.mp3"))
        pygame.mixer.music.play(-1)

        initial_knights = utils.get_knights()
        knights_list = []
        weaker_knight = ['', 9999999, 0]
        for kn in initial_knights:
            if(kn[1] < weaker_knight[1]):
                weaker_knight = kn
            knights_list.append(AstarFight.Knight(kn))

        for knight in knights_list:
            if(knight.kn_name == weaker_knight[0]):
                knight.lives = knight.lives - 1 #reduzindo uma vida do mais fraco apenas para o a*

        houses_list = utils.get_houses()

        print "Deciding battle plan"
        fightingPlan = AstarFight.path_search(knights_list,houses_list)
        i = 1
        for knight_comb in fightingPlan[0]:
            print i
            for knight_in_comb in knight_comb:
                print knight_in_comb
            i+=1

        game.battleCost = fightingPlan[1]
        game.fightingPlan = fightingPlan[0]

        print "Deciding path to traverse"
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
        print "BattleCost: " + str(fightingPlan[1])
        game.semaphore = False #Semaphore DOWN

    def LoadSprites(self):
        self.agent = Agent(self.background.startCoordenate, self.background.startPoint)

    def endingScreen(self, accCost, battleTime):
        my_font = pygame.font.SysFont("Times New Roman", 15)
        end_screen = pygame.display.set_mode((800,500))
        end_background = pygame.image.load(os.path.normcase('images/final.jpg'))
        end_background = pygame.transform.scale(end_background, (600, 500))
        end_screen.blit(end_background,(200,0))
        labelTraverse = my_font.render(" Custo caminho: " + str(accCost), 1, (255,255,255))
        labelBattle = my_font.render(" Custo batalha: " + "%.2f" %battleTime, 1, (255,255,255))
        labelTotal = my_font.render(" Custo total: " + "%.2f" %(battleTime + accCost), 1, (255,255,255))

        label2 = my_font.render(" COMPONENTES", 1, (255,255,255))
        label3 = my_font.render(" Eric Grinstein", 1, (255,255,255))
        label4 = my_font.render(" Maria Beatriz Vaz", 1, (255,255,255))
        label5 = my_font.render(" Patrick Sava", 1, (255,255,255))

        end_screen.blit(label2, (5, 5))
        end_screen.blit(label3, (5, 30))
        end_screen.blit(label4, (5, 45))
        end_screen.blit(label5, (5, 60))
        end_screen.blit(labelTraverse, (5, 90))
        end_screen.blit(labelBattle, (5, 105))
        end_screen.blit(labelTotal, (5, 135))

        pygame.display.flip()
