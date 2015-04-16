#! -*- coding:utf-8 -*-

import heapq, math, time, copy, sys

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

        combinations_cache = {}
        nodes_visited = {}

        def __init__(self, tuple ):
            self.cost = tuple[0]
            self.houses_left = tuple[1]
            self.knights_left = tuple[2] #knights list
            self.parent = tuple[3]
            self.time_elapsed = tuple[4]
            self.time_from_house_before = tuple[5]
            self.knights_used_before = tuple[6]
            self.key = str(len(self.houses_left))
            for knight in self.knights_left:
                self.key = self.key+knight.kn_name+str(knight.lives)



        def node_key(self):
            return self.key


        def to_tuple(self):
            return [self.heuristic_result, self.houses_left, self.knights_left, self.parent, self.time_elapsed, self.time_from_house_before, self.knights_used_before]

        def __str__(self):
            return "houses_left: "+str(len(self.houses_left))+" nodeid:"+str(self.key)

        def getNextNode(self):

            #crivo para não combinar
            knights_to_be_combined = ""
            for kn in self.knights_left:
                knights_to_be_combined += kn.kn_name + str(kn.lives)
            if knights_to_be_combined in AstarFight.Node.combinations_cache:
                combs = AstarFight.Node.combinations_cache[knights_to_be_combined]
            else:
                combs = utils.get_all_combinations(self.knights_left)
                AstarFight.Node.combinations_cache[knights_to_be_combined] = combs



            new_nodes = []
            for comb in combs:
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


                if new_knights_left or len(new_houses) == 0:
                    new_node = AstarFight.Node([-1 , new_houses , new_knights_left , self , self.time_elapsed+time_fight, time_fight, comb])
                    if not new_node.node_key() in AstarFight.Node.nodes_visited:
                        new_node.heuristic_result = AstarFight.heuristic(new_node) + time_fight +self.time_elapsed #*(12 - len(new_houses))
                        new_nodes.append(new_node)

            return new_nodes

    @staticmethod
    def heuristic( node ):
        houses_left_total_time = 0
        for house in node.houses_left:
            houses_left_total_time += house
        knights_left_lives = 0



        cost = houses_left_total_time/6.5


        return cost





    @staticmethod
    def path_search( knights, houses ):
        startTime = time.time()
        heap = [] #Priority min heap to keep the positions to be expanded
        visited = {} #Nodes that have already been visited
        heapq.heappush(heap, [ 0, houses , knights, None, 0, 0, []]) # Includes start point as first node in the heap
        house_seen = 12
        while len(heap) > 0:

            current = AstarFight.Node(heapq.heappop(heap)) # Removes the best node front he expansion frontier

            if len(current.houses_left) < house_seen:
                print str(current)
                house_seen = len(current.houses_left)

            if not current.houses_left: #Found objective

                n = current
                listSteps = []
                startTimeReversing = time.time()
                while n.parent != None: # Create a list of steps from last to first
                    listSteps.append(n.knights_used_before)
                    n = n.parent

                listSteps.reverse() # Reverse steps so that we get the directions from start to goal
                finishTime = time.time()

                print "Total execution time: "+str(finishTime - startTime)
                print "tempo gasto:",current.time_elapsed
                return listSteps

            AstarFight.Node.nodes_visited[current.node_key()] = current # Sets node as visited
            for nextMove in current.getNextNode(): # For each possible move
                key = nextMove.node_key()
                if key in AstarFight.Node.nodes_visited:
                    continue
                    #print "ja visitei:"+ str(nextMove),str(nextMove.parent)
                    if nextMove.cost < AstarFight.Node.nodes_visited[key].cost:
                        #print "custo melhorou:",str(nextMove)
                        del visited[key]
                        heapq.heappush(heap, nextMove.to_tuple())


                else: #key not in visited:
                    heapq.heappush(heap, nextMove.to_tuple()) # Puts node in the expansion frontier heap


__author__ = 'eric, mbvaz, psava'
