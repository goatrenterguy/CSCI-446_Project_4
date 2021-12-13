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
    '''
    for col in cols:
        for row in rows:
            #if not track.isWall((col, row)):
            #    startCells.append((col, row))
            for x_vel in speeds:
                for y_vel in speeds:
                    for action in actions:
                        if track.isFinish((col, row)):
                            qTable[((col, row), (x_vel, y_vel), action)] = 0
                        else:
                            qTable[((col, row), (x_vel, y_vel), action)] = -1'''
    makeTable(cols, rows, track)
    counter = 0
    startLine = False
    while counter <= iterations:
        if counter == iterations/10:
            epsilon = 0.1
        if counter == iterations/2:
            print("-------------------50%-----------------")
            learning_rate = 1
            startLine = True
            


        if startLine:
            pos = random.choice(track.startLine)
            vel = (0, 0)
            for mov in movesList:
                if mov in track.finishLine:
                    print(movesList)
        else:
            legal = False
            while not legal:
                pos = (random.choice(cols), random.choice(rows))
                vel = (random.choice(speeds), random.choice(speeds))
                if vel[0]+pos[0] in cols and vel[1]+pos[1] in rows:
                    legal = True

        done = False
        movesList = []
        movesList.append(pos)

        moves = 0


        while not done:
            statusOfMove, cell = track.checkTraversed(pos, (pos[0]+vel[0], pos[1]+vel[1]))
            moves += 1
            prevPos = pos
            prevVel = vel

            # First change the velocity
            inVel = False
            while not inVel:  # until you get a valid action
                # Select action using the epsilon-greedy method
                if random.random() < EPSILON:  # on p(EPSILON) select a random action
                    action = random.choice(actions)
                else:  # otherwise select the optimal action
                    action = optimal(pos, vel)
                newVel = (vel[0] + action[0], vel[1] + action[1])  # calculate new velocity
                if newVel[0] in speeds and newVel[1] in speeds:
                    if pos[0]+newVel[0] in cols and pos[1]+newVel[1] in rows: # check if the velocity is a legal speed
                        vel = newVel  # set new velocity
                        inVel = True

            newPos = (pos[0]+vel[0], pos[1]+vel[1])  # calculate the new position
            
            statusOfMove, cell = track.checkTraversed(pos, newPos)  # check if the move is possible
            if cell[0] <= max(cols) and cell[0] >= min(cols)  and cell[1] <= max(rows) and cell[1] >= min(rows):
                done = True
            if statusOfMove == -1:  # handle crashes
                if hardCrash:  # if hard crashes are enabled
                    pos = random.choice(track.startLine)  # move to the start
                    vel = (0, 0)  # set speed to zero
                else:
                    pos = cell  # move to the cell where the crash occured
                    vel = (0, 0)  # set speed to zero
                rewardValue = -1000
            elif statusOfMove == 1: # finish line crossed!
                pos = cell
                rewardValue = 0
                #print("FINISHED!")
            elif statusOfMove == 0: # the car did not crash
                pos = cell  # move the car
                if pos in track.startLine:
                    rewardValue = -100
                else:
                    rewardValue = -1
            movesList.append(pos)
            bestNext = optimal(pos, vel)
            if type(bestNext) == int:
                qTable[(prevPos, prevVel, action)] = bestNext
            else:
                qTable[(prevPos, prevVel, action)] = (1-learning_rate)*qTable[(prevPos, prevVel, action)] + \
                    learning_rate*(rewardValue+qTable[(pos, vel, bestNext)] - qTable[(prevPos, prevVel, action)])

            # break if the agent reaches the goal or hits max moves
            if rewardValue == 1 or moves > MAX_MOVES:
                counter += 1
                done = True
    print(optimal((1, 7), (0, 0)))
    policy = {}
    for cell in startCells:
        for vel_x in speeds:
            for vel_y in speeds:
                val = optimal(cell, (vel_x, vel_y))
                if type(val) != int:
                    policy[(cell, (vel_x, vel_y))] = val
    print(policy[((4, 7), (1, 1))])
    return policy


def optimal(pos, vel):
    maxVal = -10
    bestAct = ()
    for action in actions:
        #if not (vel == (0, 0) and action == (0, 0)):
        if qTable[(pos, vel, action)] > maxVal and not (vel == (0, 0) and action == (0, 0)):
            maxVal = qTable[(pos, vel, action)]
            bestAct = action
    return bestAct

def makeTable(cols, rows, track):
    for col in cols:
        for row in rows:
            startCells.append((col, row))
            for x_vel in speeds:
                for y_vel in speeds:
                    for action in actions:
                        if track.isFinish((col, row)):
                            qTable[((col, row), (x_vel, y_vel), action)] = 0
                        else:
                            qTable[((col, row), (x_vel, y_vel), action)] = -1