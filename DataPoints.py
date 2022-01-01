import json
from os import X_OK, error
from typing import Counter



class DataPoint:
    def __init__(self, databaseName, databaseField, getBallchasing, getCalculated, ballchasingPlayerIndex = False, teamIndex = False, calculatedPlayerIndex = False, calculateEval = False, calculateVariables = False, value = False, getFromBallchasingPreference = True):
        self.databaseName = databaseName
        self.databaseField = databaseField
        self.getBallchasing = getBallchasing
        self.getCalculated = getCalculated
        self.ballchasingPlayerIndex =  ballchasingPlayerIndex
        self.teamIndex = teamIndex
        self.calculatedPlayerIndex = calculatedPlayerIndex
        self.calculateEval = calculateEval
        self.calculateVariables = calculateVariables
        self.value = value
        self.getFromBallchasingPreference = getFromBallchasingPreference
    def getValue(self):
        if(self.value): return
        if(self.calculateEval):
            if(type(self.calculateEval) == str):
                calcVariables = []
                for variables in self.calculateVariables:
                    dictionary = variables[0]
                    variables = variables[1:]
                    variables = variables.split(";")
                    
                    getList = "".join([f"['{x}']"if type(x) == str else f"[{x}]" for x in variables])
                    if(dictionary == "b"):
                        try:
                            getList = getList.replace("'pIndex'", str(self.ballchasingPlayerIndex))
                            getList = getList.replace("tIndex", str(self.teamIndex))
                        except TypeError:
                            pass
                        calcVariables.append(eval(f"ballchasingDict{getList}"))
                    else:
                        try:
                            getList = getList.replace("'pIndex'", str(self.ballchasingPlayerIndex))
                            getList = getList.replace("tIndex", str(self.teamIndex))
                        except TypeError:
                            pass
                        calcVariables.append(eval(f"calculatedDict{getList}"))
                    #self.calculateEval = self.calculateEval.format([x for x in calcVariables])
                for var in calcVariables:
                    self.calculateEval = self.calculateEval.replace("{}", f"'{var}'" if type(var) == str else str(var), 1)
                self.value = eval(self.calculateEval)               
            else:
                self.calculateEval()
            return
        if(self.getFromBallchasingPreference and self.getBallchasing):
            getList = "".join([f"['{x}']"if type(x) == str else f"[{x}]" for x in self.getBallchasing])
            try:
                getList = getList.replace("'pIndex'", str(self.ballchasingPlayerIndex))
                getList = getList.replace("tIndex", str(self.teamIndex))
            except TypeError:
                pass
            try:
                self.value = eval(f"ballchasingDict{getList}")
            except KeyError:
                print(f"Could not find {getList}")
                self.value = -1
        elif(self.getCalculated):
            getList = "".join([f"['{x}']"if type(x) == str else f"[{x}]" for x in self.getCalculated])
            try:
                getList = getList.replace("'pIndex'", str(self.calculatedPlayerIndex))
                getList = getList.replace("tIndex", str(self.teamIndex))
            except TypeError:
                pass
            try:
                self.value = eval(f"calculatedDict{getList}")
            except KeyError:
                print(f"Could not find {getList}")
                self.value = -1
            except:
                print(self)
                print(getList)
                raise ValueError()
        else:
            raise KeyError("Cannot Get Value")
    def __repr__(self) -> str:
        return f"""
        Database Name: {self.databaseName}
        Database Field: {self.databaseField}
        Get Ballchasing: {self.getBallchasing}
        Get Calculated: {self.getCalculated}
        Ballchasing Player Index: {self.ballchasingPlayerIndex}
        Team Index: {self.teamIndex}
        Calculated Player Index: {self.calculatedPlayerIndex}
        Calculate Eval: {self.calculateEval}
        Calculate Variables: {self.calculateVariables}
        Value: {self.value}
        Get Ballchasing Preference: {self.getFromBallchasingPreference}"""



def GetMMR():
    mmrFile = open(r"C:\Users\tom\AppData\Roaming\bakkesmod\bakkesmod\RocketStats\RocketStats_MMR.txt", 'r')
    currentMMR = float(mmrFile.read())
    mmrFile.close()
    mmrFile = open(r"C:\Users\tom\AppData\Roaming\bakkesmod\bakkesmod\RocketStats\RocketStats_MMRChange.txt", 'r')
    changeMMR = float(mmrFile.read())
    return currentMMR - changeMMR
