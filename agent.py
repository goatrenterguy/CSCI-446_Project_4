from raceTrack import RaceTrack
from random import random


class Agent:
    def __init__(self, track: RaceTrack, hardCrash: bool = False):
        """
        Initializes an agent onto a race tracks starting line
        :param track: A race track of type  RaceTrack
        :param hardCrash: Optional Parameter for changing the crash type
        """
        self.track = track
        self.position = random.choice(track.startLine)
        self.prevPosition = self.position
        self.hardCrash = hardCrash
        self.velocity = (0, 0)

    def _mildCrash(self):
        """
        Method for when the car crashes and the crash mode is mild. It resets the agents velocity to (0,0)
        and returns it to the closest spot on the course to where the crash occurred
        """
        pass

    def _hardCrash(self):
        """
        Method for when the car crashes and the crash mode is hard. It resets the agents velocity to (0,0)
        and returns it to the starting line
        """
        pass

    def _move(self):
        """
        Moves the agent based on current velocity and position
        """
        # Save previous position in case of a crash
        self.prevPosition = self.position
        # Update position based on current position and velocity
        self.position = (self.position[0] + self.velocity[0], self.position[1] + self.velocity[1])
        # @TODO Check if passed finish line
        # @TODO Check if agent has hit a wall

    def changeVelocity(self, x, y):
        """
        Changes the velocity of the agent. Velocity cannot exceed -5 or +5 in any direction
        :param x: Value to adjust the velocity in the X coordinate. x must be -1, 0, or 1
        :param y: Value to adjust the velocity in the Y coordinate. y must be -1, 0, or 1
        """
        newXVelocity = self.velocity[0] + x
        newYVelocity = self.velocity[1] + y
        if abs(newXVelocity) > 5:
            newXVelocity = 5
        if abs(newYVelocity) > 5:
            newYVelocity = 5
        self.velocity = (newXVelocity, newYVelocity)

