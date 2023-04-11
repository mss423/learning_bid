# Learning Bid Simulations - Max Springer, October 2022

import numpy as np
import pandas as pd
import os, time, csv
import matplotlib.pyplot as plt
from numpy import random
from utils import *

alg_budget = 50000 # * bin_size # initialize somehow
thresh_budget = 75000
T = 1000
ks = [0.5, 1.4, 2.3]
ulims = [5000, 16.34 * 2, 5.5 * 2]
M = 100

for n in range(len(ks)):
	k = ks[n]
	ulim = ulims[n]
	count = 0
	bid_hist = []
	cost_hist = [0]
	for t in range(T):
		if count < 1:
			alg_bid = alg_budget / T
		else:
			alg_bid = get_bid_thresh(bid_hist, cost_hist, alg_budget, thresh_budget, count, T, 0.1)
		bid_hist = np.append(bid_hist, alg_bid)
		cost = fn(alg_bid, k, M)
		cost_hist = np.append(cost_hist, cost)
		count = count + 1

	# plt.set_title("Bids")
	plt.plot(range(T), bid_hist)
	plt.xlim([0,999])
	plt.xlabel('Time')
	plt.ylabel('Bid Value')

	plt.show()
