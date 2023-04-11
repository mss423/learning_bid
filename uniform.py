# Learning Bid Simulations - Max Springer, October 2022

import numpy as np
import pandas as pd
import os, time, csv
import matplotlib.pyplot as plt
from numpy import random
from utils import *

alg_budget = 50000 # * bin_size # initialize somehow
T = 1000
ks = [0.5, 1.4, 2.3]
# ulims = [5000, 16.34 * 2, 5.5 * 2]
ulim = 500
M = 100

for n in range(len(ks)):
	k = ks[n]
	# ulim = ulims[n]
	count = 0
	bid_hist = []
	cost_hist = [0]
	for t in range(T):
		if count < 1:
			alg_bid = alg_budget / T
		else:
			alg_bid = get_bid(bid_hist, cost_hist, alg_budget, count, T, 0.1)
		bid_hist = np.append(bid_hist, alg_bid)
		cost = fn(alg_bid, k, M)
		cost_hist = np.append(cost_hist, cost)
		count = count + 1

	# Bifurcation analysis plotting:
	dsp       = lambda x: x**k
	stab_line = lambda x: x
	first_it  = lambda x: x * ((alg_budget - np.minimum(dsp(x),M)) / (np.minimum(dsp(x),M) * T))
	second_it = lambda x: first_it(x) * ((alg_budget - np.minimum(dsp(x),M) - np.minimum(dsp(first_it(x)),M)) / ((T - 1) * (np.minimum(dsp(first_it(x)), M))))

	plt.title("Bids")
	plt.plot(range(T), bid_hist)
	plt.xlim([1,ulim])
	plt.ylim([0,np.max(bid_hist[:ulim])*1.5])
	# ax1.set_ylim([0,np.max(bid_hist)])
	plt.xlabel('Time')
	plt.ylabel('Bid Value')
	# plt.yticks([])
	plt.show()

	'''
	inp = np.linspace(0.01,ulim,1000)
	fig, (ax1, ax2) = plt.subplots(1,2, figsize=(20,8))
	ax1.set_title("Bids")
	ax1.plot(range(T), bid_hist)
	ax1.set_xlim([0,100])
	ax1.set(xlabel='Time', ylabel='Bid Value')
	# ax1.xlabel('Time')
	# ax1.ylabel('Bid Value')
	# plt.show()

	ax2.set_title("Cobweb Diagram")
	ax2.plot(inp, stab_line(inp))
	ax2.plot(inp, first_it(inp))
	ax2.plot(inp, second_it(inp))
	ax2.legend((r'$y=x$',r'$f(x_n)$',r'$f(f(x_n))$'), loc='lower right')
	ax2.set(xlabel=r'$x_n$',ylabel=r'$x_{n+1}$')
	ax2.set_xlim([0,ulim])
	ax2.set_ylim([0,ulim])
	# plt.show()

	plt.show()
	'''
