from raceTrack import RaceTrack
import random
import numpy

# CONSTANTS
MAX_MOVES = 10
MAX_VELOCITY = 5
MIN_VELOCITY = -5
LEARNING_RATE = 0.1
EPSILON = 0.1

speeds = range(MIN_VELOCITY, MAX_VELOCITY + 1)
actions = [(-1, -1), (0, -1), (1, -1), (-1, 0), (0, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
qTable = []
cols = 0
rows = 0

def qLearning(track: RaceTrack, hardCrash: bool, iterations):
    moves = 0

    cols = range(len(track.track[0]))
    rows = range(len(track.track))
    startCells = []
    qTable = [[[[[0 for _ in actions] for _ in speeds] for _ in speeds] for _ in cols] for _ in rows]  # Initialize all values in Q-table to zero

    # gather all valid start states
    for col in range(len(cols)):
        for row in range(len(rows)):
            if track.track[row][col] == "." or track.track[row][col] == "S":
                startCells.append((col,row))
    
    while moves <= iterations:
        startCol, startRow = random.choice(startCells)
        startX_vel = random.choice(speeds)
        startY_vel = random.choice(speeds)
        pos = (startCol, startRow)
        vel = (startX_vel, startY_vel)
        
        done = False
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
                    actionIndex = numpy.argmax(qTable[pos[1]][pos[0]][vel[0]][vel[1]])
                    action = actions[actionIndex]
                newVel = (vel[0] + action[0], vel[1] + action[1])  # calculate new velocity
                # check if the velocity is a legal speed
                if newVel[0] in speeds and newVel[1] in speeds:
                    vel = newVel  # set new velocity
                    inVel = True
            
            # Move the car
            newPos = (pos[0]+vel[0], pos[1]+vel[1])  # calculate the new position
            statusOfMove, cell = track.checkTraversed(pos, newPos)  # check if the move is possible
            if statusOfMove == -1:  # handle crashes
                if hardCrash:  # if hard crashes are enabled
                    pos = random.choice(track.startLine)  # move to the start
                    vel = (0, 0)  # set speed to zero
                    done = True
                else:
                    pos = cell  # move to the cell where the crash occured
                    vel = (0, 0)  # set speed to zero
            else:  # the car did not crash
                pos = cell  # move the car
            
            # CALCULATE Q VALUE ------------> ok I'm 50/50 this is the proper formula
            rewardValue = reward(track.track[pos[1]][pos[0]])
            bestNextActionIndex = numpy.argmax(qTable[pos[1]][pos[0]][vel[0]][vel[1]])
            qTable[prevPos[1]][prevPos[0]][prevVel[0]][prevVel[1]][actionIndex] = qTable[prevPos[1]][prevPos[0]][prevVel[0]][prevVel[1]][actionIndex]+LEARNING_RATE*(rewardValue+0.5*(qTable[pos[1]][pos[0]][vel[0]][vel[1]][bestNextActionIndex]-qTable[prevPos[1]][prevPos[0]][prevVel[0]][prevVel[1]][actionIndex]))
            
            # break if the agent reaches the goal or hits max moves
            if reward == 0 or moves > MAX_MOVES:
                done = True
                    
    # After iterations we need to get the policy from the Q table
    policy = {} # initialize the policy
    # Iterate over each possible state
    for col in range(len(track.track[0])):
        for row in range(len(track.track)):
            for vel_x in speeds:
                for vel_y in speeds:
                    # Select the best action from the current state and add it to the policy
                    policy[(col, row, vel_x, vel_y)] = actions[numpy.argmax(qTable[row][col][vel_x][vel_y])]
    return policy # Return the optimal policy
            

def reward(state):
    if state == 'F':
        return 0
    elif state == 'S' or state == '.':
        return -1
    else:
        return -10