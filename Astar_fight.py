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


    class Node:
        def __init__(self, tuple):
            self.houses_left = tuple[0]
            self.knights_left = tuple[1] #knights list
            self.parent = tuple[2]
            

        def __str__(self):
            return "Node: ("+ str(self.position[0]) +","+ str(self.position[1]) +") - Cost: "+ str(self.cost)

        def node_key(self):
            return str(self.position[0]) + '-' + str(self.position[1])


        def move_cost(self, matrix, position):
            terrain = matrix[position[0]][position[1]]
            if(terrain == '_'):
                return 200
            if(terrain == 'P'):
                return 1
            if(terrain == 'R'):
                return 5

            return 1

        def to_tuple(self):
            return [self.cost, self.position, self.parent, self.direction, self.total_cost]

    @staticmethod
    def path_heuristic(goal, current):
        #Mannhatan Modulus
        modA = current[0] - goal[0]
        modB = current[1] - goal[1]

        cost = (math.fabs(modA) + math.fabs(modB));

        return cost



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
