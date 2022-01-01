#3.8

from logging import error
import sqlite3; from sqlite3 import Error
import carball, ballchasing
from numpy import float64
from time import sleep
from glob import glob
from os import path
from shutil import ExecError, move
debugMode = False
databaseFolder = r"d:\\Users\\tom\Documents\\Visual Studio Code\\Python Files\\RocketReplayAnalysis\\Database\\"
databaseName = r"replayDatabase.db"

replayFolder = r"C:\\Users\\tom\\AppData\\Roaming\\bakkesmod\\bakkesmod\\data\\replays\\"
#replayFolder = r"d:\\Users\\tom\\Documents\\My Games\\Rocket League\\TAGame\\Demos\\"
processedReplayFolder = r"d:\\Users\\tom\\Documents\\My Games\\Rocket League\\TAGame\\Demos\\processedReplays\\"
errorFolder = r"d:\\Users\\tom\\Documents\\My Games\\Rocket League\\TAGame\\Demos\\processedReplays\\error replays\\"
ballchasingAPIToken = "otD1YFTrYz5sUy7GfZBW9mMNTB66QTLnQcqrpeIS"

colours = ["blue", "orange"]

def CreateConnection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"SQLite3 Version: {sqlite3.version}")
    except Error as e:
        print(e)
    return conn
    #finally:
    #    if conn:
    #        conn.close()
def CreateTable(conn, createTableStatement):
    try:
        c = conn.cursor()
        c.execute(createTableStatement)
    except Error as e:
        print(e)
###Data Point Functions
def GetMMR():
    mmrFile = open(r"C:\Users\tom\AppData\Roaming\bakkesmod\bakkesmod\RocketStats\RocketStats_MMR.txt", 'r')
    currentMMR = float(mmrFile.read())
    mmrFile.close()
    mmrFile = open(r"C:\Users\tom\AppData\Roaming\bakkesmod\bakkesmod\RocketStats\RocketStats_MMRChange.txt", 'r')
    changeMMR = float(mmrFile.read())
    return currentMMR - changeMMR
def SortDateTime(date):
    return date.split("T")
def CalculateGoalSequence(goals, playerIDs):
    playerGameIDs = [x[0] for x in playerIDs]
    playerDatabaseIDs = [x[1] for x in playerIDs]
    goalSequence = ""
    for goal in goals:
        goalID = goal["playerID"]["id"]
        idIndex = playerGameIDs.index(goalID)
        goalSequence += f"{str(playerDatabaseIDs[idIndex])},"
    return goalSequence[:-1]
class DataPointAnalysis:
    def __init__(self, name, relevancy, relevantDifference,
                       isSoloStat,
                       *compareTo):
        self.name = name
        self.r = relevancy
        self.rD = relevantDifference
        self.isSoloStat = isSoloStat
        self.cT = compareTo
        self.sN = 0
        #vsAllMatch, vsAllSeries,
        #vsOpponentsMatch, vsOpponentsSeries,
        #vsTeamMatch, vsTeamSeries,
        #vsSelfSeries, vsSelfHistoric,
        #teamVSOpponentsMatch, teamVSOpponentsSeries,
        #teamsVSSelfHistoric, teamsVSSelfSeries
    def CalculateSNR(self, match,  conn, series = [], relative = True,  compareValue = None):
        if self.r <= 0:
            self.sN = 0
        for compareAgainst in self.cT:
            if self.isSoloStat:
                if compareAgainst == "allMatch":
                    compareToStats = [x.__dict__[self.name] for x in match.players]
                    compareToStats.remove()
                    if relative == True:
                        pass
                    else:
                        pass
                elif compareAgainst == "allSeries":
                    pass
                elif compareAgainst == "opponentsMatch":
                    pass
                elif compareAgainst == "opponentsSeries":
                    pass
                elif compareAgainst == "teamMatch":
                    pass
                elif compareAgainst == "teamSeries":
                    pass
                elif compareAgainst == "selfSeries":
                    pass
                elif compareAgainst == "selfHistoric":
                    pass
                elif compareAgainst == "value":
                    pass
                else:
                    print("Pepega")
            else:
                if compareAgainst == "opponentMatch":
                    pass
                elif compareAgainst == "opponentSeries":
                    pass
                elif compareAgainst == "selfSeries":
                    pass
                elif compareAgainst == "selfHistoric":
                    pass
                else:
                    print("Pepega v2")

        
        
