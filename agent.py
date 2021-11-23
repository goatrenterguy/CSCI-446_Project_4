import math
from math import floor

from raceTrack import RaceTrack
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
        board = self.track.track.copy()
        board[self.position[1]][self.position[0]] = "C"
        out = "Board:\n"
        for x in board:
            out += str(x) + "\n"
        print(out)

    def _mildCrash(self):
        """
        Method for when the car crashes and the crash mode is mild. It resets the agents velocity to (0,0)
        and returns it to the closest spot on the course to where the crash occurred
        """
        self.position = self.prevPosition
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
        self.position = (self.position[0] + self.velocity[0], self.position[1] + self.velocity[1])
        for cell in self._path(self.prevPosition, self.position):
            if self.track.isWall(cell):
                if self.debug:
                    print("Crash at " + str(cell))
                if self.hardCrash:
                    self._hardCrash()
                else:
                    self._mildCrash()
                return False
            elif self.track.isFinish(cell):
                return True
            else:
                self.prevPosition = cell

    def _path(self, A: tuple, B: tuple):
        """
        Return all cells of the unit grid crossed by the line segment between A and B.
        @:param A: Tuple with x,y (x,y)
        @:param B: Tuple with x,y (x,y)
        """
        traversed = []
        if A == B:
            return traversed
        (x1, y1) = A
        (x2, y2) = B
        deltaX = x2 - x1
        deltaY = y2 - y1
        if deltaX == 0:
            if y1 > y2:
                step = -1
            else:
                step = 1
            for y in range(y1, y2 + 1, step):
                traversed.append((x1, y))
            if self.debug:
                print(traversed)
            return traversed
        distance = math.sqrt(math.pow(deltaX, 2) + math.pow(deltaY, 2))
        xInc = deltaX / distance
        yInc = deltaY / distance
        x = x1
        y = y1
        for step in range(round(distance)):
            x += xInc
            y += yInc
            traversed.append((round(x), round(y)))
        if self.debug:
            print(traversed)
        return traversed

    def changeVelocity(self, x, y):
        """
        Changes the velocity of the agent. Velocity cannot exceed -5 or +5 in any direction
        :param x: Value to adjust the velocity in the X coordinate. x must be -1, 0, or 1
        :param y: Value to adjust the velocity in the Y coordinate. y must be -1, 0, or 1
        """
        self.actions += 1
        newXVelocity = self.velocity[0] + x
        newYVelocity = self.velocity[1] + y
        if abs(newXVelocity) > 5:
            newXVelocity = 5
        if abs(newYVelocity) > 5:
            newYVelocity = 5
        self.velocity = (newXVelocity, newYVelocity)
        if self._move():
            print(self.actions)
        elif self.debug:
            self.printBoard()
