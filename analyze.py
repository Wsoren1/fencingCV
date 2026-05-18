#!/usr/bin/env python3
import pickle
import matplotlib.pyplot as plt
import sys

def positions(runDir, X):
    plt.clf()
    twoPoseEntries = [*filter(lambda x : len(x[1]) == 2, X)]
    t =  [x[0]/1000 for x in twoPoseEntries]
    y1 = [x[1][0][0] for x in twoPoseEntries]
    y2 = [x[1][1][0] for x in twoPoseEntries]

    left_pos = [min(a, b) for a, b in zip(y1, y2)]
    right_pos = [max(a, b) for a, b in zip(y1, y2)]

    plt.plot(t, left_pos, label='FOTL')
    plt.plot(t, right_pos, label='FOTR')

    plt.legend()

    plt.savefig(f'{runDir}/twofencerpos.png', dpi=300)
    pickle.dump((t, left_pos, right_pos),
                open(f'{runDir}/twofencerposdata.p', 'wb'))

def relative_distances(runDir, X):
    plt.clf()
    twoPoseEntries = [*filter(lambda x : len(x[1]) == 2, X)]

    relXDistance = [(x[0], abs(x[1][0][0] - x[1][1][0])) for x in twoPoseEntries]

    x, y = list(zip(*relXDistance))
    plt.plot([t/1000 for t in x ], y)
    plt.savefig(f'{runDir}/distance.png', dpi=300)

def main(runDir, fromScript):
    X = pickle.load(open(f"{runDir}/cmass_timeseries.p", "rb"))

    relative_distances(runDir, X)

    positions(runDir, X)
    if not fromScript:
        plt.show()



if __name__ == "__main__":
    fromScript = len(sys.argv) == 3
    main(sys.argv[1], fromScript)