def SortDateTime(date):
    date, time = date.split("T")
    dataPoints.append(DataPoint("matchTable", "time", False, False, value = time))
    return date
def CalculateGoalSequence(goals, playerIDs):
    playerGameIDs = [x[0] for x in playerIDs]
    playerDatabaseIDs = [x[1] for x in playerIDs]
    goalSequence = ""
    for goal in goals:
        goalID = goal["playerID"]["id"]
        idIndex = playerGameIDs.index(goalID)
        goalSequence += f"{str(playerDatabaseIDs[idIndex])},"
    return goalSequence[:-1]


dataPoints = [
    DataPoint("matchTable", "gameID", ["id"], ["gameMetadata", "id"]),
    DataPoint("matchTable", "replayName", ["title"], ["gameMetadata", "name"]),
    DataPoint("matchTable", "ballchasingLink", ["link"], False),
    DataPoint("matchTable", "map", ["map_code"], ["gameMetadata", "map"]),
    DataPoint("matchTable", "matchType", ["match_type"], False),
    DataPoint("matchTable", "teamSize", ["team_size"], ["gameMetadata", "teamSize"]),
    DataPoint("matchTable", "playlistID", ["playlist_id"], ["gameMetadata", "playlist"]),
    DataPoint("matchTable", "durationCalculated", False, ["gameMetadata", "length"]),
    DataPoint("matchTable", "durationBallchasing", ["duration"], False),
    DataPoint("matchTable", "overtime", ["overtime_seconds"], False),
    DataPoint("matchTable", "season", ["season"], False),
    DataPoint("matchTable", "seasonType", ["season_type"], False),
    DataPoint("matchTable", "date", False, False, calculateEval= "{}.split('T')[0]", calculateVariables = ["bdate"]),
    DataPoint("matchTable", "time", False, False, calculateEval= "{}.split('T')[1]", calculateVariables = ["bdate"]),
    DataPoint("matchTable", "mmr", False, False, calculateEval= GetMMR), 
    DataPoint("matchTable", "nFrames", False, ["gameMetadata", "frames"]),
    DataPoint("matchTable", "orangeScore", ["orange", "stats", "core", "goals"], ["gameMetadata", "score", 1]),
    DataPoint("matchTable", "blueScore", ["blue", "stats", "core", "goals"], ["gameMetadata", "score", 0]),
    #DataPoint("matchTable", "goalSequence", False, ["gameMetadata", "goals"], calculateEval = CalculateGoalSequence), #needs to be done 
    DataPoint("matchTable", "neutralPossessionTime", False, ["gameStats", "neutralPossessionTime"]),
    DataPoint("matchTable", "bTimeGround", False, ["gameStats", "ballStats", "positionalTendencies", "timeOnGround"]),
    DataPoint("matchTable", "bTimeLowAir", False, ["gameStats", "ballStats", "positionalTendencies", "timeLowInAir"]),
    DataPoint("matchTable", "bTimeHighAir", False, ["gameStats", "ballStats", "positionalTendencies", "timeHighInAir"]),
    DataPoint("matchTable", "bTimeBlueHalf", ["blue", "stats", "ball", "possession_time"], ["gameStats", "ballStats", "positionalTendencies", "timeInDefendingHalf"], getFromBallchasingPreference = False),
    DataPoint("matchTable", "bTimeOrangeHalf", ["blue", "stats", "ball", "possession_time"], ["gameStats", "ballStats", "positionalTendencies", "timeInAttackingHalf"], getFromBallchasingPreference = False),
    DataPoint("matchTable", "bTimeBlueThird", False, ["gameStats", "ballStats", "positionalTendencies", "timeInDefendingThird"]),
    DataPoint("matchTable", "bTimeNeutralThird", False, ["gameStats", "ballStats", "positionalTendencies", "timeInNeutralThird"]),
    DataPoint("matchTable", "bTimeOrangeThird", False, ["gameStats", "ballStats", "positionalTendencies", "timeInAttackingThird"]),
    DataPoint("matchTable", "bTimeNearWall", False, ["gameStats", "ballStats", "positionalTendencies", "timeNearWall"]),
    DataPoint("matchTable", "bTimeInCorner", False, ["gameStats", "ballStats", "positionalTendencies", "timeInCorner"]),
    DataPoint("matchTable", "bTimeOnWall", False, ["gameStats", "ballStats", "positionalTendencies", "timeOnWall"]),
    DataPoint("matchTable", "bAverageSpeed", False, ["gameStats", "ballStats", "averages", "averageSpeed"]),
    DataPoint("matchTable", "bType", False, ["mutators", "ballType"]),
    DataPoint("matchTable", "gameMutatorIndex", False, ["mutators", "gameMutatorIndex"]),
    DataPoint("matchTable", "tBlueClumped", False, ["teams", 0, "stats", "centerOfMass", "timeClumped"]),
    DataPoint("matchTable", "tOrangeClumped", False,["teams", 1, "stats", "centerOfMass", "timeClumped"] ),
    DataPoint("matchTable", "tBlueIsolated", False, ["teams", 0, "stats", "centerOfMass", "timeBoondocks"]),
    DataPoint("matchTable", "tOrangeIsolated", False, ["teams", 1, "stats", "centerOfMass", "timeBoondocks"]),
    DataPoint("matchTable", "tBluePossession", ["blue", "stats", "ball", "possession_time"], ["teams", 0, "stats", "possession", "possessionTime"]),
    DataPoint("matchTable", "tOrangePossession", ["orange", "stats", "ball", "possession_time"], ["teams", 1, "stats", "possession", "possessionTime"]),
    
    #DataPoint("playerMatchTable", "playerID"),
    DataPoint("playerMatchTable", "gameID", ["id"], ["gameMetadata", "id"]),
    DataPoint("playerMatchTable", "pBallchasingID", ["tIndex", "players", "pIndex", "id", "id"], False),
    DataPoint("playerMatchTable", "pCalculatedID", False, ["players", "pIndex", "id", "id"]),
    DataPoint("playerMatchTable", "pName", ["tIndex", "players", "pIndex", "name"], ["players", "pIndex", "name"]),
    DataPoint("playerMatchTable", "pPlatform", ["tIndex", "players", "pIndex", "id", "platform"], False),#lazy
    DataPoint("playerMatchTable", "pTier", ["tIndex", "players", "pIndex", "rank", "tier"], False),
    
    DataPoint("playerMatchTable", "carName", ["tIndex", "players", "pIndex", "car_name"], False),#lazy
    DataPoint("playerMatchTable", "titleID", False, ["players", "pIndex", "titleID"]),
    DataPoint("playerMatchTable", "teamColour", ["tIndex", "color"], False),

    DataPoint("playerMatchTable", "bUsage", False, ["players", "pIndex", "stats", "boost", "boostUsage"]),
    DataPoint("playerMatchTable", "bPerMinute", ["tIndex", "players", "pIndex", "stats", "boost", "bpm"], False),#lazy
    DataPoint("playerMatchTable", "bConsumptionPerMinute", ["tIndex", "players", "pIndex", "stats", "boost", "bcpm"], False),#lazy
    DataPoint("playerMatchTable", "aAmount", ["tIndex", "players", "pIndex", "stats", "boost", "avg_amount"], False),#lazy
    DataPoint("playerMatchTable", "qCollected", ["tIndex", "players", "pIndex", "stats",  "boost", "amount_collected"], False),#lazy
    DataPoint("playerMatchTable", "qStolen", ["tIndex", "players", "pIndex", "stats",  "boost", "amount_stolen"], False),#lazy
    DataPoint("playerMatchTable", "qCollectedBig", ["tIndex", "players", "pIndex", "stats", "boost", "amount_collected_big"], False),#lazy
    DataPoint("playerMatchTable", "qCollectedSmall", ["tIndex", "players", "pIndex", "stats", "boost", "amount_collected_small"], False),#lazy
    DataPoint("playerMatchTable", "qStolenBig", ["tIndex", "players", "pIndex", "stats", "boost", "amount_stolen_big"], False),#lazy
    DataPoint("playerMatchTable", "qStolenSmall", ["tIndex", "players", "pIndex", "stats", "boost", "amount_stolen_small"], False),#lazy
    DataPoint("playerMatchTable", "nCollectedBig", ["tIndex", "players", "pIndex", "stats", "boost", "count_collected_big"], False),#lazy
    DataPoint("playerMatchTable", "nCollectedSmall", ["tIndex", "players", "pIndex", "stats", "boost", "count_collected_small"], False),#lazy
    DataPoint("playerMatchTable", "nStolenBig", ["tIndex", "players", "pIndex", "stats", "boost", "count_stolen_big"], False),#lazy
    DataPoint("playerMatchTable", "nStolenSmall", ["tIndex", "players", "pIndex", "stats", "boost", "count_stolen_small"], False),#lazy
    DataPoint("playerMatchTable", "qOverfill", ["tIndex", "players", "pIndex", "stats", "boost", "amount_overfill"], False),#lazy
    DataPoint("playerMatchTable", "qOverfillStolen", ["tIndex", "players", "pIndex", "stats", "boost", "amount_overfill_stolen"], False),#lazy
    DataPoint("playerMatchTable", "qWasted", ["tIndex", "players", "pIndex", "stats", "boost", "amount_used_while_supersonic"], False),#lazy
    DataPoint("playerMatchTable", "tZeroBoost", ["tIndex", "players", "pIndex", "stats", "boost", "time_zero_boost"], False),#lazy
    DataPoint("playerMatchTable", "tFullBoost", ["tIndex", "players", "pIndex", "stats", "boost", "time_full_boost"], False),#lazy
    DataPoint("playerMatchTable", "tBZeroQuarter", ["tIndex", "players", "pIndex", "stats", "boost", "time_boost_0_25"], False),#lazy
    DataPoint("playerMatchTable", "tBQuaterHalf", ["tIndex", "players", "pIndex", "stats", "boost", "time_boost_25_50"], False),#lazy
    DataPoint("playerMatchTable", "tBHalfUpperQuater", ["tIndex", "players", "pIndex", "stats", "boost", "time_boost_50_75"], False),#lazy
    DataPoint("playerMatchTable", "tBUpperQuaterFull", ["tIndex", "players", "pIndex", "stats", "boost", "time_boost_75_100"], False),#lazy
    DataPoint("playerMatchTable", "aSpeed", ["tIndex", "players", "pIndex", "stats", "movement", "avg_speed"], False),#lazy
    DataPoint("playerMatchTable", "aHitDistance", False, ["players", "pIndex", "stats", "averages", "averageHitDistance"]),
    DataPoint("playerMatchTable", "aDistanceFromCentre", False, ["players", "pIndex", "stats", "averages", "averageDistanceFromCenter"]),
    DataPoint("playerMatchTable", "dTotal", ["tIndex", "players", "pIndex", "stats", "movement", "total_distance"], False),#lazy),
    DataPoint("playerMatchTable", "tSonicS", ["tIndex", "players", "pIndex", "stats", "movement", "time_supersonic_speed"], False),#lazy),
    DataPoint("playerMatchTable", "tBoostS", ["tIndex", "players", "pIndex", "stats", "movement", "time_boost_speed"], False),#lazy),
    DataPoint("playerMatchTable", "tSlowS", ["tIndex", "players", "pIndex", "stats", "movement", "time_slow_speed"], False),#lazy),
    DataPoint("playerMatchTable", "tGround", ["tIndex", "players", "pIndex", "stats", "movement", "time_ground"], False),#lazy),
    DataPoint("playerMatchTable", "tLowAir", ["tIndex", "players", "pIndex", "stats", "movement", "time_low_air"], False),#lazy),
    DataPoint("playerMatchTable", "tHighAir", ["tIndex", "players", "pIndex", "stats", "movement", "time_high_air"], False),#lazy),
    DataPoint("playerMatchTable", "tPowerslide", ["tIndex", "players", "pIndex", "stats", "movement", "time_powerslide"], False),#lazy),
    DataPoint("playerMatchTable", "nPowerslide", ["tIndex", "players", "pIndex", "stats", "movement", "count_powerslide"], False),#lazy),
    DataPoint("playerMatchTable", "aPowerslideDuration", ["tIndex", "players", "pIndex", "stats", "movement", "avg_powerslide_duration"], False),#lazy),
    DataPoint("playerMatchTable", "aSpeedPercentage", ["tIndex", "players", "pIndex", "stats", "movement", "avg_speed_percentage"], False),#lazy),
    DataPoint("playerMatchTable", "aDBall", ["tIndex", "players", "pIndex", "stats", "positioning", "avg_distance_to_ball"], False),#lazy),
    DataPoint("playerMatchTable", "aDBallPossession", ["tIndex", "players", "pIndex", "stats", "positioning", "avg_distance_to_ball_possession"], False),#lazy),
    DataPoint("playerMatchTable", "aDBallNoPossession", ["tIndex", "players", "pIndex", "stats", "positioning", "avg_distance_to_ball_no_possession"], False),#lazy),
    DataPoint("playerMatchTable", "aDMates", ["tIndex", "players", "pIndex", "stats", "positioning", "avg_distance_to_mates"], False),#lazy),
    DataPoint("playerMatchTable", "tDefensiveThird", ["tIndex", "players", "pIndex", "stats", "positioning", "time_defensive_third"], False),#lazy),
    DataPoint("playerMatchTable", "tNeutralThird", ["tIndex", "players", "pIndex", "stats", "positioning", "time_neutral_third"], False),#lazy),
    DataPoint("playerMatchTable", "tOffensiveThird", ["tIndex", "players", "pIndex", "stats", "positioning", "time_offensive_third"], False),#lazy),
    DataPoint("playerMatchTable", "tDefensiveHalf", ["tIndex", "players", "pIndex", "stats", "positioning", "time_defensive_half"], False),#lazy),
    DataPoint("playerMatchTable", "tOffensiveHalf", ["tIndex", "players", "pIndex", "stats", "positioning", "time_offensive_half"], False),#lazy),
    DataPoint("playerMatchTable", "tBehindBall", ["tIndex", "players", "pIndex", "stats", "positioning", "time_behind_ball"], False),#lazy),
    DataPoint("playerMatchTable", "tInFrontBall", ["tIndex", "players", "pIndex", "stats", "positioning", "time_infront_ball"], False),#lazy),
    DataPoint("playerMatchTable", "tMostBack", ["tIndex", "players", "pIndex", "stats", "positioning", "time_most_back"], False),#lazy),
    DataPoint("playerMatchTable", "tMostForward", ["tIndex", "players", "pIndex", "stats", "positioning", "time_most_forward"], False),#lazy),
    DataPoint("playerMatchTable", "goalsConcededLast", ["tIndex", "players", "pIndex", "stats", "positioning", "goals_against_while_last_defender"], False),#lazy),
    DataPoint("playerMatchTable", "tClosestBall", ["tIndex", "players", "pIndex", "stats", "positioning", "time_closest_to_ball"], False),#lazy),
    DataPoint("playerMatchTable", "tFarthestBall", ["tIndex", "players", "pIndex", "stats", "positioning", "time_farthest_from_ball"], False),#lazy),
    DataPoint("playerMatchTable", "tCloseBall", False, ["players", "pIndex", "stats", "distance", "timeCloseToBall"]),
    DataPoint("playerMatchTable", "tNearWall", False, ["players", "pIndex", "stats", "positionalTendencies", "timeNearWall"]),
    DataPoint("playerMatchTable", "tInCorner", False, ["players", "pIndex", "stats", "positionalTendencies", "timeInCorner"]),
    DataPoint("playerMatchTable", "tOnWall", False, ["players", "pIndex", "stats", "positionalTendencies", "timeOnWall"]),
    DataPoint("playerMatchTable", "dHitForward", False, ["players", "pIndex", "stats", "distance", "ballHitForward"]),
    DataPoint("playerMatchTable", "dHitBackward", False, ["players", "pIndex", "stats", "distance", "ballHitBackward"]),
    DataPoint("playerMatchTable", "pTime", False, ["players", "pIndex", "stats", "possession", "possessionTime"]),
    DataPoint("playerMatchTable", "turnovers", False, ["players", "pIndex", "stats", "possession", "turnovers"]),
    DataPoint("playerMatchTable", "turnoversMyHalf", False, ["players", "pIndex", "stats", "possession", "turnoversOnMyHalf"]),
    DataPoint("playerMatchTable", "turnoversTheirHalf", False, ["players", "pIndex", "stats", "possession", "turnoversOnTheirHalf"]),
    DataPoint("playerMatchTable", "wonTurnovers", False, ["players", "pIndex", "stats", "possession", "wonTurnovers"]),
    DataPoint("playerMatchTable", "aPDuration", False, ["players", "pIndex", "stats", "perPossessionStats", "averageDuration"]),
    DataPoint("playerMatchTable", "aPHits", False, ["players", "pIndex", "stats", "perPossessionStats", "averageHits"]),
    DataPoint("playerMatchTable", "qPossession", False, ["players", "pIndex", "stats", "perPossessionStats", "count"]),
    DataPoint("playerMatchTable", "demoInflicted", ["tIndex", "players", "pIndex", "stats", "demo", "inflicted"], False),#lazy),
    DataPoint("playerMatchTable", "demoTaken", ["tIndex", "players", "pIndex", "stats", "demo", "taken"], False),#lazy),
    DataPoint("playerMatchTable", "score", ["tIndex", "players", "pIndex", "stats", "core", "score"], False),#lazy),
    DataPoint("playerMatchTable", "goals", ["tIndex", "players", "pIndex", "stats", "core", "goals"], False),#lazy),
    DataPoint("playerMatchTable", "assists", ["tIndex", "players", "pIndex", "stats", "core", "assists"], False),#lazy),
    DataPoint("playerMatchTable", "saves", ["tIndex", "players", "pIndex", "stats", "core", "saves"], False),#lazy),
    DataPoint("playerMatchTable", "shots", ["tIndex", "players", "pIndex", "stats", "core", "shots"], False),#lazy),
    DataPoint("playerMatchTable", "mvp", ["tIndex", "players", "pIndex", "stats", "core", "mvp"], False),#lazy),
    DataPoint("playerMatchTable", "shootingP", ["tIndex", "players", "pIndex", "stats", "core", "shooting_percentage"], False),#lazy),
    DataPoint("playerMatchTable", "totalHits", False, ["players", "pIndex", "stats", "hitCounts", "totalHits"]),
    DataPoint("playerMatchTable", "totalPasses", False, ["players", "pIndex", "stats", "hitCounts", "totalPasses"]),
    DataPoint("playerMatchTable", "totalDribbles", False, ["players", "pIndex", "stats", "hitCounts", "totalDribbles"]),
    DataPoint("playerMatchTable", "totalDribblesConts", False, ["players", "pIndex", "stats", "hitCounts", "totalDribbleConts"]),
    DataPoint("playerMatchTable", "totalAerials", False, ["players", "pIndex", "stats", "hitCounts", "totalAerials"]),
    DataPoint("playerMatchTable", "totalClears", False, ["players", "pIndex", "stats", "hitCounts", "totalClears"]),
    DataPoint("playerMatchTable", "isKeyboard", False, ["players", "pIndex", "stats", "controller", "isKeyboard"]),
    DataPoint("playerMatchTable", "tBallCam", False, ["players", "pIndex", "stats", "controller", "timeBallcam"]),
    DataPoint("playerMatchTable", "qCarries", False, ["players", "pIndex", "stats", "ballCarries", "totalCarries"]),
    DataPoint("playerMatchTable", "qFlicks", False, ["players", "pIndex", "stats", "ballCarries", "totalFlicks"]),
    DataPoint("playerMatchTable", "totalCarryT", False, ["players", "pIndex", "stats", "ballCarries", "totalCarryTime"]),
    DataPoint("playerMatchTable", "totalCarryD", False, ["players", "pIndex", "stats", "ballCarries", "totalCarryDistance"]),
    DataPoint("playerMatchTable", "aCarryT", False, ["players", "pIndex", "stats", "ballCarries", "averageCarryTime"]),
    DataPoint("playerMatchTable", "totalKickoffs", False, ["players", "pIndex", "stats", "kickoffStats", "totalKickoffs"]),
    DataPoint("playerMatchTable", "numGoBoost", False, ["players", "pIndex", "stats", "kickoffStats", "numTimeBoost"]),
    DataPoint("playerMatchTable", "numnGoFollow", False, ["players", "pIndex", "stats", "kickoffStats", "numTimeCheat"]),
    DataPoint("playerMatchTable", "numGoBall", False, ["players", "pIndex", "stats", "kickoffStats", "numTimeGoToBall"]),
    DataPoint("playerMatchTable", "numFirstTouch", False, ["players", "pIndex", "stats", "kickoffStats", "numTimeFirstTouch"]),
    DataPoint("playerMatchTable", "aBoostUsed", False, ["players", "pIndex", "stats", "kickoffStats", "averageBoostUsed"]),
    DataPoint("playerMatchTable", "isBot", False, ["players", "pIndex", "isBot"]),
    DataPoint("playerMatchTable", "partyLeaderID", False, ["players", "pIndex", "partyLeader", "id"]),
    DataPoint("playerMatchTable", "ballchasingStartTime", ["tIndex", "players", "pIndex", "start_time"], False),#lazy),
    DataPoint("playerMatchTable", "ballchasingEndTime", ["tIndex", "players", "pIndex", "end_time"], False),#lazy),
    DataPoint("playerMatchTable", "ballchasingBoostTime", False, False, calculateEval = "{} + {} + {} + {}", calculateVariables=["btIndex;players;pIndex;stats;boost;time_boost_0_25", "btIndex;players;pIndex;stats;boost;time_boost_25_50", "btIndex;players;pIndex;stats;boost;time_boost_50_75", "btIndex;players;pIndex;stats;boost;time_boost_75_100"]),
    DataPoint("playerMatchTable", "ballchasingStatTime", False, False, calculateEval = "{} + {}", calculateVariables= ["btIndex;players;pIndex;stats;positioning;time_defensive_half", "btIndex;players;pIndex;stats;positioning;time_offensive_half"]),
    DataPoint("playerMatchTable", "calculatedFirstFrame", False, ["players", "pIndex", "firstFrameInGame"]),
    DataPoint("playerMatchTable", "calculatedTimeInGame", False, ["players", "pIndex", "timeInGame"]),   
]

