#!/usr/bin/env python3
import pickle
import matplotlib.pyplot as plt


X = pickle.load(open("cmass_timeseries.p", "rb"))

twoPoseEntries = [*filter(lambda x : len(x[1]) == 2, X)]



relXDistance = [(x[0], abs(x[1][0][0] - x[1][1][0])) for x in twoPoseEntries]

print(relXDistance)
x, y = list(zip(*relXDistance))
plt.plot([t/1000 for t in x ], y)
plt.show()
