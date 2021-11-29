import math


class RaceTrack:
    def __init__(self, path, debug=False):
        """
        Initializes a racetrack object
        :param path: Path to the racetrack txt file
        """
        # Read file path and store it in a 2D array
        self.track = self._parseFile(self._loadFile(path))
        self.startLine = self._findStartLine()
        self.finishLine = self._findFinishLine()
        self.debug = debug

    @staticmethod
    def _parseFile(file):
        """
        Method to turn file into a 2D array
        :param file: A racetrack file
        :return: A 2D array representing the racetrack
        """
        track = []
        for line in file:
            line = line.rstrip()
            track.append(list(line))
        return track[1:]

    @staticmethod
    def _loadFile(path):
        """
        Method to try and load file
        :param path: A string representation of the path to the file to be loaded
        :return: The opened file
        """
        try:
            file = open(path, "r")
            return file
        except IOError:
            print("Error: File not found")

    def _findStartLine(self):
        """
        Method to find the coordinates of the start line
        :return: Returns the coordinates of the start line as a list of tuples
        """
        startLine = []
        for y in range(len(self.track)):
            for x in range(len(self.track[0])):
                if self.track[y][x] == 'S':
                    startLine.append((x, y))
        return startLine

    def _findFinishLine(self):
        """
        Method to find the coordinates of the finish line
        :return: Returns the coordinates of the finish line as a list of tuples
        """
        finishLine = []
        for y in range(len(self.track)):
            for x in range(len(self.track[0])):
                if self.track[y][x] == 'F':
                    finishLine.append((x, y))
        return finishLine

    def isWall(self, cell: tuple):
        """
        Method to check if a coordinate is a wall
        :param cell: A tuple containing and x,y coordinate (x, y)
        :return: True if out of bounds of the track or a wall, False otherwise
        """
        x = cell[0]
        y = cell[1]
        if self.track[y][x] == '#' or x > len(self.track[0]) or x < 0 or y > len(self.track) or y < 0:
            return True
        else:
            return False

    def isFinish(self, cell: tuple):
        """
        Method to check if a coordinate is a finish line
        :param cell: A tuple containing and x,y coordinate (x, y)
        :return: True cell is finish line otherwise false
        """
        x = cell[0]
        y = cell[1]
        if self.track[y][x] == 'F':
            return True
        else:
            return False

    def _path(self, A: tuple, B: tuple):
        """
        Checks all cells of the unit grid crossed by the line segment between A and B.
        @:param A: Tuple with x,y (x,y)
        @:param B: Tuple with x,y (x,y)
        :return all of the cells on the line from A to B
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

    def checkTraversed(self, A: tuple, B: tuple):
        for t in self._path(A, B) + [B]:
            if self.isFinish(t):
                return 1, t
            elif self.isWall(t):
                if self.debug:
                    print("Crash at " + str(t))
                return -1, t
        return 0, B
