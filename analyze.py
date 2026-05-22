#!/usr/bin/env python3
import pickle
import matplotlib.pyplot as plt
import sys
import numpy as np

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


def three_point_angle(a, b, c):
    A = np.array(a)
    B = np.array(b)
    C = np.array(c)

    ba = A - B
    bc = C - B

    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    return np.arccos(cosine_angle)

def extensions(runDir, X):
    plt.clf()

    times = []
    extended_left = []
    extended_right = []
    
    for i, entry in enumerate(X):
        if len(entry[1]) < 2:
            continue
        
        t = entry[0]
        fencer_1 = entry[1][0]
        fencer_2 = entry[1][1]
        
        fencer_1_a = [fencer_1[i] for i in (12, 14, 16)]
        fencer_1_b = [fencer_1[i] for i in (11, 13, 15)]
        
        fencer_2_a = [fencer_2[i] for i in (12, 14, 16)]
        fencer_2_b = [fencer_2[i] for i in (11, 13, 15)]

        
        points_map = {pointset[0][0] + pointset[1][0] + pointset[2][0] :pointset for pointset in [fencer_1_a, fencer_1_b, fencer_2_a, fencer_2_b]}

        sorted_mapping = sorted(points_map)
        left_fencer_arm = points_map[sorted_mapping[1]]
        right_fencer_arm = points_map[sorted_mapping[2]]

        grounded_left_arm = [(left_fencer_arm[0][0], 0), left_fencer_arm[0], left_fencer_arm[2]]
        grounded_right_arm = [(right_fencer_arm[0][0], 0), right_fencer_arm[0], right_fencer_arm[2]]

        arm_straightness_left = np.sin(0.5 * three_point_angle(*left_fencer_arm))**6
        arm_straightness_right = np.sin(0.5 * three_point_angle(*right_fencer_arm))**6
        
        times.append(t/1000)
        arm_parallelness_left =  np.sin(0.5 * three_point_angle(*grounded_left_arm) + np.pi/4)**6
        arm_parallelness_right = np.sin(0.5 * three_point_angle(*grounded_right_arm) + np.pi/4 )**6

        extended_left.append(arm_straightness_left * arm_parallelness_left)
        extended_right.append(arm_straightness_right * arm_parallelness_right)

    extended_left = np.convolve(extended_left, [1/7] * 7, mode='same')
    extended_right = np.convolve(extended_right, [1/7] * 7, mode='same')
   
    pickle.dump((times, extended_left, extended_right),
                open(f'{runDir}/extensiondata.p', 'wb'))
    plt.plot(times, extended_left, label='FOTL')
    plt.plot(times, extended_right, label='FOTR')
    plt.legend()
    
        
        

        

    
        # get parallel angle by just grabbing the 12 or 11 and setting y to 0, then use that point
        # 12 and 16 for the angle, 12 being the midpoint
    
        # 1 = arm at 180 degrees * arm is parallel to ground


def main(runDir, fromScript):
    X = pickle.load(open(f"{runDir}/cmass_timeseries.p", "rb"))

    relative_distances(runDir, X)

    positions(runDir, X)
    X = pickle.load(open(f"{runDir}/save.p", "rb"))
    extensions(runDir, X)
    if not fromScript:
        plt.show()

    

if __name__ == "__main__":
    fromScript = len(sys.argv) == 3
    main(sys.argv[1], fromScript)
