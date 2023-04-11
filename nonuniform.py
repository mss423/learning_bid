# Learning Bid Simulations - Max Springer, October 2022

import numpy as np
import pandas as pd
import os, time, csv
import matplotlib.pyplot as plt
from numpy import random
from utils import *

alg_budget = 50000 # * bin_size # initialize somehow
T = 1000
bins = 10
divs = np.int32(T/bins)
ks = [0.5, 1.4, 2.3]
M = 100
# pacing = np.random.uniform()
pacing = np.sort(np.squeeze(np.random.dirichlet(np.ones(bins), size=1)))
ulim = 500
mults = np.ones(T)
for c1 in range(bins):
	for c2 in range(divs):
		idx = np.int32((divs)*c1 + c2)
		mults[idx] = pacing[c1]


for n in range(len(ks)):
	k = ks[n]
	# count = 0
	bid_hist = []
	cost_hist = [0]
	count = 0
	rem_budget = alg_budget
	for t in range(T):
		if t % (divs) == 0:
			cost_hist = [0]
			count = 0
		if count < 1:
			alg_bid = mults[t] * alg_budget / T
		else:
			alg_bid = get_bid(bid_hist, cost_hist, mults[t] * alg_budget, count, divs, 0.1)
		bid_hist = np.append(bid_hist, alg_bid)
		cost = fn(alg_bid, k, M)
		rem_budget = rem_budget - cost
		cost_hist = np.append(cost_hist, cost)
		count = count + 1

	plt.title("Bids")
	plt.plot(range(T), bid_hist)
	plt.xlim([1,ulim])
	plt.ylim([0,np.max(bid_hist[:ulim])])
	# ax1.set_ylim([0,np.max(bid_hist)])
	plt.xlabel('Time')
	plt.ylabel('Bid Value')
	# plt.yticks([])
	plt.show()

