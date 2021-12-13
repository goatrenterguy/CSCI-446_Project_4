import copy
from raceTrack import RaceTrack
import random
import numpy

# CONSTANTS
MAX_MOVES = 20
MAX_VELOCITY = 5
MIN_VELOCITY = -5

EPSILON = 0.1

speeds = range(MIN_VELOCITY, MAX_VELOCITY + 1)
actions = [(-1, -1), (0, -1), (1, -1), (-1, 0), (0, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
qTable = []
startCells = []
cols = 0
rows = 0

def qLearning(track: RaceTrack, hardCrash: bool, iterations):
    
    learning_rate = 1
    cols = range(len(track.track[0]))
    rows = range(len(track.track))
    
    qTable = [[[[[random.random() for _ in actions] for _ in speeds] for _ in speeds] for _ in rows] for _ in cols]  # Initialize all values in Q-table to zero

    for cell in track.finishLine:
        for x_vel in speeds:
            for y_vel in speeds:
                for act in range(len(actions)):
                    qTable[cell[0]][cell[1]][x_vel][y_vel][act] = 0

    # gather all valid start states
    for col in cols:
        for row in rows:
            if not track.isWall((col, row)) and (col, row) not in track.startLine:
                startCells.append((col, row))
    madeIt = 0
    times = 1
    counter = 0
    startLine = False
    startLineCells = track.startLine
    while counter <= iterations:
        if counter == iterations/4:
            print("-------------------25%-----------------")
        elif counter == iterations/2:
            print("-------------------50%-----------------")
        elif counter == 3*(iterations/4):
            print("-------------------75%-----------------")
            startLine = True


        if startLine:
            pos = random.choice(startLineCells)
            vel = (0, 0)
            for mov in movesList:
                if mov in track.finishLine:
                    madeIt += 1
                    print(str(madeIt/times)+"%")
            times += 1
        else:
            pos = random.choice(startCells)
            vel = (random.choice(speeds), random.choice(speeds))

        
        done = False
        movesList = []
        movesList.append(pos)
        counter += 1
        moves = 0

        while not done:
            moves += 1
            prevPos = pos
            prevVel = vel

            # First change the velocity
            inVel = False
            while not inVel:  # until you get a valid action
                # Select action using the epsilon-greedy method
                if random.random() < EPSILON:  # on p(EPSILON) select a random action
                    actionIndex = random.choice(range(9))
                    action = actions[actionIndex]
                else:  # otherwise select the optimal action
                    actionIndex = indexOfOptimal(qTable[pos[0]][pos[1]][vel[0]+5][vel[1]+5], vel[0]+5, vel[1]+5)
                    action = actions[actionIndex]
                newVel = (vel[0] + action[0], vel[1] + action[1])  # calculate new velocity
                if newVel[0] <= 5 and newVel[0] >= -5 and newVel[1] <= 5 and newVel[1] >= -5: # check if the velocity is a legal speed
                    vel = newVel  # set new velocity
                    inVel = True
            
            # Move the car
            
            newPos = (pos[0]+vel[0], pos[1]+vel[1])  # calculate the new position
            statusOfMove, cell = track.checkTraversed(pos, newPos)  # check if the move is possible
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
            elif statusOfMove == 0: # the car did not crash
                pos = cell  # move the car
                if pos in track.startLine:
                    rewardValue = -100
                else:
                    rewardValue = -1
            movesList.append(pos)
            #rewardValue -= len(movesList)
            
            bestNextActionIndex = indexOfOptimal(qTable[pos[0]][pos[1]][vel[0]+5][vel[1]+5], vel[0]+5, vel[1]+5)
            qTable[prevPos[0]][prevPos[1]][prevVel[0]+5][prevVel[1]+5][actionIndex] = (1 - learning_rate) * \
                    qTable[prevPos[0]][prevPos[1]][prevVel[0]+5][prevVel[1]+5][actionIndex] + learning_rate * \
                        (rewardValue+1*(qTable[pos[0]][pos[1]][vel[0]+5][vel[1]+5][bestNextActionIndex] - \
                            qTable[prevPos[0]][prevPos[1]][prevVel[0]+5][prevVel[1]+5][actionIndex]))
            # break if the agent reaches the goal or hits max moves
            #if rewardValue == 0:
            #    print(movesList)
            if rewardValue == 0 or moves > MAX_MOVES:
                counter += 1
                done = True
    print(indexOfOptimal(qTable[1][7][0][0], 0, 0))
    # After iterations we need to get the policy from the Q table
    policy = {} # initialize the policy
    # Iterate over each possible state
    for cell in startCells:
        for vel_x in speeds:
            for vel_y in speeds:
                policy[(cell, (vel_x, vel_y))] = actions[indexOfOptimal(qTable[cell[0]][cell[1]][vel_x][vel_y], vel_x, vel_y)]
                #if cell in startLineCells:
                #    print(indexOfOptimal(qTable[cell[0]][cell[1]][vel_x][vel_y], vel_x, vel_y))
    #print(policy.keys())
    print(policy.get((2, 8, 1, 1)))
    #for col in range(len(track.track[0])):
    #    for row in range(len(track.track)):
    #        for vel_x in speeds:
    #            for vel_y in speeds:
    #                # Select the best action from the current state and add it to the policy
    #                policy[(col, row, vel_x, vel_y)] = actions[indexOfOptimal(qTable[col][row][vel_x][vel_y], vel_x, vel_y)]
    return policy # Return the optimal policy
            

def reward(state):
    if state == 'F':
        return 0
    elif state == "#":
        return -100
    else:
        return -10

def indexOfOptimal(acts, vel_x, vel_y):
    index = 0
    maxVal = -100
    for i in range(len(acts)):
        if not (vel_x == 0 and vel_y == 0 and actions[i] == (0, 0)):
            if acts[i] > maxVal:
                maxVal = acts[i]
                index = i
    return index
    