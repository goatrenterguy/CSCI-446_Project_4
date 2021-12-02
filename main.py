from markovDecisionProcess import MDP
from valueIteration import valueIteration
from raceTrack import RaceTrack
from agent import Agent
from pprint import pprint

if __name__ == '__main__':
    RaceTrack = RaceTrack("Tracks/L-track.txt")
    Agent = Agent(RaceTrack, debug=True, hardCrash=True)
    print(Agent.fastestPathValueIteration())
