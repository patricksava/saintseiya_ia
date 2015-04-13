import heapq, math, time

import utils

class AstarFight:

    class knight:
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
            return self.name == other.name


    class Node:
        id = 0

        def __init__(self, tuple):
            self.houses_left = tuple[0]
            self.knights_left = tuple[1] #knights list
            self.parent = tuple[2]
            self.time_elapsed = tuple[3]
            self.time_next_house = tuple[4]
            self.id = id

            id += 1


        def node_key(self):
            return self.id


        def to_tuple(self):
            return [self.time_next_house, self.houses_left, self.knights_left, self.parent, self.time_elapsed, self.id]


        def getNextNode(self):
            "Gets next possible combination of knights in the next house"
            combs = utils.get_all_combinations(self.knights_left)

            for comb in combs:
                #otimizar: fazer um crivo, checar se já está calculando
                total_power = 0
                new_knights = self.knights_left

                for knight in comb:
                    total_power += knight.cosmic_power
                    pos = 0
                    for knight_used in new_knights:
                        if knight_used == knight:
                            knight_used.decLife()

                            if knight_used.isDead():
                                del new_knights[pos]
                        pos += 1


                time_fight = self.houses_left[0]/total_power

                new_houses = self.houses_left
                del new_houses[0]



                yield Node([new_houses,new_knights, self, self.time_elapsed+time_fight,time_fight])


    @staticmethod
    def heuristic( node ):
        houses_left_total_time = 0
        knights_left_total_power = 0

        for house in node.houses_left:
            houses_left_total_time += house

        for knight in node.knights_left:
            knights_left_total_power += knights.cosmic_power

        return houses_left_total_time/knights_left_total_power





    @staticmethod
    def path_search( bg_map, start, goal ):
        startTime = time.time()
        heap = [] #Priority min heap to keep the positions to be expanded
        visited = {} #Nodes that have already been visited
        heapq.heappush(heap, [0, start, None, '',0]) # Includes start point as first node in the heap

        while len(heap) > 0:
            current = Astar.Node(heapq.heappop(heap)) # Removes the best node front he expansion frontier
            #print "\n\nAnalyzing node: "+str(current)
            if current.position == goal: #Found objective
                n = current
                listSteps = []
                startTimeReversing = time.time()
                while n.parent != None: # Create a list of steps from last to first
                    listSteps.append(n.direction)
                    n = n.parent

                listSteps.reverse() # Reverse steps so that we get the directions from start to goal
                finishTime = time.time()
                print "Recovering path: "+str(finishTime - startTimeReversing)
                print "Total execution time: "+str(finishTime - startTime)
                return listSteps

            visited[current.node_key()] = current # Sets node as visited
            for nextMove in bg_map.moves[current.position[0]][current.position[1]]: # For each possible move
                #print "Checking neighbor node: "+ str(nextMove)

                nextMove = Astar.Node(nextMove)
                nextMove.parent = current
                nextMove.total_cost = current.total_cost + nextMove.cost
                key = nextMove.node_key()
                cost = Astar.path_heuristic(goal, nextMove.position) + nextMove.cost + nextMove.total_cost # Calculates the cost + heuristic of the new node
                if key in visited and cost < visited[key].cost:
                    #print "Found better path for node " + key
                    del visited[key]
                    heapq.heappush(heap, nextMove.to_tuple())
                    continue

                if key not in visited:
                    nextMove.cost = cost
                    heapq.heappush(heap, nextMove.to_tuple()) # Puts node in the expansion frontier heap

                #print "Next in heap: "+ str(heap[0])



__author__ = 'eric'
