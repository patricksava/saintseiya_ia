import heapq

class Astar:

    class Node:
        def __init__(self, tuple):
            self.cost = tuple[0]
            self.position = tuple[1]
            self.parent = tuple[2]
            self.direction = tuple[3]

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
		return ((current[0] - goal[0])**2 + (current[1] - goal[1])**2)**0.5


    @staticmethod
    def path_search( matrix, start, goal ):
        heap = [] #Priority min heap to keep the positions to be expanded
        visited = {} #Nodes that have already been visited

        heapq.heappush(heap, [0, start, None, '']) # Includes start point as first node in the heap

        while len(heap) > 0:
            current = Astar.Node(heapq.heappop(heap)) # Removes the best node front he expansion frontier
            if current.position == goal:

                print "We have a f***ing winner!"
                n = current
                listSteps = []
                while n.parent != None: # Create a list of steps from last to first
                    listSteps.append(n.direction)
                    n = n.parent

                listSteps.reverse() # Reverse steps so that we get the directions from start to goal
                return listSteps

            visited[current.node_key()] = current # Sets node as visited
            for nextMove in current.possible_moves(matrix): # For each possible move
                nextMove = Astar.Node(nextMove)
                cost = Astar.path_heuristic(goal, nextMove.position) + nextMove.cost # Calculates the cost + heuristic of the new node
                if nextMove.node_key() in visited and cost < visited[nextMove.node_key()].cost:
                    del visited[nextMove.node_key()]

                if nextMove.node_key() not in visited:
                    nextMove.cost = cost
                    heapq.heappush(heap, nextMove.to_tuple()) # Puts node in the expansion frontier heap






    '''
    def path_search ( matrix, start, goal ):
        heap = []
        heapq.heappush(heap,[0, start])

        cost_so_far = [[-1 for x in range(len(matrix))] for x in range(len(matrix[0]))]
        came_from = []
        cost_so_far[start[0]][start[1]] = 0

        while True:
            try:
                current = heapq.heappop(heap)

                if (current[1] == goal):
                    break

                if(cost_so_far[current[1][0]][current[1][1]] == -1):
                    for next in Astar.possible_moves(matrix, current[1]):
                        new_cost = cost_so_far[current[1][0]][current[1][1]] + next[0]
                        if new_cost < cost_so_far[next[1][0]][next[1][1]]:
                            cost_so_far[next[1][0]][next[1][1]] = new_cost
                            priority = new_cost + Astar.path_heuristic(goal, next[1])
                            heapq.heappush(heap, [priority, next[1]])
                            came_from.append(next[2])

            except IndexError as inst:
                break

        return [came_from, cost_so_far]
'''


