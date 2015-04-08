import heapq

class Astar:

    @staticmethod
    def path_heuristic(goal, current):
		return ((current[0] - goal[0])**2 + (current[1] - goal[1])**2)**0.5

    @staticmethod
    def possible_moves( matrix, position ):
        i = len(matrix)
        j = len(matrix[0])
        moves = []

        # NORTE
        if(position[1] > 0):
            new_position = [position[0], position[1] - 1]
            moves.append({'cost':Astar.move_cost(matrix, new_position), 'position': new_position, 'direction':'N', 'parent':position})

        # SUL
        if(position[1] < j-1):
            new_position = [position[0], position[1] + 1]
            moves.append({'cost':Astar.move_cost(matrix, new_position), 'position': new_position, 'direction':'S', 'parent':position})

        # ESQUERDA
        if(position[0] > 0):
            new_position = [position[0] - 1, position[1]]
            moves.append({'cost':Astar.move_cost(matrix, new_position), 'position': new_position, 'direction':'E', 'parent':position})

        # DIREITA
        if(position[1] < i-1):
            new_position = [position[0] + 1, position[1]]
            moves.append({'cost':Astar.move_cost(matrix, new_position), 'position': new_position, 'direction':'D', 'parent':position})

        return moves

    @staticmethod
    def move_key( move ):
        ind1 = move['position'][0]
        ind2 = move['position'][1]
        print str(ind1) + '-' + str(ind2)
        return str(ind1) + '-' + str(ind2)

    @staticmethod
    def path_search( matrix, start, goal ):
        heap = [] #Priority min heap to keep the positions to be expanded
        visited = {} #Nodes that have already been visited

        heapq.heappush(heap, {'cost':0, 'position':start, 'parent':None}) # Includes start point as first node in the heap

        while len(heap) > 0:
            current = heapq.heappop(heap) # Removes the best node front he expansion edge
            if current['position'] == goal:
                print "We have a f***ing winner!"
                break
            nodeName = Astar.move_key(current)
            visited[nodeName] = current # Sets node as visited
            for nextMove in Astar.possible_moves(matrix, current['position']):
                cost = Astar.path_heuristic(goal, nextMove['position']) + nextMove['cost'] #Calculates the cost + heuristic of the new node
                if Astar.move_key(nextMove) in visited and cost < visited[Astar.move_key(nextMove)]['cost']:
                    del visited[Astar.move_key(nextMove)]

                if Astar.move_key(nextMove) not in visited:
                    nextMove['cost'] = cost
                    heapq.heappush(heap, nextMove)





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

    @staticmethod
    def move_cost(matrix, position):
        terrain = matrix[position[0]][position[1]]
        if(terrain == '_'):
            return 200
        if(terrain == 'P'):
            return 1
        if(terrain == 'R'):
            return 5

        return 1

