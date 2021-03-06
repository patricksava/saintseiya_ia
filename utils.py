__author__ = 'eric'

import itertools
import csv, os


def get_all_combinations(knights):

    combs = []
    knights_len = len(knights)

    for i in xrange(1, knights_len + 1):
        els = [list(x) for x in itertools.combinations(knights,i)]
        combs.extend(els)

    return combs


def get_houses():
    with open(os.path.normcase('config/houses.csv')) as houses_file:
        houses_gen = csv.DictReader(houses_file)
        houses = []
        houses_diff = []
        for house in houses_gen:
            houses.append(eval(house['difficulty']))
        houses.sort(None, None, True)
        #print houses
	return houses

def get_houses_full():
    with open(os.path.normcase('config/houses.csv')) as houses_file:
        houses_gen = csv.DictReader(houses_file)
        houses = []
        houses_diff = []
        for house in houses_gen:
            houses.append([house['sign'], eval(house['difficulty'])])
        #print houses
	return houses



def get_knights():
    with open('config/knights.csv') as knights_file:
    	knights_gen = csv.DictReader(knights_file)
	knights = []
	for knight in knights_gen:
	    knights.append([knight['knight-name'],eval(knight['cosmic-power']),eval(knight['lives'])])

        return knights


