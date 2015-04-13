__author__ = 'egrinstein, psava, mbvaz'

"adapted from http://dave.dkjones.org/posts/2012/2012-03-12-astar-python.html"

import utils
import heapq, math

class State(object):
    """Represents the knights alive and the house they're in """
    knights_left = utils.get_knights()


    def __init__(self, knights_used, house_no, knights_left):
        self.house_no = house_no
        self.knights_used = knights_used
	self.knights_left = knights_left
        self.cosmic_power_used = 0

        


    def __hash__(self):
        return hash((self.house_no, self.knights_left))

    def __repr__(self):
        return "%d knights used on house %d" % (len(self.knights_used), self.house_no)

    def __eq__(self, other):
        return self.total_cosmic_power == other.total_cosmic_power and self.house_no == other.house_no

    def get_moves(self):
        "Gets next possible combination of knights in the next house"

        combs = utils.get_all_combinations(self.knights_left)

        for comb in combs:
            yield State(comb, house_no+1)




def heuristic( initial_time , current_time)
    for knight in self.knights_used:
         total_cosmic_power += knight['cosmic-power']
    return initial_time - current_time




def build_path(start, finish, parent):
    """Reconstruct the path from start to finish given a dict of parent links. """
    x = finish
    xs = [x]
    while x != start:
        x = parent[x]
        xs.append(x)
    xs.reverse()
    return xs



def get_fighting_plan(heuristic):
    """Find the shortest time from house 1 to house 12."""

    knights = get_knights()
    houses_to_beat = get_houses()
    max_time = 0
    for house in houses:
        max_time += house[difficulty]
    total_houses = len(houses_to_beat)

    initial_state = State(knights,1)

    heap = []

    link = {} # parent node link
    h = {} # heuristic function cache
    g = {} # shortest path to a node

    g[initial_state] = 0
    h[initial_state] = 0
    link[initial_state] = None


    heapq.heappush(heap, (0, 0, initial_state))
    # keep a count of the  number of steps, and avoid an infinite loop.
    for kk in xrange(1000000):
        f, junk, current = heapq.heappop(heap)
        if current.house_no > total_houses:  # cuidado para não parar sem lutar na casa 12,etc
            print "time:", g[current]
            return g[current], build_path(start, finish, link)

        moves = current.get_moves()
        distance = g[current]
        for mv in moves:
            if mv not in g or g[mv] > distance + 1:
                g[mv] = distance + 1
                if mv not in h:
                    h[mv] = heuristic(mv)
                link[mv] = current
                heapq.heappush(heap, (g[mv] + h[mv], -kk, mv))

