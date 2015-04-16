#! -*- coding:utf-8 -*-

import heapq, math, time, copy

import utils

class AstarFight:

    class Knight:
        def __init__(self, tuple):
            self.kn_name = tuple[0]
            self.cosmic_power = tuple[1]
            self.lives = tuple[2]

        def decLife(self):
            self.lives -= 1
        def isDead(self):
            if not self.lives:
                return 1
            return 0

        def __eq__(self, other):
            return self.kn_name == other.kn_name

        def __str__(self):
            return self.kn_name


    class Node:
        seq_id = 0

        all_knights_combination = None

        def __init__(self, tuple ):
            self.heuristic_result = tuple[0];

            self.houses_left = tuple[1]
            self.knights_left = tuple[2] #knights list
            self.parent = tuple[3]
            self.time_elapsed = tuple[4]
            self.time_from_house_before = tuple[5]
            self.id = AstarFight.Node.seq_id
            self.knights_used_before = tuple[6]
            AstarFight.Node.seq_id += 1



        def node_key(self):
            return self.id


        def to_tuple(self):
            return [self.heuristic_result, self.houses_left, self.knights_left, self.parent, self.time_elapsed, self.time_from_house_before, self.knights_used_before]

        def __str__(self):
            return "houses_left: "+str(len(self.houses_left))+" nodeid:"+str(self.id)

        def getNextNode(self):
            # Cache das combinações entre todos os cavaleiros -> não está tirando vidas

            '''if len(self.knights_left) == 5:
                if AstarFight.Node.all_knights_combination == None:
                    AstarFight.Node.all_knights_combination = utils.get_all_combinations(self.knights_left)
                    combs = AstarFight.Node.all_knights_combination
                else:
                    combs = AstarFight.Node.all_knights_combination
            else:
                combs = utils.get_all_combinations(self.knights_left)'''


            combs = utils.get_all_combinations(self.knights_left)



            for comb in combs:

                #otimizar: fazer um crivo, checar se já está calculando
                total_power = 0
                new_knights_left = copy.deepcopy(self.knights_left)
                #print ">>>"

                for knight in comb:
                    #print str(knight)
                    total_power += knight.cosmic_power
                    pos = 0
                    for kn in new_knights_left:
                        if knight == kn:
                            kn.decLife()
                            if kn.isDead():
                                 del new_knights_left[pos]
                        pos += 1

                time_fight = self.houses_left[0]/total_power

                new_houses = copy.deepcopy(self.houses_left)
                del new_houses[0]


                if new_knights_left:
                    new_node = AstarFight.Node([self.heuristic_result , new_houses , new_knights_left , self , self.time_elapsed+time_fight, time_fight, comb,self.id])
                    new_node.heuristic_result = AstarFight.heuristic(new_node)
                    yield new_node

    @staticmethod
    def heuristic( node ):
        houses_left_total_time = 0
        knights_left_total_power = 0

        house_count = 0
        #print "houses>"
        for house in node.houses_left:
            house_count += 1
            #print str(house)
            houses_left_total_time += house
        #print "knights>"
        for knight in node.knights_left:
            #print knight.kn_name,knight.cosmic_power,knight.lives
            knights_left_total_power += knight.lives*knight.cosmic_power


        cost = houses_left_total_time/knights_left_total_power

        #cost*=len(node.knights_used_before)

        #print "heurisica informa>",cost

        return cost /(12 - house_count)





    @staticmethod
    def path_search( knights, houses ):
        startTime = time.time()
        heap = [] #Priority min heap to keep the positions to be expanded
        visited = {} #Nodes that have already been visited
        heapq.heappush(heap, [ 0, houses , knights, None, 0, 0, []]) # Includes start point as first node in the heap

        while len(heap) > 0:

            current = AstarFight.Node(heapq.heappop(heap)) # Removes the best node front he expansion frontier
            #print "\n\n"+str(current)
            if not current.houses_left: #Found objective

                n = current
                print str(current)
                listSteps = []
                startTimeReversing = time.time()
                while n.parent != None: # Create a list of steps from last to first
                    listSteps.append(n.knights_used_before)
                    n = n.parent

                listSteps.reverse() # Reverse steps so that we get the directions from start to goal
                finishTime = time.time()

                print "tempo gasto:",current.time_elapsed
                return listSteps

            visited[current.id] = current # Sets node as visited
            for nextMove in current.getNextNode(): # For each possible move
                key = nextMove.id
                if key in visited and nextMove.heuristic_result < visited[key].heuristic_result:

                    del visited[key]
                    if nextMove.knights_left:
                        heapq.heappush(heap, nextMove.to_tuple())
                    continue

                if key not in visited:
                    heapq.heappush(heap, nextMove.to_tuple()) # Puts node in the expansion frontier heap

        print "heap ficou vazio...caramba"

__author__ = 'eric, mbvaz, psava'
