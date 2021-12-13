import copy
from math import inf
from warnings import catch_warnings
from raceTrack import RaceTrack
import random

# CONSTANTS
MAX_MOVES = 20
MAX_VELOCITY = 5
MIN_VELOCITY = -5
EPSILON = 0.1

speeds = range(-5, 6)
actions = [(-1, -1), (0, -1), (1, -1), (-1, 0), (0, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
qTable = {}
startCells = []


def qLearning(track: RaceTrack, hardCrash: bool, iterations):
    learning_rate = 0.9
    epsilon = 0.3
    cols = range(len(track.track[0]))
    rows = range(len(track.track))

    makeTable(cols, rows, track)
    counter = 0
    startLine = False
    while counter <= iterations:
        if counter == 0.75*iterations:
            print("-------------------75%-----------------")
            epsilon = 0.07
            learning_rate = 1
            madeIt = 0
            startLine = True

        if startLine:
            pos = random.choice(track.startLine)
            vel = (0, 0)
            #for mov in movesList:
            #    if mov in track.finishLine:
            #        madeIt += 1
            #        print(str(madeIt/(0.25*iterations))+"%")
        else:
            legal = False
            while not legal:
                pos = (random.choice(startCells))
                vel = (random.choice(speeds), random.choice(speeds))
                if vel[0]+pos[0] in cols and vel[1]+pos[1] in rows:
                    legal = True

        done = False
        movesList = []
        movesList.append(pos)

        moves = 0


        while not done:
            moves += 1
            prevPos = pos
            prevVel = vel

            # First change the velocity

            if moves == 0:
                pos = (pos[0]+vel[0], pos[1]+vel[1])
            else:
                inVel = False
                while not inVel:  # until you get a valid action
                    # Select action using the epsilon-greedy method
                    if random.random() < epsilon:  # on p(EPSILON) select a random action
                        action = random.choice(actions)
                    else:  # otherwise select the optimal action
                        action = optimal(pos, vel)
                    newVel = (vel[0] + action[0], vel[1] + action[1])  # calculate new velocity
                    if newVel[0] in speeds and newVel[1] in speeds:
                        vel = newVel  # set new velocity
                        inVel = True
                newPos = (pos[0]+vel[0], pos[1]+vel[1])  # calculate the new position
            
            stat, cell = track.checkTraversed(pos, newPos)
            if stat == -1:
                if hardCrash:  # if hard crashes are enabled
                    pos = random.choice(track.startLine)  # move to the start
                    vel = (0, 0)  # set speed to zero
                else:
                    pos = cell  # move to the cell where the crash occured
                    vel = (0, 0)  # set speed to zero
                rewardValue = -100
            elif stat == 1: # finish line crossed!
                rewardValue = 1
                pos = cell
                #print("FINISHED!")
            elif stat == 0: # the car did not crash
                pos = cell
                if newPos in track.startLine:
                    rewardValue = -10
                else:
                    rewardValue = -1
            movesList.append(pos)
            bestNext = optimal(pos, vel)
            qTable[(prevPos, prevVel, action)] = (1-learning_rate)*qTable[(prevPos, prevVel, action)] + \
                learning_rate*(rewardValue+0.5*(qTable[(pos, vel, bestNext)] - qTable[(prevPos, prevVel, action)]))

            # break if the agent reaches the goal or hits max moves
            if rewardValue == 0 or rewardValue == -100 or moves > 100:
                counter += 1
                done = True
    policy = {}
    for col in cols:
        for row in rows:
            for vel_x in speeds:
                for vel_y in speeds:
                    policy[((col, row), (vel_x, vel_y))] = optimal((col, row), (vel_x, vel_y))
    return policy


def optimal(pos, vel):
    maxVal = -inf
    bestAct = ()
    for act in actions:
        if qTable[(pos, vel, act)] > maxVal and not (vel == (0, 0) and act == (0, 0)):
            maxVal = qTable[(pos, vel, act)]
            bestAct = act
    return bestAct

def makeTable(cols, rows, track):
    for col in cols:
        for row in rows:
            if not track.isWall((col, row)):
                startCells.append((col, row))
            for x_vel in speeds:
                for y_vel in speeds:
                    for act in actions:
                        if track.isFinish((col, row)):
                            qTable[((col, row), (x_vel, y_vel), act)] = 0
                        else:
                            qTable[((col, row), (x_vel, y_vel), act)] = random.random()