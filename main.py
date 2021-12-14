from markovDecisionProcess import MDP
from valueIteration import valueIteration
from raceTrack import RaceTrack
from agent import Agent
from pprint import pprint
from qLearning import qLearning

if __name__ == '__main__':
    track = RaceTrack("Tracks/R-track.txt", debug=False)
    a = Agent(track, debug=False, hardCrash=False)
    print(a.fastestPathQLearning())