class Player():
    def __init__(self, playerIndex, teamIndex, ballchasingPlayerIndex, calculatedPlayerIndex):
        self.playerIndex = playerIndex
        self.teamIndex = teamIndex
        self.ballchasingPlayerIndex = ballchasingPlayerIndex
        self.calculatedPlayerIndex = calculatedPlayerIndex
        self.dataPoints = []
openFile = open(r"d:\Users\tom\Documents\Visual Studio Code\Python Files\RocketReplayAnalysis\Examples and Testing\ballchasingAnalysis.json")
ballchasingDict = json.load(openFile)
openFile.close()
openFile = open(r"d:\Users\tom\Documents\Visual Studio Code\Python Files\RocketReplayAnalysis\Examples and Testing\exampleReplay3.replay.json")
calculatedDict = json.load(openFile)
openFile.close()

matchDataPoints = []
playerDataPoints = []
players = []
for dataPoint in dataPoints:
    if(dataPoint.databaseName == "matchTable"):
        dataPoint.getValue()
        matchDataPoints.append(dataPoint)
    else:
        playerDataPoints.append(dataPoint)
playerIndex = -1
colours = ["blue", "orange"]

for colour in colours:
    for i, player in enumerate(ballchasingDict[colour]["players"]):
        playerIndex += 1
        teamIndex = colour
        ballchasingPlayerIndex = i
        name = player["name"]
        foundPlayer = False
        verifyCheck = int(player["stats"]["core"]["score"])
        for i, playerC in enumerate(calculatedDict["players"]):
            if playerC["name"] == name and int(playerC["score"]) == verifyCheck:
                calculatedIndex = i
                foundPlayer = True
                break
        if not foundPlayer:
            for i, playerC in enumerate(calculatedDict["players"]):
                if playerC["name"] == name:
                    calculatedIndex = i
                    break
        players.append(Player(playerIndex, teamIndex, ballchasingPlayerIndex, calculatedIndex))


for player in players:
    for dataPoint in playerDataPoints:
        newDataPoint = DataPoint(dataPoint.databaseName, dataPoint.databaseField, 
                                 dataPoint.getBallchasing, dataPoint.getCalculated,
                                 ballchasingPlayerIndex = player.ballchasingPlayerIndex,
                                 teamIndex = player.teamIndex,
                                 calculatedPlayerIndex = player.calculatedPlayerIndex,
                                 calculateEval = dataPoint.calculateEval,
                                 calculateVariables = dataPoint.calculateVariables,
                                 value = dataPoint.value,
                                 getFromBallchasingPreference = dataPoint.getFromBallchasingPreference)
        newDataPoint.getValue()
        player.dataPoints.append(newDataPoint)

print(matchDataPoints)

#for player in players:
#    print(player.dataPoints)

