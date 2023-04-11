# Learning Bid Simulations - Max Springer, October 2022

import numpy as np
import pandas as pd
import os, time, csv
import matplotlib.pyplot as plt
from numpy import random
from utils import *

def bid_dynamics(budget=50000, T=1000, k=1.5):
	bid_hist  = []
	cost_hist = [0]
	max_cost  = 100
	min_cost  = 0.1

	for t in range(T):
		if t == 0:
			alg_bid = np.random.rand() * budget / T
		else:
			alg_bid = get_bid(bid_hist, cost_hist, budget, t, T, min_cost)
		bid_hist = np.append(bid_hist, alg_bid)
		cost_hist = np.append(cost_hist, fn(alg_bid, k, max_cost))
		# budget = budget - cost_hist[-1]
	plt.title("Bid Dynamics for k = %s" % k)
	plt.plot(range(T), bid_hist)
	plt.show()

def auction_sim(min_cost=0.1):
	data_dir = '/Users/maxspringer/Documents/GitHub/learning_bid/Data/rtb_video/'
	d = pd.read_csv(os.path.join(data_dir, "ad_bid_data.txt"), sep="\t", header=None)

	min_cost = 0.1
	sel_ad = np.squeeze(d[:][1].mode())
	ads_info = np.array(d[:][1])
	d_sel = np.argwhere(ads_info == sel_ad)
	sel_idx = np.squeeze(np.argwhere(ads_info == sel_ad))

	d_sel = d.loc[sel_idx]
	max_cost = np.max(d_sel[3])
	d_sel[0] = pd.to_datetime(d_sel[0])
	dtimes = np.array(d_sel[:][0])
	times = np.array(d_sel[:][0].unique())
	bid_hist = []
	cost_hist = [0]
	alg_budget = len(times) / 4 # * bin_size # initialize somehow

	count = 0
	for t in times:
		t_idx = np.squeeze(np.argwhere(dtimes == t))
		t_bids = d_sel.iloc[t_idx][3] # Get set of bids on impression for current time
		if count == 0:
			alg_bid = np.random.rand() * alg_budget / len(times)
		else:
			alg_bid = get_bid(bid_hist, cost_hist, alg_budget, count, len(times), min_cost)
		bid_hist = np.append(bid_hist, alg_bid)
		winner = first_price(np.append(t_bids,alg_bid))
		count = count + 1
		if winner == alg_bid: # if algorithm wins
			alg_budget = alg_budget - np.min([alg_bid, max_cost])
			cost_hist = np.append(cost_hist, alg_bid)
		else:
			cost_hist = np.append(cost_hist, 0)

	budget_time = np.cumsum(cost_hist) / alg_budget
	plt.title("Bids")
	plt.plot(range(len(times)), bid_hist)
	plt.show()

	plt.title("Portion of Budget Spent")
	plt.plot(range(len(times)+1), budget_time)
	plt.show()

if __name__ == "__main__":
	bid_dynamics()
	auction_sim()








