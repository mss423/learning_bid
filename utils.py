import numpy as np
import pandas as pd
import os, time, csv
import matplotlib.pyplot as plt
from numpy import random

def fn(bid,k,M):
	cost = bid ** k
	return np.minimum(cost,M)

def first_price(bids):
	'''
	FIRST PRICE AUCTION PAYOUTS
	Input: array of bids
	Output: winner index, incurred cost
	'''
	winner = np.max(bids)
	# print(winner)
	return winner

def second_price(bids):
	'''
	SECOND PRICE AUCTION PAYOUTS
	Input: array of bids
	Output: winner index, incurred cost
	'''
	winner = np.argmax(bids)
	bids = np.delete(bids, winner)
	cost = np.max(bids)
	return winner, cost

def get_bid(bid_history, cost_history, alg_budget, t, T, min_cost):
	'''
	Input: prior bid, history of spent amount, remaining budget,
		   current iteration and total time
	Output: bid for next time bucket from algorithm implementation
	'''
	rem_budget = alg_budget - np.sum(cost_history)

	if cost_history[-1] <= 0:
		r1 = bid_history[-1] / min_cost
	else:
		r1 = (bid_history[-1] / cost_history[-1])
	r2 = rem_budget / (T-t)
	if r2 <= 0:
		return 0
	return r1*r2

def get_bid_thresh(bid_history, cost_history, alg_budget, thresh, t, T, min_cost):
	'''
	Input: prior bid, history of spent amount, remaining budget,
		   current iteration and total time
	Output: bid for next time bucket from algorithm implementation
	'''
	if alg_budget > thresh:
		rem_budget = alg_budget - np.sum(cost_history)

		if cost_history[-1] <= 0:
			r1 = bid_history[-1] / min_cost
		else:
			r1 = (bid_history[-1] / cost_history[-1])
		r2 = rem_budget / (T-t)
		if r2 <= 0:
			return 0
		return r1*r2
	else:
		rem_budget = thresh - np.sum(cost_history)
		pseu = alg_budget - np.sum(cost_history)

		if cost_history[-1] <= 0:
			r1 = bid_history[-1] / min_cost
		else:
			r1 = (bid_history[-1] / cost_history[-1])
		r2 = rem_budget / (T-t)
		if pseu <= 0:
			return 0
		return r1*r2



