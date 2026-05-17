#!/usr/bin/env python3
import pickle
import matplotlib.pyplot as plt
import sys

def main(runDir):

    X = pickle.load(open(f"{runDir}/cmass_timeseries.p", "rb"))

    twoPoseEntries = [*filter(lambda x : len(x[1]) == 2, X)]



    relXDistance = [(x[0], abs(x[1][0][0] - x[1][1][0])) for x in twoPoseEntries]


    x, y = list(zip(*relXDistance))
    plt.plot([t/1000 for t in x ], y)
    plt.savefig(f'{runDir}/figure.png', dpi=300)

if __name__ == "__main__":
    main(sys.argv[1])
