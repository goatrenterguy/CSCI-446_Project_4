from raceTrack import RaceTrack

if __name__ == '__main__':
    RaceTrack = RaceTrack("Tracks/L-track.txt")
    print(RaceTrack.track)
    print(RaceTrack.startLine)
    print(RaceTrack.finishLine)
    print(RaceTrack.isWall(-1, 6))


