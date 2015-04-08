import heapq

class Astar:

    @staticmethod
    def path_heuristic(current, goal):
		return ((current[0] - goal[0])**2 + (current[1] - goal[1])**2)**0.5

    @staticmethod
    def possible_moves( matrix, position ):
        i = len(matrix)
        j = len(matrix[0])
        moves = []

        # NORTE
        if(position[1] > 0):
            new_position = [position[0], position[1] - 1]
            moves.append([Astar.move_cost(matrix, new_position),new_position])

        # SUL
        if(position[1] < j-1):
            new_position = [position[0], position[1] + 1]
            moves.append([Astar.move_cost(matrix, new_position),new_position])

        # ESQUERDA
        if(position[0] > 0):
            new_position = [position[0] - 1, position[1]]
            moves.append([Astar.move_cost(matrix, new_position),new_position])

        # DIREITA
        if(position[1] < i-1):
            new_position = [position[0] + 1, position[1]]
            moves.append([Astar.move_cost(matrix, new_position),new_position])

        return moves

    @staticmethod
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

                for next in Astar.possible_moves(matrix, current[1]):
                    new_cost = cost_so_far[current[1][0]][current[1][1]] + next[0]
                    if cost_so_far[next[1][0]][next[1][1]] == -1 or new_cost < cost_so_far[next[1][0]][next[1][1]]:
                        cost_so_far[next[1][0]][next[1][1]] = new_cost
                        priority = new_cost + Astar.path_heuristic(goal, next[1])
                        heapq.heappush(heap, [priority, next[1]])
                        came_from.append(next)

            except IndexError as inst:
                break

        return [came_from, cost_so_far]

    @staticmethod
    def move_cost(matrix, position):
        terrain = matrix[position[0]][position[1]]
        if(terrain == '_'):
            return 200
        if(terrain == 'P'):
            return 1
        if(terrain == 'R'):
            return 5

        return 0

