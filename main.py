from markovDecisionProcess import MDP
from valueIteration import valueIteration
from raceTrack import RaceTrack
from agent import Agent
from pprint import pprint
from qTesting import qLearning

if __name__ == '__main__':
    RaceTrack = RaceTrack("Tracks/L-track.txt", debug=False)
    Agent = Agent(RaceTrack, debug=True, hardCrash=False)
    #print(Agent.fastestPathValueIteration())
    print(Agent.fastestPathQLearning())
    #qLearning(RaceTrack, hardCrash=True, iterations=10000)