import heapq, math, time

class Astar:

    class Node:
        def __init__(self, tuple):
            self.cost = tuple[0]
            self.position = tuple[1]
            self.parent = tuple[2]
            self.direction = tuple[3]

        def __str__(self):
            return "Node: ("+ str(self.position[0]) +","+ str(self.position[1]) +") - Cost: "+ str(self.cost)

        def node_key(self):
            return str(self.position[0]) + '-' + str(self.position[1])

        def possible_moves( self, matrix ):
            i = len(matrix)
            j = len(matrix[0])
            moves = []

            # NORTE
            if(self.position[1] > 0):
                new_position = [self.position[0], self.position[1] - 1]
                moves.append([self.move_cost(matrix, new_position), new_position, self, 'N'])

            # SUL
            if(self.position[1] < j-1):
                new_position = [self.position[0], self.position[1] + 1]
                moves.append([self.move_cost(matrix, new_position), new_position, self, 'S'])

            # ESQUERDA
            if(self.position[0] > 0):
                new_position = [self.position[0] - 1, self.position[1]]
                moves.append([self.move_cost(matrix, new_position), new_position, self, 'E'])

            # DIREITA
            if(self.position[1] < i-1):
                new_position = [self.position[0] + 1, self.position[1]]
                moves.append([self.move_cost(matrix, new_position), new_position, self, 'D'])

            return moves

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
            return [self.cost, self.position, self.parent, self.direction]

    @staticmethod
    def path_heuristic(goal, current):
        #Mannhatan Modulus
        modA = current[0] - goal[0]
        modB = current[1] - goal[1]

        return (math.fabs(modA) + math.fabs(modB));



    @staticmethod
    def path_search( matrix, start, goal ):
        startTime = time.time()
        heap = [] #Priority min heap to keep the positions to be expanded
        visited = {} #Nodes that have already been visited

        heapq.heappush(heap, [0, start, None, '']) # Includes start point as first node in the heap

        while len(heap) > 0:
            current = Astar.Node(heapq.heappop(heap)) # Removes the best node front he expansion frontier
            print "\n\nAnalyzing node: "+str(current)
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
            for nextMove in current.possible_moves(matrix): # For each possible move
                print "Checking neighbor node: "+ str(nextMove)
                nextMove = Astar.Node(nextMove)
                key = nextMove.node_key()
                cost = Astar.path_heuristic(goal, nextMove.position) + nextMove.cost # Calculates the cost + heuristic of the new node
                if key in visited and cost < visited[key].cost:
                    print "Found better path for node " + key
                    del visited[key]
                    heapq.heappush(heap, nextMove.to_tuple())
                    continue

                if key not in visited:
                    nextMove.cost = cost
                    heapq.heappush(heap, nextMove.to_tuple()) # Puts node in the expansion frontier heap

                print "Next in heap: "+ str(heap[0])



