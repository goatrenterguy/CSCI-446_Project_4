from raceTrack import RaceTrack
from agent import Agent

if __name__ == '__main__':
    RaceTrack = RaceTrack("Tracks/L-track.txt")
    Agent = Agent(RaceTrack, debug=True)
    Agent.changeVelocity(0, 0)
    Agent.changeVelocity(5, 0)
    Agent.changeVelocity(0, 0)
    Agent.changeVelocity(0, 0)
    Agent.changeVelocity(0, 0)
    Agent.changeVelocity(-1, 0)
    Agent.changeVelocity(-1, 0)
    Agent.changeVelocity(-1, 0)
    Agent.changeVelocity(0, -1)
    Agent.changeVelocity(-1, -1)
    Agent.changeVelocity(0, -1)
