import random

from raceTrack import RaceTrack


class MDP:
    def __init__(self, discountFactor=.8, debug=False):
        self.discountFactor = discountFactor
        self.debug = debug
        self.states = []
        self.rewards = {}
        self.transitions = {}
        self.terminals = []

    def T(self, state, action):
        """
        Get the array of possible states given an action
        :param state: State in
        :param action: Action to take
        :return: Array of possible end states
        """
        return self.transitions[state][action]

    def R(self, state):
        """
        Get the reward of a state
        :param state: A state
        :return: The reward of the state
        """
        return self.rewards[state]

    def A(self, state):
        """
        Returns all actions for a state
        :rtype: list of all possible actions
        """
        return self.transitions[state]

    def makeMDPFromTrack(self, rt: RaceTrack, hardCrash=False):
        """
        Function to take in a RaceTrack and create an MDP for it
        :param rt: RaceTrack Object
        :param hardCrash: The type of crash being used
        """
        actions = [-1, 0, 1]
        # Generate all states based on track
        self.makeStatesForMDP(rt.track)
        # Generate all rewards for each state
        self.makeRewardsForMDP(rt.track)
        # Iterate through all states
        for state in self.states:
            action = {}
            # Iterate though all possible combinations of actions
            for actionY in actions:
                for actionX in actions:
                    # Change velocity based on action. Velocity must be between -5 and 5
                    velocityX = state[1][0] + actionX
                    if abs(velocityX) > 5:
                        velocityX = state[1][0]
                    velocityY = state[1][1] + actionY
                    if abs(velocityY) > 5:
                        velocityY = state[1][1]
                    # The new position based on action and state
                    sToSPrimeX = state[0][0] + velocityX
                    sToSPrimeY = state[0][1] + velocityY
                    endStates = []
                    # Try the action
                    status, cell = rt.checkTraversed(state[0], (sToSPrimeX, sToSPrimeY))
                    # If crash is hard
                    if hardCrash:
                        # If action causes crash
                        if status == -1:
                            endStates.append((.8, (random.choice(rt.startLine), (0, 0))))
                        # If action hits finish line
                        elif status == 1:
                            endStates.append((.8, (cell, (0, 0))))
                        # If it doesnt crash or pass finish line
                        else:
                            endStates.append((.8, ((sToSPrimeX, sToSPrimeY), (velocityX, velocityY))))
                        # Check car path if action failed
                        status, cell = rt.checkTraversed(state[0], (state[0][0] + state[1][0], state[0][1] + state[1][1]))
                        # If car crashes
                        if status == -1:
                            endStates.append((.2, (random.choice(rt.startLine), (0, 0))))
                        # If car passes finish
                        elif status == 1:
                            endStates.append((.2, (cell, (0, 0))))
                        # If its just moved
                        else:
                            endStates.append((.2, (cell, state[1])))
                    # If mild crash is being used
                    else:
                        # If action causes car to pass finish line or crash
                        if status == -1 or status == 1:
                            endStates.append((.8, (cell, (0, 0))))
                        # Otherwise
                        else:
                            endStates.append((.8, ((sToSPrimeX, sToSPrimeY), (velocityX, velocityY))))
                        # If action failed
                        status, cell = rt.checkTraversed(state[0], (state[0][0] + state[1][0], state[0][1] + state[1][1]))
                        # If action causes car to pass finish line or crash
                        if status == -1 or status == 1:
                            endStates.append((.2, (cell, (0, 0))))
                        # Otherwise
                        else:
                            endStates.append((.2, (cell, state[1])))
                    # Add possible end state to action
                    action[(actionX, actionY)] = endStates
            # Add transitions for all states
            self.transitions[state] = action

    def makeRewardsForMDP(self, track):
        """
        Function to get rewards for each state
        :param track: 2D-array of a track
        """
        # Iterate through states
        for state in self.states:
            # If it crosses finish line reward is 0
            if track[state[0][1]][state[0][0]] == 'F':
                self.terminals.append((state[0][0], state[0][1]))
                self.rewards[state] = 0
            # If it is start or open reward is -1
            elif track[state[0][1]][state[0][0]] == '.' or track[state[0][1]][state[0][0]] == 'S':
                self.rewards[state] = -1
            # If it is a wall we dont want the car to hit it so we sent the penalty to -10
            else:
                self.rewards[state] = -10

    def makeStatesForMDP(self, track):
        """
        Function to get all states from a track
        :param track: 2D-array for a track
        """
        for y in range(len(track)):
            for x in range(len(track[0])):
                if track[y][x] != '#':
                    for yVelocity in range(-5, 6):
                        for xVelocity in range(-5, 6):
                            self.states.append(((x, y), (xVelocity, yVelocity)))
