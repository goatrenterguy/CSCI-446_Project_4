import copy

from raceTrack import RaceTrack
from markovDecisionProcess import MDP
from valueIteration import valueIteration
from qLearning import qLearning
import random


class Agent:
    def __init__(self, track: RaceTrack, hardCrash: bool = False, debug: bool = False):
        """
        Initializes an agent onto a race tracks starting line
        :param track: A race track of type  RaceTrack
        :param hardCrash: Optional Parameter for changing the crash type
        """
        random.seed(1)
        self.debug = debug
        self.actions = 0
        self.track = track
        self.position = random.choice(track.startLine)
        self.prevPosition = self.position
        self.hardCrash = hardCrash
        self.velocity = (0, 0)

    def printBoard(self):
        """
        Function for printing the track and where the agent currently is
        """
        board = copy.deepcopy(self.track.track)
        board[self.position[1]][self.position[0]] = "C"
        out = "Board:\n"
        for x in board:
            out += str(x) + "\n"
        print(out)

    def fastestPathValueIteration(self):
        """
        Function for finding the fastest path to the finish line using value iteration
        :return: Array of the path taken
        """
        mdp = MDP()
        mdp.makeMDPFromTrack(self.track, self.hardCrash)
        utilities = valueIteration(mdp)
        path = []
        actionsTaken = []
        while not self.track.isFinish(self.position):
            actions = mdp.A((self.position, self.velocity))
            utilitiesPerAction = {}
            for action in actions:
                utilitiesPerAction[action] = utilities[actions[action][0][1]]
            actionToTake = max(utilitiesPerAction, key=utilitiesPerAction.get)
            if not self.changeVelocity(actionToTake[0], actionToTake[1]):
                actionsTaken.append(actionToTake)
            else:
                actionsTaken.append((0, 0))
                if self.debug:
                    print("Action " + str(actionToTake) + " failed")
            path.append(self.position)
        return path

    def fastestPathQLearning(self):
        policy = qLearning(self.track, self.hardCrash, 10000)
        self.position = (3, 7)
        path = []
        actionsTaken = []
        while not self.track.isFinish(self.position) and len(actionsTaken) < 10:
            bestAction = policy[self.position[0], self.position[1], self.velocity[0], self.velocity[1]]
            if not self.changeVelocity(bestAction[0], bestAction[1]):
                actionsTaken.append(bestAction)
            else:
                actionsTaken.append((0, 0))
                if self.debug:
                    print("Action " + str(bestAction) + " failed")
            path.append(self.position)
        return path

    def _mildCrash(self, cell):
        """
        Method for when the car crashes and the crash mode is mild. It resets the agents velocity to (0,0)
        and returns it to the closest spot on the course to where the crash occurred
        """
        self.position = cell
        self.velocity = (0, 0)

    def _hardCrash(self):
        """
        Method for when the car crashes and the crash mode is hard. It resets the agents velocity to (0,0)
        and returns it to the starting line
        """
        self.position = random.choice(self.track.startLine)
        self.velocity = (0, 0)

    def _move(self):
        """
        Moves the agent based on current velocity and position
        """
        # Save previous position in case of a crash
        self.prevPosition = self.position
        # Update position based on current position and velocity
        potentialPosition = (self.position[0] + self.velocity[0], self.position[1] + self.velocity[1])
        statusOfMove, cell = self.track.checkTraversed(self.prevPosition, potentialPosition)
        if statusOfMove == -1:
            self.position = cell
            if self.hardCrash:
                self._hardCrash()
            else:
                self._mildCrash(cell)
            if self.debug:
                print("Crash at " + str(cell))
        elif statusOfMove == 1:
            self.position = cell
            return True
        else:
            self.prevPosition = self.position
            self.position = potentialPosition
        return False

    def changeVelocity(self, x, y):
        """
        Changes the velocity of the agent. Velocity cannot exceed -5 or +5 in any direction
        :param x: Value to adjust the velocity in the X coordinate. x must be -1, 0, or 1
        :param y: Value to adjust the velocity in the Y coordinate. y must be -1, 0, or 1
        """
        self.actions += 1
        failed = False
        r = random.random()
        if r <= .8:
            newXVelocity = self.velocity[0] + x
            newYVelocity = self.velocity[1] + y
        else:
            newXVelocity = self.velocity[0]
            newYVelocity = self.velocity[1]
            failed = True
        if abs(newXVelocity) > 5:
            newXVelocity = 5
        if abs(newYVelocity) > 5:
            newYVelocity = 5
        self.velocity = (newXVelocity, newYVelocity)
        self._move()
        if self.debug:
            self.printBoard()
        return failed
