import heapq, math, time

class Astar:

    class Node:
        def __init__(self, tuple):
            self.cost = tuple[0]
            self.position = tuple[1]
            self.parent = tuple[2]
            self.direction = tuple[3]
	    self.total_cost = tuple[4]

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
		mv_cost = self.move_cost(matrix, new_position)
                moves.append([mv_cost, new_position, self, 'N', self.total_cost+mv_cost])

            # SUL
            if(self.position[1] < j-1):
                new_position = [self.position[0], self.position[1] + 1]
		mv_cost = self.move_cost(matrix, new_position)
                moves.append([mv_cost, new_position, self, 'S',self.total_cost+mv_cost])

            # ESQUERDA
            if(self.position[0] > 0):
                new_position = [self.position[0] - 1, self.position[1]]
		mv_cost = self.move_cost(matrix, new_position)
                moves.append([mv_cost, new_position, self, 'E',self.total_cost+mv_cost])

            # DIREITA
            if(self.position[1] < i-1):
                new_position = [self.position[0] + 1, self.position[1]]
		mv_cost = self.move_cost(matrix, new_position)
                moves.append([mv_cost, new_position, self, 'D',self.total_cost+mv_cost])

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
            return [self.cost, self.position, self.parent, self.direction, self.total_cost]

    @staticmethod
    def path_heuristic(goal, current,next_dir, last_dir):
        #Mannhatan Modulus
        modA = current[0] - goal[0]
        modB = current[1] - goal[1]

        cost = (math.fabs(modA) + math.fabs(modB));

	if next_dir == last_dir:
		cost*=0.98
	return cost



    @staticmethod
    def path_search( matrix, start, goal ):
        startTime = time.time()
        heap = [] #Priority min heap to keep the positions to be expanded
        visited = {} #Nodes that have already been visited
	last_direction = 'E'
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
	    last_direction = current.direction
            for nextMove in current.possible_moves(matrix): # For each possible move
                #print "Checking neighbor node: "+ str(nextMove)
                nextMove = Astar.Node(nextMove)
                key = nextMove.node_key()
                cost = Astar.path_heuristic(goal, nextMove.position,nextMove.direction,last_direction) + nextMove.cost + nextMove.total_cost # Calculates the cost + heuristic of the new node
		if key in visited and cost < visited[key].cost:
                    #print "Found better path for node " + key
                    del visited[key]
                    heapq.heappush(heap, nextMove.to_tuple())
                    continue

                if key not in visited:
                    nextMove.cost = cost
                    heapq.heappush(heap, nextMove.to_tuple()) # Puts node in the expansion frontier heap

                #print "Next in heap: "+ str(heap[0])



