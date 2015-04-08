import heapq

class Astar:

	def possible_moves( matrix, position ):
		i = len(matrix)
		j = len(matrix[0])
		moves = []

		# NORTE
		if(position[1] > 0)
			moves.push([position[0], position[1] - 1])

		# SUL
		if(position[1] < j-1)
			moves.push([position[0], position[1] + 1])

		# ESQUERDA
		if(position[0] > 0)
			moves.push([position[0] - 1, position[1]])

		# DIREITA
		if(position[1] < i-1)
			moves.push([position[0] + 1, position[1]])

		return moves

	def path_search ( matrix, start, goal):

		heap = []
		heapq.heappush(heap,[0, start])

    	cost_so_far = [[-1 for x in range(len(matrix))] for x in range(len(matrix[0]))]
    	came_from = []
    	cost_so_far[start[0]][start[1]] = 0

    	while (True):
    		try:
    			current = heapq.heappop(heap)

    			if current[1] == goal:
    				break

    			for next in moves(matrix, current):
           			new_cost = cost_so_far[current[1][0]][current[1][1]] + current[0]
		            if  cost_so_far[next[0]][next[1]] == -1 or new_cost < cost_so_far[next[0]][next[1]]:
		                cost_so_far[next[0]][next[1]] = new_cost
		                priority = new_cost + heuristic(goal, next)
		                heapq.heappush(heap, [priority, next])
		                came_from.push(current)

    		except IndexError as inst:
    			break

    	return came_from, cost_so_far