class DataPoint:
    def __init__(self, databaseName, databaseField, getBallchasing, getCalculated, ballchasingPlayerIndex = False, teamIndex = False, calculatedPlayerIndex = False, calculateEval = False, calculateVariables = False, value = False):
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
    def getValue(self):
        if(self.value != False):return
        if(self.calculateEval):
            if(type(self.calculateEval) == str):
                try:
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
                except KeyError:
                    print(f"couldn't find {calcVariables}")
            else:
                self.calculateEval()
            return
        if(self.getBallchasing):
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
            except (KeyError, SyntaxError):
                print(f"Could not find {getList}")
                self.value = -1
            except:
                print("Data Point ERROR")
                print(self)
                print(getList)
                raise ValueError("data point")
        else:
            raise KeyError("Cannot Get Value")
        if(type(self.value) not in [str, int, float]):
            if(type(self.value)) == bool:
                self.value = int(self.value)
            elif(type(self.value) == float64):
                self.value = float(self.value)
            else:
                raise TypeError(f"Invalid Type: {type(self.value)}")
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
        Value: {self.value}"""
    def CreateCopy(self):
        return DataPoint(self.databaseName, self.databaseField, self.getBallchasing, self.getCalculated, self.ballchasingPlayerIndex, self.teamIndex, self.calculatedPlayerIndex, self.calculateEval, self.calculateVariables, self.value)

matchDataPoints = [
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
    #DataPoint("matchTable", "bTimeBlueHalf", ["blue", "stats", "ball", "possession_time"], ["gameStats", "ballStats", "positionalTendencies", "timeInDefendingHalf"], getFromBallchasingPreference = False),
    #DataPoint("matchTable", "bTimeOrangeHalf", ["blue", "stats", "ball", "possession_time"], ["gameStats", "ballStats", "positionalTendencies", "timeInAttackingHalf"], getFromBallchasingPreference = False),
    DataPoint("matchTable", "bTimeBlueHalf", False, ["gameStats", "ballStats", "positionalTendencies", "timeInDefendingHalf"]),
    DataPoint("matchTable", "bTimeOrangeHalf", False, ["gameStats", "ballStats", "positionalTendencies", "timeInAttackingHalf"]),
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
    DataPoint("matchTable", "tOrangePossession", ["orange", "stats", "ball", "possession_time"], ["teams", 1, "stats", "possession", "possessionTime"])]
    
    #DataPoint("playerMatchTable", "playerID"),
playerDataPoints = [
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
    def __init__(self, playerIndex, teamIndex, ballchasingPlayerIndex, calculatedPlayerIndex, calculatedID):
        self.playerIndex = playerIndex
        self.teamIndex = teamIndex
        self.ballchasingPlayerIndex = ballchasingPlayerIndex
        self.calculatedPlayerIndex = calculatedPlayerIndex
        self.dataPoints = []
        self.calculatedID = calculatedID
    def sortID(self):
        if type(self.calculatedID) == list:
            self.calculatedID = self.calculatedID[0]
            try:
                self.calculatedID = int(self.calculatedID)
            except ValueError:
                pass


def GetLatestReplay(replayFolder):
    files = glob(replayFolder + "\*replay")
    try:
        return max(files, key = path.getctime)
    except ValueError as e:
        print(f"no new replays to process {e}")
def GetBallchasingDict(ballchasingAPI: ballchasing.Api, latestReplay):
    replayFile = open(latestReplay, "rb")
    replay = ballchasingAPI.upload_replay(replayFile)
    replayID = replay["id"]
    replayFile.close()
    return ballchasingAPI.get_replay(replayID)
def GetCalculatedDict(latestReplay):
    #carball.analyze_replay_file(latestReplay, calculate_intensive_events=True).get_json_data()
    try:
        analysis_manager = carball.analyze_replay_file(latestReplay,
                                               calculate_intensive_events=True)
        analysisJson = analysis_manager.get_json_data()
        return analysisJson
    except Exception as e:
        print(f"Error Getting Calculated Dictionary {e}")
        print("hello are you here?!?!??!?!?!??")
        raise ValueError("Calculated Dict")
        return {}

def GetPlayers(playerIndex : int):
    for colour in colours:
        if "blue" not in ballchasingDict:
            print(ballchasingDict)
            raise BufferError("Player Error")
        for i, player in enumerate(ballchasingDict[colour]["players"]):
            playerIndex += 1
            name = player["name"]
            foundPlayer = False
            verifyCheck = int(player["stats"]["core"]["score"])
            calculatedIndex = ""
            if "players" in calculatedDict:
                for j, playerC in enumerate(calculatedDict["players"]):
                    try:
                        if playerC["name"] == name and int(playerC["score"]) == verifyCheck:
                            calculatedIndex = j
                            foundPlayer = True
                            break
                    except KeyError:
                        print("no score bruv")
                        calculatedIndex = j
                        foundPlayer = True
                        break

                if not foundPlayer:
                    for j, playerC in enumerate(calculatedDict["players"]):
                        if playerC["name"].replace("ぎ", "N0").replace("М", "").replace("っ", "c0").replace("ø", "").replace("μ", "").replace("ı", "1").replace("Ψ", "").replace("ﱞ", "^").replace("ㅁ", "A1").replace("é", "e").replace("レ", "0").replace("ツ", "0").replace("ï", "i").replace("º", "o").replace("たげい", "_0R0D0").replace("ヘイズ-", "000-") == name:#fucking invisible characters and broken shit
                            calculatedIndex = j
                            break
                if calculatedIndex == "":
                    #print([x["id"] for x in calculatedDict["players"]])
                    #print([player["id"] for player in ballchasingDict[colour]["players"]])
                    #print(player["id"])
                    #input()
                    for j, playerC in enumerate(calculatedDict["players"]):
                        try:
                            if playerC["id"]["id"] == player["id"]["id"]:
                                calculatedIndex = j
                        except KeyError:
                            raise ValueError("Player oopsie")
                            pass
                    if calculatedIndex == "":
                        print("calculated ids:",[x["id"] for x in calculatedDict["players"]])
                        print("calculated players:",[x["name"] for x in calculatedDict["players"]])
                        print("ballchasing players", [player["name"] for player in ballchasingDict[colour]["players"]])
                        print("ballchasing player ids:",[player["id"] for player in ballchasingDict[colour]["players"]])
                        print("ballchasing player id:",player["id"])
                        #print(player)
                        raise ValueError("Player Error")
            else:
                print("\nno players\n")
                print(calculatedDict)
                #input()
            try:
                calculatedID = calculatedDict["players"][calculatedIndex]["id"]["id"]
            except (TypeError, KeyError):
                calculatedID = ""
            players.append(Player(playerIndex, colour, i, calculatedIndex, calculatedID))
    return playerIndex

def AddFailedReplay(replay, fRS = r"d:\Users\tom\Documents\Visual Studio Code\Python Files\RocketReplayAnalysis\Database\failedReplays.txt"):
    fRFile = open(fRS, "a")
    fRFile.write(str(replay))
    fRFile.write("\n")
    fRFile.close()
def HandleReplay(replay, ballchasingAPI, matchIndex, playerIndex, cur, dbConn):
    global ballchasingDict
    global calculatedDict
    global players
    print(f"Replay: {replay}")
    try:
        ballchasingDict = GetBallchasingDict(ballchasingAPI, replay)
        calculatedDict = GetCalculatedDict(replay)
    except IndexError as e:
        print(f"index error handling replays, skipping: {e}")
        AddFailedReplay(replay)
        return matchIndex, playerIndex, True
    originalPlayerIndex = playerIndex
    players = []
    matchIndex += 1
    matchData = [DataPoint("matchTable", "matchID", False, False, value = matchIndex)]
    for dataPoint in matchDataPoints:
        newDataPoint = dataPoint.CreateCopy()
        newDataPoint.getValue()
        matchData.append(newDataPoint)
    goalSequence = ""
    try:
        playerIndex = GetPlayers(playerIndex)
    #except UnboundLocalError as e:
    except BufferError as e:
        AddFailedReplay(replay)
        print(f"replay failed, could not get players: {e}")
        return matchIndex - 1, originalPlayerIndex, True
    #print("\n" * 5)
    try:
        #print(calculatedDict["gameMetadata"]["goals"])
        #print([x.calculatedID for x in players])
        for goal in calculatedDict["gameMetadata"]["goals"]:
            goalScorer = [x.playerIndex for x in players if x.calculatedID == goal["playerId"]["id"]][0]
            #print(goalScorer)
            goalSequence += str(goalScorer - (originalPlayerIndex + 1))
            goalSequence += ","
        goalSequence = goalSequence[:-1]
        matchData.append(DataPoint("matchTable", "goalSequence", False, False, value = goalSequence))
    except Exception as e:#KeyError as e:
        print("cannot get goal sequence data")
        print(e)
    matchData.append(DataPoint("matchTable", "startPlayerIndex", False, False, value = originalPlayerIndex + 1))
    try:
        cur.execute(f"""INSERT INTO matchTable ({','.join([x.databaseField for x in matchData])}) VALUES ({','.join([f'"{x.value}"' if type(x.value) == str else f"{str(x.value)}" for x in matchData])})""")
    except sqlite3.IntegrityError:
        print(f"Duplicate Replay - Ignored")
        return matchIndex - 1, originalPlayerIndex, False
    try:
        fiftyFifties = calculatedDict["gameStats"]["fiftyFifties"]
        fiftyStats = {}
        for player in players:
            fiftyStats[player.playerIndex] = [0, 0, 0]
            player.sortID()
        for fifty in fiftyFifties:
            try:
                playerOne = fifty["players"][0]["id"]
                playerOne = [x for x in players if x.calculatedID == playerOne][0]
                playerTwo = fifty["players"][1]["id"]
                playerTwo = [x for x in players if x.calculatedID == playerTwo][0]
            except IndexError as e:
                print(f"Index Error Fifty: {e}")
                continue
            try:
                winner = fifty["winner"]["id"]
                if playerOne.calculatedID == winner:
                    fiftyStats[playerOne.playerIndex] = [fiftyStats[playerOne.playerIndex][0] + 1, fiftyStats[playerOne.playerIndex][1], fiftyStats[playerOne.playerIndex][2]]
                    fiftyStats[playerTwo.playerIndex] = [fiftyStats[playerTwo.playerIndex][0], fiftyStats[playerTwo.playerIndex][1] + 1, fiftyStats[playerTwo.playerIndex][2]]
                else:
                    fiftyStats[playerOne.playerIndex] = [fiftyStats[playerOne.playerIndex][0], fiftyStats[playerOne.playerIndex][1] + 1, fiftyStats[playerOne.playerIndex][2]]
                    fiftyStats[playerTwo.playerIndex] = [fiftyStats[playerTwo.playerIndex][0] + 1, fiftyStats[playerTwo.playerIndex][1], fiftyStats[playerTwo.playerIndex][2]]
            except KeyError:
                print("draw")
                fiftyStats[playerOne.playerIndex] = [fiftyStats[playerOne.playerIndex][0], fiftyStats[playerOne.playerIndex][1], fiftyStats[playerOne.playerIndex][2] + 1]
                fiftyStats[playerTwo.playerIndex] = [fiftyStats[playerTwo.playerIndex][0], fiftyStats[playerTwo.playerIndex][1], fiftyStats[playerTwo.playerIndex][2] + 1]
    except KeyError:
        print("Could not Find Fifty Fifty Data")
        fiftyStats = []
    for player in players:
        player.dataPoints.append(DataPoint("playerMatchTable", "playerID", False, False, value = player.playerIndex))
        player.dataPoints.append(DataPoint("playerMatchTable", "matchID", False, False, value = matchIndex))
        if (player.playerIndex in fiftyStats):
            print("getting fifty stats")
            playerFiftyStats = fiftyStats[player.playerIndex]
            player.dataPoints.append(DataPoint("playerMatchTable", "fiftyWins", False, False, value = playerFiftyStats[0]))
            player.dataPoints.append(DataPoint("playerMatchTable", "fiftyLosses", False, False, value = playerFiftyStats[1]))
            player.dataPoints.append(DataPoint("playerMatchTable", "fiftyDraws", False, False, value = playerFiftyStats[2]))
        for dataPoint in playerDataPoints:
            newDataPoint = DataPoint(dataPoint.databaseName, dataPoint.databaseField, 
                         dataPoint.getBallchasing, dataPoint.getCalculated,
                         ballchasingPlayerIndex = player.ballchasingPlayerIndex,
                         teamIndex = player.teamIndex,
                         calculatedPlayerIndex = player.calculatedPlayerIndex,
                         calculateEval = dataPoint.calculateEval,
                         calculateVariables = dataPoint.calculateVariables,
                         value = dataPoint.value)
            newDataPoint.getValue()
            if dataPoint.databaseField == "pName":
                newDataPoint.value = newDataPoint.value.replace('"', "'")
            player.dataPoints.append(newDataPoint) 
        
        
        executeSTR = f"""INSERT INTO playerMatchTable ({','.join([x.databaseField for x in player.dataPoints])}) VALUES ({','.join([f'"{x.value}"' if type(x.value) == str else f"{str(x.value)}" for x in player.dataPoints])})"""
        try:
            cur.execute(executeSTR)
        except Exception as e:
            print(executeSTR)
            raise e

    dbConn.commit()
    return matchIndex, playerIndex, False

def main(replayFolder = r"C:\\Users\\tom\\AppData\\Roaming\\bakkesmod\\bakkesmod\\data\\replays\\"):
    global ballchasingDict
    global calculatedDict
    global players

    dbConn = CreateConnection(databaseFolder + databaseName)
    cur = dbConn.cursor()
    
    latestReplay = GetLatestReplay(replayFolder)
    #b = boost, t = time
    CreateTable(dbConn, """CREATE TABLE IF NOT EXISTS matchTable(
                                matchID integer PRIMARY KEY,
                                gameID text UNIQUE,
                                replayName text,
                                ballchasingLink text,
                                map text,
                                matchType integer,
                                teamSize integer,
                                playlistID text,
                                durationCalculated real,
                                durationBallchasing real,
                                overtime integer,
                                season integer,
                                seasonType integer,
                                date text,
                                time text,
                                mmr integer,
                                nFrames integer,
                                orangeScore integer,
                                blueScore integer,
                                goalSequence text,

                                neutralPossessionTime real,
                                bTimeGround real,
                                bTimeLowAir real,
                                bTimeHighAir real,
                                bTimeBlueHalf real,
                                bTimeOrangeHalf real,
                                bTimeBlueThird real,
                                bTimeNeutralThird real,
                                bTimeOrangeThird real,
                                bTimeNearWall real,
                                bTimeInCorner real,
                                bTimeOnWall real,
                                bAverageSpeed real,

                                bType text,
                                gameMutatorIndex integer,

                                tBlueClumped real,
                                tOrangeClumped real,
                                tBlueIsolated real,
                                tOrangeIsolated real,
                                tBluePossession real,
                                tOrangePossession real,

                                replayTagOne text,
                                replayTagTwo text,
                                replayTagThree text,
                                replayTagFour text,
                                replayTagFive text,

                                startPlayerIndex integer
                            ) WITHOUT ROWID;""")
    #p = player, b = boost, a = average, q = quanity, n = num, t = time, d = distance, p = possession/ player, s = speed
    CreateTable(dbConn, """CREATE TABLE IF NOT EXISTS playerMatchTable(
                                playerID integer PRIMARY KEY,
                                matchID integer NOT NULL,
                                gameID integer,
                                pBallchasingID text,
                                pCalculatedId text,
                                pName text,
                                pPlatform text integer,
                                pTier integer,
                                
                                carName text,
                                titleID integer,

                                teamColour integer,

                                bUsage real,
                                bPerMinute real,
                                bConsumptionPerMinute real,
                                aAmount real,
                                qCollected integer,
                                qStolen integer,
                                qCollectedBig integer,
                                qCollectedSmall integer,
                                qStolenBig integer,
                                qStolenSmall integer,
                                nCollectedBig integer,
                                nCollectedSmall integer,
                                nStolenBig integer,
                                nStolenSmall integer,
                                qOverfill integer,
                                qOverfillStolen integer,
                                qWasted integer,

                                tZeroBoost real,
                                tFullBoost real,
                                tBZeroQuarter real,
                                tBQuaterHalf real,
                                tBHalfUpperQuater real,
                                tBUpperQuaterFull real,
                                
                                aSpeed integer,
                                aHitDistance real,
                                aDistanceFromCentre real,

                                dTotal integer,
                                tSonicS real,
                                tBoostS real,
                                tSlowS real,
                                
                                tGround real,
                                tLowAir real,
                                tHighAir real,
                                tPowerslide real,
                                nPowerslide integer,
                                aPowerslideDuration real,
                                aSpeedPercentage real,

                                aDBall integer,
                                aDBallPossession integer,
                                aDBallNoPossession integer,
                                aDMates integer,
                                tDefensiveThird real,
                                tNeutralThird real,
                                tOffensiveThird real,
                                tDefensiveHalf real,
                                tOffensiveHalf real,
                                tBehindBall real,
                                tInFrontBall real,
                                tMostBack real,
                                tMostForward real,
                                goalsConcededLast integer,
                                tClosestBall real,
                                tFarthestBall real,
                                tCloseBall real,

                                tNearWall real,
                                tInCorner real,
                                tOnWall real,

                                dHitForward real,
                                dHitBackward real,

                                pTime real,
                                turnovers integer,
                                turnoversMyHalf integer,
                                turnoversTheirHalf integer,
                                wonTurnovers integer,
                                aPDuration real,
                                aPHits real,
                                qPossession integer,

                                demoInflicted integer,
                                demoTaken integer,

                                score integer,
                                goals integer,
                                assists integer,
                                saves integer,
                                shots integer,
                                mvp integer,
                                shootingP integer,

                                totalHits integer,
                                totalPasses integer,
                                totalDribbles integer,
                                totalDribblesConts integer,
                                totalAerials integer,
                                totalClears integer,

                                isKeyboard integer,
                                tBallCam real,

                                qCarries integer,
                                qFlicks integer,
                                totalCarryT real,
                                totalCarryD real,
                                aCarryT real,
                                
                                totalKickoffs integer,
                                numGoBoost integer,
                                numnGoFollow integer,
                                numGoBall integer,
                                numFirstTouch integer,
                                aBoostUsed real,

                                fiftyWins integer,
                                fiftyLosses integer,
                                fiftyDraws integer,
                                
                                isBot integer,

                                partyLeaderID,

                                ballchasingStartTime real,
                                ballchasingEndTime real,
                                ballchasingBoostTime real,
                                ballchasingStatTime real,

                                calculatedFirstFrame integer,
                                calculatedTimeInGame real,

                                FOREIGN KEY(matchID)
                                    REFERENCES matchTable (matchID)
                            ) WITHOUT ROWID;""")
    cur.execute("SELECT playerID FROM playerMatchTable ORDER BY playerID DESC;")
    try:
        playerIndex = int(cur.fetchone()[0])
    except TypeError:
        playerIndex = -1
    cur.execute("SELECT matchID FROM matchTable ORDER BY matchID DESC")
    try:
        matchIndex = int(cur.fetchone()[0])
    except TypeError:
        matchIndex = -1
    
    ballchasingAPI = ballchasing.Api(ballchasingAPIToken)

    sortedFiles = list(filter(path.isfile, glob(replayFolder + "\*replay")))
    sortedFiles.sort(key=lambda x: path.getmtime(x))
    for file in sortedFiles:
        try:
            matchIndex, playerIndex, error = HandleReplay(file, ballchasingAPI, matchIndex, playerIndex, cur, dbConn)
        except ZeroDivisionError:
            print("zero division error?")
        except ExecError:#Exception as e:
            print(f"Error as E: {e} {type(e)}")
            if pauseOnError: input()
            AddFailedReplay(file)
            error = True
            
        renameFile = file.split('\\'[0])[-1]
        renameFile = renameFile.replace(".replay", "")
        renameFile += f"-{matchIndex}"
        renameFile += ".replay"
        if error:
            move(file, errorFolder + renameFile)
        else:
            move(file, processedReplayFolder + renameFile)
        print("Sleeping")
        sleep(0.5)


    while True:
        newReplay = GetLatestReplay(replayFolder)
        if latestReplay != newReplay or debugMode:
            latestReplay = newReplay
            matchIndex, playerIndex = HandleReplay(latestReplay, ballchasingAPI, matchIndex, playerIndex, cur, dbConn)  
        if debugMode: return
        sleep(5)

continueThruError = True
pauseOnError = True



while True:
    try:
        main()
    except ZeroDivisionError:
        pass
    #except Exception as e:
    except UnboundLocalError as e:
        print(f"Error Type: {type(e)}")
        print(e)
        if pauseOnError: input()
        if not continueThruError: break


    