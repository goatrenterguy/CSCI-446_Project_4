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
        return self.transitions[state][action]

    def R(self, state):
        return self.rewards[state]

    def A(self, state):
        return self.transitions[state]

    def makeMDPFromTrack(self, rt: RaceTrack):
        actions = [-1, 0, 1]
        self.makeStatesForMDP(rt.track)
        self.makeRewardsForMDP(rt.track)
        for state in self.states:
            action = {}
            for actionY in actions:
                for actionX in actions:
                    velocityX = state[1][0] + actionX
                    if abs(velocityX) > 5:
                        velocityX = state[1][0]
                    velocityY = state[1][1] + actionX
                    if abs(velocityY) > 5:
                        velocityY = state[1][1]
                    sToSPrimeX = state[0][0] + velocityX
                    sToSPrimeY = state[0][1] + velocityY
                    status, cell = rt.checkTraversed(state[0], (sToSPrimeX, sToSPrimeY))
                    # if status != -1:
                    action[(actionX, actionY)] = [(.8, ((sToSPrimeX, sToSPrimeY), (velocityX, velocityY))),
                                                  (.2, (state[0][0] + state[1][0], state[0][1] + state[1][1]),
                                                   (velocityX, velocityY))]
            self.transitions[state] = action

    def makeRewardsForMDP(self, track):
        for state in self.states:
            if track[state[0][1]][state[0][0]] == 'F':
                self.rewards[state] = 0
            elif track[state[0][1]][state[0][0]] == '.' or track[state[0][1]][state[0][0]] == 'S':
                self.rewards[state] = -1
            else:
                self.rewards[state] = -10

    def makeStatesForMDP(self, track):
        for y in range(len(track)):
            for x in range(len(track[0])):
                if track[y][x] != '#':
                    for yVelocity in range(-5, 6):
                        for xVelocity in range(-5, 6):
                            self.states.append(((x, y), (xVelocity, yVelocity)))
