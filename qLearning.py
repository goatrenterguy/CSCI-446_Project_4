from math import inf
from raceTrack import RaceTrack
import random

# Global variables
speeds = range(-5, 6)
actions = [(-1, -1), (0, -1), (1, -1), (-1, 0), (0, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
qTable = {}
startCells = []


def qLearning(track: RaceTrack, hardCrash: bool, iterations):
    learning_rate = 0.9 # The learning rate at which new information will replace old
    epsilon = 0.5 # The chance that a random action is chosen rather than the optimal
    cols = range(len(track.track[0]))
    rows = range(len(track.track))

    makeTable(cols, rows, track) # Populate the qTable
    counter = 0 # Counter to check iterations

    # Loop for the total number of iterations given
    while counter <= iterations:
        if counter % (iterations*0.1) == 0: # Every time the counter reaches a tenth of the counter
            learning_rate = learning_rate*0.8 # Decrement the learning rate so values persist more
            epsilon = epsilon*0.8 # Decrement epsilon so that random actions are taken less

        # Find a position and velocity that it within the confines of the board
        legal = False
        while not legal:
            pos = (random.choice(startCells))
            vel = (random.choice(speeds), random.choice(speeds))
            if vel[0]+pos[0] in cols and vel[1]+pos[1] in rows:
                legal = True

        # Reset variables for the loop that represetnts this iteration
        done = False
        moves = 0
        crashes = 0
        while not done:
            moves += 1
            prevPos = pos # Make pos and vel ready to change
            prevVel = vel

            # First change the velocity
            if moves == 0:
                pos = (pos[0]+vel[0], pos[1]+vel[1])
            else:
                inVel = False
                while not inVel:  # Until a velocity is valid
                    if random.random() < epsilon:  # On epsilon select a random action
                        action = random.choice(actions)
                    else:
                        action = optimal(pos, vel) # Otherwise select the optimal action
                    newVel = (vel[0] + action[0], vel[1] + action[1]) # Calculate and check legality of new velocity
                    if newVel[0] in speeds and newVel[1] in speeds:
                        vel = newVel  # Set new velocity
                        inVel = True
                newPos = (pos[0]+vel[0], pos[1]+vel[1])  # Calculate the new position
            stat, cell = track.checkTraversed(pos, newPos) # Find the passed through cells and get status
            if stat == -1:
                if hardCrash:  # Handle hard crashes
                    pos = random.choice(track.startLine)
                    vel = (0, 0)
                else: # Handle mild crashes
                    pos = cell
                    vel = (0, 0)
                rewardValue = -100 # Set a very low reward
                crashes += 1
            elif stat == 1: # Crossed finish line, set reward high
                rewardValue = 100
                pos = cell
            elif stat == 0: # Car did not crash
                pos = cell
                if newPos in track.startLine: # We want to motivate it away from the starting line
                    rewardValue = -20 # So we give it a low reward
                else:
                    rewardValue = 1 # Otherwise it is a blank space, set a small but positive value
            bestNext = optimal(pos, vel) # Find the optimal action for our new position and velocity
            # And use the Bellman algorithm to obtain a value for the action compared to the previous state
            qTable[(prevPos, prevVel, action)] = (1-learning_rate)*qTable[(prevPos, prevVel, action)] + \
                learning_rate*(rewardValue+0.99*(qTable[(pos, vel, bestNext)] - qTable[(prevPos, prevVel, action)]))

            # Break when we find a goal state
            if rewardValue == 100:
                counter += 1
                done = True

    # Create the policy by iterating through all states and selecting the optimal action
    policy = {}
    for col in cols:
        for row in rows:
            for vel_x in speeds:
                for vel_y in speeds:
                    policy[((col, row), (vel_x, vel_y))] = optimal((col, row), (vel_x, vel_y))
    return policy


# Iterate through the actions in a state and find the highest valued one
def optimal(pos, vel):
    maxVal = -inf
    bestAct = ()
    for act in actions:
        if qTable[(pos, vel, act)] > maxVal and not (vel == (0, 0) and act == (0, 0)):
            maxVal = qTable[(pos, vel, act)]
            bestAct = act
    return bestAct

# Populate the values in the table, if it is a finish line with a 0, and otherwise with a random value
def makeTable(cols, rows, track):
    for col in cols:
        for row in rows:
            if not track.isWall((col, row)):
                startCells.append((col, row))
            for x_vel in speeds:
                for y_vel in speeds:
                    for act in actions:
                        if track.isFinish((col, row)):
                            qTable[((col, row), (x_vel, y_vel), act)] = 1
                        else:
                            qTable[((col, row), (x_vel, y_vel), act)] = random.random()