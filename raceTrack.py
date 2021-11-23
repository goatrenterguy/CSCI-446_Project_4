class RaceTrack:
    def __init__(self, path):
        """
        Initializes a racetrack object
        :param path: Path to the racetrack txt file
        """
        # Read file path and store it in a 2D array
        self.track = self._parseFile(self._loadFile(path))
        self.startLine = self._findStartLine()
        self.finishLine = self._findFinishLine()

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
