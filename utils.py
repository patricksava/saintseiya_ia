__author__ = 'eric'

import itertools
import csv

def get_all_combinations(knights):

    combs = []
    knights_len = len(knights)

    for i in xrange(1, knights_len + 1):
        els = [list(x) for x in itertools.combinations(knights,i)]
        combs.extend(els)

    return combs


def get_houses():
    with open('config/houses.csv') as houses_file:
        houses_gen = csv.DictReader(houses_file)
        houses = []
        houses_diff = []
        for house in houses_gen:
            houses.append(house)

	return houses


def get_knights():
    with open('config/knights.csv') as knights_file:
    	knights_gen = csv.DictReader(knights_file)
	knights = []
	for knight in knights_gen:
	    knights.append(knight)

        return knights
