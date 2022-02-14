import sqlite3
import tkinter as tk

from collections import Counter
from tkinter import ttk

def sign(val):
    if val == 0:
        return 0
    else:
        return 1 if val > 0 else -1


######################
#AnalysisNode(DefaultAnalysisNode, Value)
#
#
#
#
#
#
#
#
###########
allNodes = {"Match" : ["matchID", "gameID", "replayName", "ballchasingLink", "map", "matchType", 
                "teamSize", "playlistID", "durationCalculated", "durationBallchasing", 
                "overtime", "season", "seasonType", "date", "time", "mmr", "nFrames", "orangeScore", "blueScore", 
                "goalSequence", "neutralPossessionTime", "bTimeGround", "bTimeLowAir", "bTimeHighAir", "bTimeBlueHalf", 
                "bTimeOrangeHalf", "bTimeBlueThird", "bTimeNeutralThird", "bTimeOrangeThird", "bTimeNearWall", "bTimeInCorner", 
                "bTimeOnWall", "bAverageSpeed", "bType", "gameMutatorIndex", "tBlueClumped", "tOrangeClumped", "tBlueIsolated", 
                "tOrangeIsolated", "tBluePossession", "tOrangePossession", "replayTagOne", "replayTagTwo", "replayTagThree", 
                "replayTagFour", "replayTagFive", "startPlayerIndex"],
            "Player" : ["playerID", "matchID", "gameID", "pBallchasingID", "pCalculatedId", "pName", "pPlatform", "pTier", 
                "carName", "titleID", "teamColour", "bUsage", "bPerMinute", "bConsumptionPerMinute", "aAmount", 
                "qCollected", "qStolen", "qCollectedBig", "qCollectedSmall", "qStolenBig", "qStolenSmall", "nCollectedBig", 
                "nCollectedSmall", "nStolenBig", "nStolenSmall", "qOverfill", "qOverfillStolen", "qWasted", "tZeroBoost", "tFullBoost", 
                "tBZeroQuarter", "tBQuaterHalf", "tBHalfUpperQuater", "tBUpperQuaterFull", "aSpeed", "aHitDistance", "aDistanceFromCentre", 
                "dTotal", "tSonicS", "tBoostS", "tSlowS", "tGround", "tLowAir", "tHighAir", "tPowerslide", "nPowerslide", "aPowerslideDuration", 
                "aSpeedPercentage", "aDBall", "aDBallPossession", "aDBallNoPossession", "aDMates", "tDefensiveThird", "tNeutralThird", "tOffensiveThird", 
                "tDefensiveHalf", "tOffensiveHalf", "tBehindBall", "tInFrontBall", "tMostBack", "tMostForward", "goalsConcededLast", "tClosestBall", 
                "tFarthestBall", "tCloseBall", "tNearWall", "tInCorner", "tOnWall", "dHitForward", "dHitBackward", "pTime", "turnovers", "turnoversMyHalf", 
                "turnoversTheirHalf", "wonTurnovers", "aPDuration", "aPHits", "qPossession", "demoInflicted", "demoTaken", "score", "goals", 
                "assists", "saves", "shots", "mvp", "shootingP", "totalHits", "totalPasses", "totalDribbles", "totalDribblesConts", 
                "totalAerials", "totalClears", "isKeyboard", "tBallCam", "qCarries", "qFlicks", "totalCarryT", "totalCarryD", "aCarryT", "totalKickoffs", 
                "numGoBoost", "numnGoFollow", "numGoBall", "numFirstTouch", "aBoostUsed", "fiftyWins", "fiftyLosses", "fiftyDraws", "isBot", "partyLeaderID", 
                "ballchasingStartTime", "ballchasingEndTime", "ballchasingBoostTime", "ballchasingStatTime", "calculatedFirstFrame", "calculatedTimeInGame"]}
retrievalNodes = {"Match" : ["matchID", "gameID", "map", "matchType", 
                "teamSize", "durationCalculated", "durationBallchasing", 
                "overtime", "nFrames", "orangeScore", "blueScore", 
                "goalSequence", "neutralPossessionTime", "bTimeGround", "bTimeLowAir", "bTimeHighAir", "bTimeBlueHalf", 
                "bTimeOrangeHalf", "bTimeBlueThird", "bTimeNeutralThird", "bTimeOrangeThird", "bTimeNearWall", "bTimeInCorner", 
                "bTimeOnWall", "bAverageSpeed", "bType", "gameMutatorIndex", "tBlueClumped", "tOrangeClumped", "tBlueIsolated", 
                "tOrangeIsolated", "tBluePossession", "tOrangePossession", "replayTagOne", "replayTagTwo", "replayTagThree", 
                "replayTagFour", "replayTagFive", "startPlayerIndex"],
                  "Player" : ["playerID", "pBallchasingID", "pCalculatedId", "pName", "pPlatform", "pTier", 
                "carName", "titleID", "teamColour", "bUsage", "bPerMinute", "bConsumptionPerMinute", "aAmount", 
                "qCollected", "qStolen", "qCollectedBig", "qCollectedSmall", "qStolenBig", "qStolenSmall", "nCollectedBig", 
                "nCollectedSmall", "nStolenBig", "nStolenSmall", "qOverfill", "qOverfillStolen", "qWasted", "tZeroBoost", "tFullBoost", 
                "tBZeroQuarter", "tBQuaterHalf", "tBHalfUpperQuater", "tBUpperQuaterFull", "aSpeed", "aHitDistance", "aDistanceFromCentre", 
                "dTotal", "tSonicS", "tBoostS", "tSlowS", "tGround", "tLowAir", "tHighAir", "tPowerslide", "nPowerslide", "aPowerslideDuration", 
                "aSpeedPercentage", "aDBall", "aDBallPossession", "aDBallNoPossession", "aDMates", "tDefensiveThird", "tNeutralThird", "tOffensiveThird", 
                "tDefensiveHalf", "tOffensiveHalf", "tBehindBall", "tInFrontBall", "tMostBack", "tMostForward", "goalsConcededLast", "tClosestBall", 
                "tFarthestBall", "tCloseBall", "tNearWall", "tInCorner", "tOnWall", "dHitForward", "dHitBackward", "pTime", "turnovers", "turnoversMyHalf", 
                "turnoversTheirHalf", "wonTurnovers", "aPDuration", "aPHits", "qPossession", "demoInflicted", "demoTaken", "score", "goals", 
                "assists", "saves", "shots", "mvp", "shootingP", "totalHits", "totalPasses", "totalDribbles", "totalDribblesConts", 
                "totalAerials", "totalClears", "isKeyboard", "tBallCam", "qCarries", "qFlicks", "totalCarryT", "totalCarryD", "aCarryT", "totalKickoffs", 
                "numGoBoost", "numnGoFollow", "numGoBall", "numFirstTouch", "aBoostUsed", "fiftyWins", "fiftyLosses", "fiftyDraws", "isBot", "partyLeaderID", 
                "ballchasingStartTime", "ballchasingEndTime", "ballchasingBoostTime", "ballchasingStatTime", "calculatedFirstFrame", "calculatedTimeInGame", "matchID"]}
analysisNodeDictionary = {"default" : {"analysisType" : 0, "accountForDuplicates" : False, "punishDuplicates" : False, "relevancy" : 1, "percentageAccountForValue" : False},
                          "qOverfillStolen" : {"punishDuplicates" : True},
                         }
punishDuplicatesAvg = {"default" : 0.2}

percentageAccountValues = {"default" : [0.7, 0.2]}


tagsDictionary = {}

class ValueNode:
    def __init__(self, name, percentage = False, calculation = False, teamStat = True, default = -1, valueType = "Player", valueRangeType = 0) -> None:
        """Name: Name of Node
           Percentage: Name of Node it is Percentage Of
           Calculation: List, Element 0 is eval string in form "@ + @", where @ are replaced with variables, all other elements are names of variables in calculation
           Team Stat: Whether that stat is relevant to a team/ should be included in the Team Object
           Default: If the fetched value is None, NaN or -1 it is set to this value
           ValueType: What object the node is for
           ValueRangeType: Whether to treat it as a continous curve of values or as a True or False, etc.
           
           Index: Location in retrievalNodes"""
        
        
        self.n = name
        self.p = percentage #name of stat that it is percentage of
        self.c = calculation

        self.tS = teamStat
        self.valueRangeType = valueRangeType
        self.default = default
        self.valueType = valueType
        if name in retrievalNodes[valueType]:
            self.i = retrievalNodes[valueType].index(name)
        else:
            self.i = -1
    def __eq__(self, __o: object) -> bool:
        return self.n == __o.n
    def __repr__(self) -> str:
        output = f"Name: {self.n}\nIndex: {self.i}\nDefault: {self.default}\nPercentage: {self.p}"
        if "rV" in self.__dict__:
            output += f"\nRaw Value: {self.rV}"
        if "v" in self.__dict__:
            output += f"\nValue: {self.v}"
        if "rR" in self.__dict__:
            output += f"\nRaw Relevancy: {self.rR}"
        if "cR" in self.__dict__:
            output += f"\nCalculated Relevancy: {self.cR}"
        if "pos" in self.__dict__:
            output += f"\nPosition: {self.pos}"
        return output
    def GiveValue(s, rawValue, percentageOf = None, calculationValues = None, individualPlayers = None, teamCalculation = False):
        node = ValueNode(s.n, s.p, s.c, s.tS, s.default, s.valueType, s.valueRangeType) 
        node.rawValue = rawValue
        node.percentageOf = percentageOf
        node.calculationValues = calculationValues
        node.individualPlayers = individualPlayers


        if node.rawValue in [None, "NaN", -1]:
            node.calculatedValue = s.default
            return node
        cachedValue = node.rawValue
        if node.c and not teamCalculation:
            if node.c == True:
                cachedValue = calculationValues[0]
            else:
                if calculationValues.count(-1) == len(calculationValues):
                    node.calculatedValue = s.default
                    return node
                else:
                    calculationValues = [x if x != -1 else 0 for x in calculationValues]
                    calculationString = node.c[0]
                    for cValue in calculationValues:
                        calculationString = calculationString.replace("@", str(cValue), 1)
                    cachedValue = eval(calculationString)
            node.rawValue = cachedValue
        if node.p and not teamCalculation:
            if percentageOf != -1:
                if percentageOf == 0:
                    cachedValue /= 1
                else:
                    cachedValue /= percentageOf
            else:
                cachedValue /= 1
        node.calculatedValue = cachedValue
        return node

valueNodes = {"Match" : [ValueNode('overtime', valueType = "Match"), 
                    ValueNode('neutralPossessionTime', percentage = "durationCalculated", valueType = "Match"),
                    ValueNode('bTimeGround', percentage = "durationCalculated", valueType = "Match"),
                    ValueNode('bTimeLowAir', percentage = "durationCalculated", valueType = "Match"),
                    ValueNode('bTimeHighAir', percentage = "durationCalculated", valueType = "Match"),
                    ValueNode('bTimeNeutralThird', percentage = "durationCalculated", valueType = "Match"),
                    ValueNode('bTimeNearWall', percentage = "durationCalculated", valueType = "Match"),
                    ValueNode('bTimeInCorner', percentage = "durationCalculated", valueType = "Match"),
                    ValueNode('bTimeOnWall', percentage = "durationCalculated", valueType = "Match"),
                    ValueNode('bAverageSpeed'),],
              "Player": [ValueNode('carName', teamStat = False, valueRangeType = 1), 
                    ValueNode('bUsage'),
                    ValueNode('bPerMinute'),
                    ValueNode('bConsumptionPerMinute'),
                    ValueNode('aAmount'),
                    ValueNode('qCollected'),
                    ValueNode('qStolen'),
                    ValueNode('qCollectedBig'),
                    ValueNode('qCollectedSmall'),
                    ValueNode('qStolenBig'),
                    ValueNode('qStolenSmall'),
                    ValueNode('nCollectedBig'),
                    ValueNode('nCollectedSmall'),
                    ValueNode('nStolenBig'),
                    ValueNode('nStolenSmall'),
                    ValueNode('qOverfill'),
                    ValueNode('qOverfillStolen'),
                    ValueNode('qWasted'),
                    ValueNode('tZeroBoost', percentage = "ballchasingBoostTime"),
                    ValueNode('tFullBoost', percentage = "ballchasingBoostTime"),
                    ValueNode('tBZeroQuarter', percentage = "ballchasingBoostTime"),
                    ValueNode('tBQuaterHalf', percentage = "ballchasingBoostTime"),
                    ValueNode('tBHalfUpperQuater', percentage = "ballchasingBoostTime"),
                    ValueNode('tBUpperQuaterFull', percentage = "ballchasingBoostTime"),
                    ValueNode('aSpeed'),
                    ValueNode('aHitDistance'),
                    ValueNode('aDistanceFromCentre'),
                    ValueNode('dTotal'),
                    ValueNode('tSonicS', percentage = "ballchasingStatTime"),
                    ValueNode('tBoostS', percentage = "ballchasingStatTime"),
                    ValueNode('tSlowS', percentage = "ballchasingStatTime"),
                    ValueNode('tGround', percentage = "ballchasingStatTime"),
                    ValueNode('tLowAir', percentage = "ballchasingStatTime"),
                    ValueNode('tHighAir', percentage = "ballchasingStatTime"),
                    ValueNode('tPowerslide', percentage = "ballchasingStatTime"),
                    ValueNode('nPowerslide'),
                    ValueNode('aPowerslideDuration'),
                    ValueNode('aSpeedPercentage'),
                    ValueNode('aDBall'),
                    ValueNode('aDBallPossession'),
                    ValueNode('aDBallNoPossession'),
                    ValueNode('aDMates'),
                    ValueNode('tDefensiveThird', percentage = "ballchasingStatTime"),
                    ValueNode('tNeutralThird', percentage = "ballchasingStatTime"),
                    ValueNode('tOffensiveThird', percentage = "ballchasingStatTime"),
                    ValueNode('tDefensiveHalf', percentage = "ballchasingStatTime"),
                    ValueNode('tOffensiveHalf', percentage = "ballchasingStatTime"),
                    ValueNode('tBehindBall', percentage = "ballchasingStatTime"),
                    ValueNode('tInFrontBall', percentage = "ballchasingStatTime"),
                    ValueNode('tMostBack', percentage = "ballchasingStatTime"),
                    ValueNode('tMostForward', percentage = "ballchasingStatTime"),
                    ValueNode('goalsConcededLast', teamStat = False),
                    ValueNode('tClosestBall', percentage = "ballchasingStatTime"),
                    ValueNode('tFarthestBall', percentage = "ballchasingStatTime"),
                    ValueNode('tCloseBall', percentage = "ballchasingStatTime"),
                    ValueNode('tNearWall', percentage = "ballchasingStatTime"),
                    ValueNode('tInCorner', percentage = "ballchasingStatTime"),
                    ValueNode('tOnWall', percentage = "ballchasingStatTime"),
                    ValueNode('dHitForward'),
                    ValueNode('dHitBackward'),
                    ValueNode('pTime', percentage = "ballchasingStatTime"),
                    ValueNode('turnovers'),
                    ValueNode('turnoversMyHalf'),
                    ValueNode('turnoversTheirHalf'),
                    ValueNode('wonTurnovers'),
                    ValueNode('aPDuration'),
                    ValueNode('aPHits'),
                    ValueNode('qPossession'),
                    ValueNode('demoInflicted'),
                    ValueNode('demoTaken'),
                    ValueNode('score'),
                    ValueNode('goals'),
                    ValueNode('assists'),
                    ValueNode('saves'),
                    ValueNode('shots'),
                    ValueNode('mvp'),
                    ValueNode('shootingP'),
                    ValueNode('totalHits'),
                    ValueNode('totalPasses'),
                    ValueNode('totalDribbles'),
                    ValueNode('totalDribblesConts'),
                    ValueNode('totalAerials'),
                    ValueNode('totalClears'),
                    ValueNode('tBallCam', percentage = "ballchasingStatTime"),
                    ValueNode('qCarries'),
                    ValueNode('qFlicks'),
                    ValueNode('totalCarryT', percentage = "ballchasingStatTime"),
                    ValueNode('totalCarryD'),
                    ValueNode('aCarryT'),
                    ValueNode('totalKickoffs'),
                    ValueNode('numGoBoost'),
                    ValueNode('numnGoFollow'),
                    ValueNode('numGoBall'),
                    ValueNode('numFirstTouch'),
                    ValueNode('aBoostUsed'),
                    ValueNode('fiftyWins'),
                    ValueNode('fiftyLosses'),
                    ValueNode('fiftyDraws'),
                    ValueNode("fiftyWinRate", percentage = "totalFifties"),
                    ValueNode("fiftyNotLossRate", percentage = "totalFifties", calculation = ["@ + @", "fiftyWins", "fiftyDraws"]),
                    ValueNode('goalParticipation', percentage = "teamGoals", calculation = ["@ + @", "goals", "assists"]),
                    ValueNode('scoredFirst', calculation = True, valueRangeType = 1)],
              "Team": [ValueNode("maxLead"),
                     ValueNode("maxDeficit"),
                     ValueNode("finalLead"),
                     ValueNode("comeback"),
                     ValueNode("choke")]
}
for nodeType in valueNodes:#Match, Player
    nodeDict = {}
    for node in valueNodes[nodeType]:
        nodeDict[node.n] = node
    valueNodes[nodeType] = nodeDict

class AnalysisNode:
    def __init__(s, valueNode : ValueNode, againstValues = None, typeOfAnalysis = 0, **kwargs) -> None:
        #Account for Duplicates, Punish Duplicates, Relevancy, 
        keywordArgs = ["analysisType", "accountForDuplicates", "punishDuplicates", "relevancy", "percentageAccountForValue"] #Analysis Node Arguments
        s.valueNode = valueNode #Setting Value Node 
        name = valueNode.n #Fetching name for use
        for kArg in keywordArgs: #For argument in keyword Args
            if kArg in kwargs: #If in given values
                s.__dict__[kArg] = kwargs[kArg] 
            elif name in analysisNodeDictionary and kArg in analysisNodeDictionary[name]: #Checks to see if it's in analysisNodeDict
                s.__dict__[kArg] = analysisNodeDictionary[name][kArg]
            else:
                s.__dict__[kArg] = analysisNodeDictionary["default"][kArg] #Sets to default value
        if s.punishDuplicates:
            if name in punishDuplicatesAvg:
                s.punishDuplicates = punishDuplicatesAvg[name]
            else:
                s.punishDuplicates = punishDuplicatesAvg["default"]
        if s.percentageAccountForValue:
            if name in percentageAccountValues:
                s.percentageAccountForValue = percentageAccountValues[name]
            else:
                s.percentageAccountForValue = percentageAccountValues["default"]
        if againstValues:
            s.valueIndex = againstValues.index(valueNode.calculatedValue)
            if typeOfAnalysis == 0:
                match s.analysisType:
                    case 0:
                        average = sum(againstValues) / len(againstValues)
                        s.rawWeight = valueNode.calculatedValue / average

                        if s.percentageAccountForValue:
                            s.rawWeight *= s.percentageAccountForValue[0]
                            
                            weightEffect = valueNode.calculatedValue * s.percentageAccountForValue[1]
                            
                            s.alteredWeight += weightEffect

                        s.equalisedWeight = s.rawWeight - 1
                        s.alteredWeight = s.equalisedWeight
                        if s.punishDuplicates:
                            repeats = againstValues.count(valueNode.calculatedValue) - 1
                            weightEffect = repeats * s.punishDuplicates
                            s.alteredWeight -= weightEffect * sign(s.alteredWeight)
                            



                        s.calculatedWeight = s.equalisedWeight * s.relevancy
                    case 1 | 2:
                        relativeAppearances = againstValues.count(valueNode.calculatedValue) / sum(againstValues.values())
                        s.rawWeight = (1 / pow(relativeAppearances, 0.5))

                        s.alteredWeight = s.rawWeight
                        s.equalisedWeight = s.rawWeight - 1
                        s.calculatedWeight = s.equalisedWeight * s.relevancy
            else:
                match s.analysisType:
                    case 0:
                        pass
                    case 1:
                        pass
                    case 2:
                        pass
class HistoricalNode:
    def __init__(s, name, relevancy, value, againstValue, index, analysisType) -> None:
        s.n = name
        s.r = relevancy
        s.v = value
        s.aV = againstValue
        s.i = index
        s.aT = analysisType
        if s.aT == 0:
            s.cR = value / againstValue
            s.cR -= 0.5
            s.cR *= relevancy
        elif s.aT == 1:
            againstValue : Counter
            try:
                s.cR = againstValue[value] / sum(againstValue.values())
            except ZeroDivisionError as e:
                s.cR = 0.5
            
            s.cR -= 0.5
            s.cR *= relevancy
        elif s.aT == 2:
            try:
                s.cR = againstValue[value] / sum(againstValue.values())
            except ZeroDivisionError as e:
                s.cR = 0.5
            s.cR -= 0.5
            s.cR *= relevancy
        else:
            print("cunt")
class Player:
    def __init__(self, playerList, matchList):
        self.pList = playerList
        self.mL = matchList
        
        self.valueNodes = {}
        
        for node in valueNodes["Player"].values():
            node : ValueNode
            if node.c:
                if node.c == True:
                    match node.n:
                        case "scoredFirst":
                            try:
                                calcVariables = [playerList[0] == matchList[11][0]]
                            except (TypeError, IndexError):
                                calcVariables = [-1]
                else:
                    calcVariables = [x.calculatedValue for x in self.valueNodes.values() if x.n in node.c[1:]]
            else:
                calcVariables = None
                rawValue = playerList[node.i]
            if node.p:
                if node.p in retrievalNodes["Player"]:
                    divValue = playerList[retrievalNodes["Player"].index(node.p)]
                else:
                    match node.p:
                        case "teamGoals":
                            teamGoalsIndex = 10 if playerList[8] == "blue" else 9
                            divValue = matchList[teamGoalsIndex]
                        case "totalFifties":
                            try:
                                divValue = playerList[retrievalNodes["Player"].index("fiftyWins")] + playerList[retrievalNodes["Player"].index("fiftyLosses")] + playerList[retrievalNodes["Player"].index("fiftyDraws")]
                            except TypeError:
                                divValue = -1
                if divValue in [None, "NaN"]:
                    divValue = -1
            else:
                divValue = None       
            self.valueNodes[node.n] = node.GiveValue(rawValue, divValue, calcVariables)
class PlayerHistoric(Player):
    countForHistoric = 3
    def __init__(s, players, intensiveStats = False):
        s.players = players
        s.averageValues = {}
        s.numAppearances = len(players)
        s.iS = intensiveStats
        s.id = players[0].pList[1]
        for stat in valueNodes["Player"].values():
            match stat.valueRangeType:
                case 0:
                    aList = [x.valueNodes[stat.n].calculatedValue for x in players if stat.n in x.valueNodes and x.valueNodes[stat.n].calculatedValue != -1]
                    try:
                        aSum = sum(aList)
                    except TypeError as e:
                        print(aList)
                        raise e
                    try:
                        aAvg = aSum / len(aList)
                    except ZeroDivisionError:
                        aAvg = -1

                    s.averageValues[stat.n] = [aAvg, aList]
                case 1 | 2:
                    allValues = [p.valueNodes[stat.n].calculatedValue for p in players if stat.n in p.valueNodes]
                    s.averageValues[stat.n] = Counter(allValues)
                    
        if intensiveStats:
            raise NotImplementedError()
            allIDs = [x.mL[0] for x in players]
            allPlayers = [x for x in intensiveStats if x.mL[0] in allIDs]

            s.aN = {}

            for stat in PlayerHistoric.analysisNodes:
                if stat.aT != 0:
                    continue
                otherPStats = [x.nodes[stat.n].v for x in allPlayers]
                aAvg = sum(otherPStats) / len(otherPStats)
                s.aN[stat.n] = aAvg
    def __eq__(self, o: object) -> bool:
        if isinstance(o, PlayerHistoric):
            return self.id == o.id
        else:
            return self.id == o
    def GetHistoricPlayer(playerObject : Player, allPlayers):
        playerAppearances = [x for x in allPlayers if x.pList[0] == playerObject.pList[0]]
        if len(playerAppearances) > PlayerHistoric.countForHistoric:
            return PlayerHistoric(playerAppearances)
        return False
class Team:
    def __init__(self, players, matchList) -> None:
        self.players = players
        self.valueNodes = {}
        self.mL = matchList
        playersValues = [list(x.valueNodes.values()) for x in players]
        for i, node in enumerate(valueNodes["Player"].values()):
            node : ValueNode
            if not node.tS:
                continue
            try:
                playerStatValues = [x[i].calculatedValue for x in playersValues if x[i].calculatedValue != -1]
                if len(playerStatValues) == 0:
                    calculatedValue = -1
                else:
                    calculatedValue = sum(playerStatValues) / len(playerStatValues)
            except TypeError as e:
                match node.n:
                    case "scoredFirst":
                        playerStatValues = [x[i].calculatedValue for x in playersValues]
                        calculatedValue = True in playerStatValues
                    case _:
                        print("Error")
                        print(node.n)
                        print([x[i].v for x in playersValues if x[i].v not in [-1, None]])
                        raise e
            self.valueNodes[node.n] = node.GiveValue(calculatedValue, individualPlayers = playerStatValues, teamCalculation = True)

        teamPlayerIDs = [x.pList[0] for x in players]

        goalSequence = matchList[11]
        if goalSequence:
            goalSequence = goalSequence.split(",")
            currentScores = [0]
            for goal in goalSequence:
                currentScore = currentScores[-1]
                if int(goal) in teamPlayerIDs:
                    currentScore += 1
                else:
                    currentScore -= 1
                currentScores.append(currentScore)

            maxLeadNode = valueNodes["Team"]["maxLead"].GiveValue(max(currentScores))
            minLeadNode = valueNodes["Team"]["maxDeficit"].GiveValue(min(currentScores))
            finalLeadNode = valueNodes["Team"]["finalLead"].GiveValue(currentScores[-1])

            comebackNode = valueNodes["Team"]["comeback"].GiveValue(minLeadNode.calculatedValue if minLeadNode.calculatedValue < 0 and finalLeadNode.calculatedValue > 0 else 0)
            chokeNode = valueNodes["Team"]["choke"].GiveValue(maxLeadNode.calculatedValue if maxLeadNode.calculatedValue > 1 and finalLeadNode.calculatedValue < 0 else 0)
            leadNodes = [maxLeadNode, minLeadNode, finalLeadNode, comebackNode, chokeNode]
            for node in leadNodes:
                self.valueNodes[node.n] = node
class TeamHistoric(Team):
    countForHistoric = 3 
class Match:
    def __init__(self, matchList) -> None:
        self.mL = matchList
        self.valueNodes = {}
        for node in valueNodes["Match"].values():
            rawValue = matchList[node.i]
            if node.p:
                divValue = matchList[retrievalNodes["Match"].index(node.p)]
            else:
                divValue = None
            self.valueNodes[node.n] = node.GiveValue(rawValue, divValue)

    def __repr__(self) -> str:
        output = ""
        for node in self.nodes:
            output += f"{node} : {self.nodes[node]}\n"
        return output

class ReplayAnalysis:
    def __init__(self, loadReplays = True, tagsToLoad = None):
        #self.dbFile = r"d:\Users\tom\Documents\Visual Studio Code\Python Files\RocketReplayAnalysis\RocketReplayAnalysis\Database\replayDatabase.db"
        self.dbFile = r"D:\Users\tom\Documents\Programming Work\Python\RocketReplayAnalysis\Database\replayDatabase.db"
        self.CreateConnection(self.dbFile)
        self.replays = []
        if loadReplays:
            self.LoadReplays(tagsToLoad)
    def CreateConnection(self, dbFile):
        print(f"Connected to {dbFile}")
        self.conn = sqlite3.connect(dbFile)
        self.c = self.conn.cursor()
        print(f"SQLite3 Version: {sqlite3.version}")
    def GetReplay(self, replayID, getTeams = True):
        if replayID < 0:
            executeSTR = f"SELECT matchID FROM matchTable ORDER BY matchID DESC;"
            self.c.execute(executeSTR)
            replayID *= -1
            replayID = self.c.fetchmany(replayID)[replayID - 1][0]
        executeSTR = f"SELECT {', '.join(Match.retrievalNodes)} from matchTable WHERE matchID = {replayID}"
        self.c.execute(executeSTR)
        matchDetails = self.c.fetchone()

        executeSTR = f"SELECT {', '.join(Player.retrievalNodes)} from playerMatchTable WHERE matchID = {replayID}"
        self.c.execute(executeSTR)

        players = [x for x in self.c.fetchall()]
        if getTeams:
            players = [Player(x, matchDetails) for x in players]
            return Match(matchDetails), players, [Team([x for x in players if x.pList[8] == "blue"], matchDetails), Team([x for x in players if x.pList[8] == "orange"], matchDetails)]
        else:
            return Match(matchDetails), [Player(x, matchDetails) for x in players]    
    def FetchGame(self, replayID):
        match = [x for x in self.matches if x.mL[0] == replayID][0]
        players = [x for x in self.players if x.mL[0] == replayID]
        teams = [x for x in self.teams if x.mL[0] == replayID]

        historicPlayers = []
    def LoadReplays(self, tagsToLoad = None, num = -1, loadTeams = True, instantiateHistoricPlayers = True, instantiateHistoricTeams = True):
        tagsSTR = ""
        if tagsToLoad:
            tagsSTR = f""" WHERE {'and'.join([f'{x[0]} = "{x[1]}"' if isinstance(x[1], str) else f'{x[0]} = {x[1]}' for x in tagsToLoad])}"""
        executeSTR = f"SELECT matchID FROM matchTable ORDER BY matchID DESC{tagsSTR};"

        self.c.execute(executeSTR)
        if num < 1:
            matchIDs = [x[0] for x in self.c.fetchall()]
        else:
            matchIDs = [x[0] for x in self.c.fetchmany(num)]
        matchIDsSTR = f"({', '.join([str(x) for x in matchIDs])})"
        matchNodesToSelectSTR = ", ".join(retrievalNodes["Match"])
        playerNodesToSelectSTR = ", ".join(retrievalNodes["Player"])

        self.c.execute(f"SELECT {matchNodesToSelectSTR} FROM matchTable WHERE matchID in {matchIDsSTR}")
        matchLists = self.c.fetchall()

        self.c.execute(f"SELECT {playerNodesToSelectSTR} FROM playerMatchTable WHERE matchID in {matchIDsSTR}")
        playerLists = self.c.fetchall()
        self.matches = []
        self.matches = [Match(x) for x in matchLists]
        self.matchesDict = {x.mL[0] : x for x in self.matches}
        self.players = []
        for player in playerLists:
            self.players.append(Player(player, self.matchesDict[player[-1]].mL))
        self.teamsD = {}
        if loadTeams:
            for player in self.players:
                try:
                    self.teamsD[player.pList[-1]][player.pList[8]].append(player)
                except KeyError:
                    self.teamsD[player.pList[-1]] = {}
                    self.teamsD[player.pList[-1]][player.pList[8]] = [player]
            self.teamsPlayers = []
            for players in self.teamsD.values():
                try:
                    self.teamsPlayers.append(players["orange"])
                except KeyError:
                    pass
                try:
                    self.teamsPlayers.append(players["blue"])
                except KeyError:
                    pass
            self.teams = []
            for team in self.teamsPlayers:
                self.teams.append(Team(team, team[0].mL))
        if instantiateHistoricPlayers:
            self.historicPlayers = []
            playersDict = {}
            for player in self.players:
                id = player.pList[1]
                if id in playersDict:
                    playersDict[id] += 1
                else:
                    playersDict[id] = 1
            historicDict = {}
            for player in self.players:
                id = player.pList[1]
                if playersDict[id] >= PlayerHistoric.countForHistoric:
                    if id in historicDict:
                        historicDict[id].append(player)
                    else:
                        historicDict[id] = [player]
            for hPlayer in historicDict.values():
                self.historicPlayers.append(PlayerHistoric(hPlayer))
        if instantiateHistoricTeams:
            pass
    def CompareReplaySelf(s, gamePlayers, gameTeams):
        playerStats = {}
        for statName in valueNodes["Player"]:
            allStats = [x.valueNodes[statName].calculatedValue for x in gamePlayers] #Get All Player Stats
            allStats = [x for x in allStats if x != -1] #Remove Invalid Values
            if len(allStats) == 0:
                continue
            statAverage = sum(allStats) / len(allStats)
            for singlePlayer in gamePlayers:
                pass


    
    
    
    def _AnalyseNode_(self, analyseNode, nodesList, aType = "top", extraTopRelevance = 5, onlyTags = False):
        """Deprecated"""
        
        
        #type : top%, average
        if isinstance(nodesList, str):
            nodeType = nodesList
            nodesList = self.__dict__[nodesList]

        matchTags = []
        if onlyTags == True:
            matchTags = analyseNode.mL[-6:-2]
        elif onlyTags:
            matchTags = onlyTags
        matchTags = [x for x in matchTags if x not in [0, None, "NULL"]]
        for i, tag in enumerate(matchTags):
            nodesList = [x for x in nodesList if x.mL[-6 + i] == tag]
        for node in analyseNode.nodes.values():
            if not node:
                del node
            if node.v in [-1]:
                node.rR = 0
                node.cR = 0
                node.pos = "N/A"
            else:
                match node.aT:
                    case 0:
                        nodesAll = [xPlayer.nodes[node.n].v for xPlayer in nodesList if xPlayer.nodes[node.n].v not in [-1, "NaN", None]]
                        if aType == "top":
                            nodesListInsert = nodesAll
                            nodesListInsert.append(node.v)
                            try:
                                nodesListInsert.sort()
                            except TypeError as e:
                                print(node.n)
                                print(nodesListInsert)
                                raise e

                            valueIndex = nodesListInsert.index(node.v)
                            listLength = len(nodesListInsert)
                            node.pos = (valueIndex, listLength)
                            node.rR = valueIndex / (listLength - 1)
                            node.cR = node.rR
                            node.cR -= 0.5
                            if node.aFD:
                                node.cR += nodesListInsert.count(node.v) / (listLength - 1)
                            if node.pD:
                                node.cR *= float(node.pD) * (1 - nodesListInsert.count(node.v) / listLength)
                            if valueIndex < extraTopRelevance or listLength - extraTopRelevance <= valueIndex:
                                node.cR *= 1.1 + min(valueIndex, listLength - valueIndex - 1) * 0.02

                            node.cR *= 2
                            if "top" in node.r:
                                node.cR *= node.r["top"]

                        elif aType == "average":
                            nodesAverage = sum(nodesAll) / len(nodesAll)

                            node.rR = node.v / nodesAverage
                            node.cR = node.rR
                            node.cR -= 1

                            if node.v > max(nodesAll) or node.v < min(nodesAll):
                                node.cR *= 1.2
                            if "average" in node.r:
                                node.cR *= node.r["average"]
                            nodesAll.append(node.v)
                            nIndex = nodesAll.index(node.v)

                            node.pos = (nIndex, len(nodesAll))
                        else:
                            raise NotImplementedError(f"What type: {type}")
                    case _:
                        node.rR = 0
                        node.cR = 0
                        node.pos = "N/A"
        analyseNode.againstNodes = False
        if nodeType == "players":
            if analyseNode.pList[1] in self.historicPlayers:
                hPlayer = self.historicPlayers[self.historicPlayers.index(analyseNode.pList[1])]
                analyseNode.againstNodes = []
                for node in analyseNode.nodes.values():
                    if node.aT == 0:
                        nList = hPlayer.n[node.n][1]
                        nList.append(node.v)
                        sList = sorted(nList, reverse = True)

                        nIndex = [sList.index(node.v) + 1, len(sList)]
                        againstValues = hPlayer.n[node.n][0]
                    else:
                        nIndex = hPlayer.n[node.n][node.v] / sum(hPlayer.n[node.n].values())
                        try:
                            againstValues = hPlayer.n[node.n]
                        except KeyError:
                            againstValues = Counter([])

                    
                    analyseNode.againstNodes.append(HistoricalNode(node.n, node.r[nodeType] if nodeType in node.r else 1, node.v, againstValues, nIndex, node.aT))

        elif nodeType == "Team":
            pass

        return analyseNode

class ReplayGUI:
    def __init__(s) -> None:
        s.w = tk.Tk()
        s.w.title("Rocket Replay Analysis")
        s.w.geometry("1000x400")

        s.tagsEntry = tk.Entry(s.w)
        s.tagsEntry.insert(0, "Enter Tags")
        s.tagsEntry.grid(row = 0, column = 0)

        s.tagsButton = tk.Button(s.w, text = "Enter", command = s.EnterTags)
        s.tagsButton.grid(row = 0, column = 1)

        s.w.mainloop()

    def EnterTags(s):
        tags = s.tagsEntry.get()
        if tags != "Enter Tags":
            tags = tags.split(",")
        else:
            tags = None
        s.analysisEngine = ReplayAnalysis(tagsToLoad = tags)

        s.tagsEntry.destroy()
        s.tagsButton.destroy()
        
        s.CreateGameEntryWindow()
    
    def CreateGameEntryWindow(s):
        s.idEntry = tk.Entry(s.w)
        s.idEntry.insert(0, "Enter Id(s)")
        s.idEntry.grid(row = 0, column = 0)

        s.idButton = tk.Button(s.w, text = "Enter", command = s.EnterIDs)
        s.idButton.grid(row = 0, column = 1)


    def EnterIDs(s):
        gameIDs = s.idEntry.get()
        gameIDs = [int(x) for x in gameIDs.split(",")]
        analysisType = "top"

        if len(gameIDs) == 1:
            match, players, teams = s.analysisEngine.GetReplay(gameIDs[0])
            matchAnalysed = s.analysisEngine.AnalyseNode(match, "matches")
            playersAnalysed = []
            for player in players:
                playersAnalysed.append(s.analysisEngine.AnalyseNode(player, "players"))
            teamsAnalysed = []
            for team in teams:
                teamsAnalysed.append(s.analysisEngine.AnalyseNode(team, "teams"))
            
            matchNodes = [x for x in matchAnalysed.nodes.values()]
            matchNodes.sort(reverse = True, key = lambda x : abs(x.cR))

            playersNodes = [[x for x in y.nodes.values()] for y in playersAnalysed]
            playersNodes = [sorted(x, reverse = True, key = lambda x : abs(x.cR)) for x in playersNodes]

            playersHNodes = [[x for x in y.againstNodes] for y in playersAnalysed if y.againstNodes]
            playersHIDs = [y.pList[3] for y in playersAnalysed if y.againstNodes]
            playersHNodes = [sorted(x, reverse = True, key = lambda x : abs(x.cR)) for x in playersHNodes]

            teamsNodes = [[x for x in y.nodes.values()] for y in teamsAnalysed]
            teamsNodes = [sorted(x, reverse = True, key = lambda x : abs(x.cR)) for x in teamsNodes]
        else:
            match, players, teams = s.analysisEngine.GetReplay(gameIDs[0])
            allDetails = [s.analysisEngine.GetReplay(x) for x in gameIDs[1:]]
            aMatches, aPlayers, aTeams = []
            for detail in allDetails:
                aMatches.append(detail[0])
                aPlayers.append(detail[1])
                aTeams.append(detail[2])
            
            matchAnalysed = s.analysisEngine.AnalyseNode(match, aMatches, aType = "average")

            playersAnalysed = []
            for player in players:
                playersAnalysed.append(s.analysisEngine.AnalyseNode(player, aPlayers, aType = "average"))
            teamsAnalysed = []
            for team in teams:
                teamsAnalysed.append(s.analysisEngine.AnalyseNode(team, aTeams, aType = "average"))
            
            matchNodes = [x for x in matchAnalysed.nodes.values()]
            matchNodes.sort(reverse = True, key = lambda x : abs(x.cR))

            playersNodes = [[x for x in y.nodes.values()] for y in playersAnalysed]
            playersNodes = [sorted(x, reverse = True, key = lambda x : abs(x.cR)) for x in playersNodes]

            playersHNodes = [[x for x in y.againstNodes] for y in playersAnalysed if y.againstNodes]
            playersHIDs = [y.pList[3] for y in playersAnalysed if y.againstNodes]
            playersHNodes = [sorted(x, reverse = True, key = lambda x : abs(x.cR)) for x in playersHNodes]

            teamsNodes = [[x for x in y.nodes.values()] for y in teamsAnalysed]
            teamsNodes = [sorted(x, reverse = True, key = lambda x : abs(x.cR)) for x in teamsNodes]

        s.GenerateAnalysedNodesGUI(matchNodes, playersNodes, teamsNodes, analysisType, players, teams, [playersHNodes, playersHIDs])
    
    def CreateTree(s, values, window, aType, columnIDs = ("name", "tag", "relevancy", "accountForDuplicates", "percentage",
                               "rawValue", "value", "rawRelevancy", "calculatedRelevancy", "pos"), 
                              columnNames = ("Name", "Tag", "Relevancy", "Account for Duplicates", "Percentage",
                               "Raw Value", "Value", "Raw Relevancy", "Calculated Relevancy", "Position"),
                              columnWidths = (120, 100, 70, 70, 100, 100, 100, 100, 120, 100), historical = False):
        tree = ttk.Treeview(window, columns = columnIDs, show = "headings")

        tree.grid(column = 0, row = 0)

        scrollBar = ttk.Scrollbar(window, orient = tk.VERTICAL, command = tree.yview)

        tree.configure(yscroll = scrollBar.set)

        scrollBar.grid(column = 1, row = 0)

        for i in range(len(columnIDs)):
            tree.heading(columnIDs[i], text = columnNames[i])
            tree.column(tree["columns"][i], width = columnWidths[i])
        for node in values:
            if not historical:
                tableV = [node.n, node.t, node.r[aType] if aType in node.r else 1, node.aFD, node.dV, node.rV, node.v, node.rR, node.cR, node.pos]
            else:
                tableV = [node.n, node.r, node.v, node.aV, node.i, node.aT, node.cR]
            tableV = [round(x, 2) if isinstance(x, float) else x for x in tableV]
             
            tree.insert("", tk.END, values = tableV)
        
        return tree, scrollBar

    def GenerateAnalysedNodesGUI(s, mNodes, pNodes, tNodes, aType, players, teams, playersHNodes = False):
        s.DeleteIDEntries()

        s.tabParent = ttk.Notebook(s.w)
        s.matchTab = ttk.Frame(s.tabParent)

        s.playerTabs = [ttk.Frame(s.tabParent) for _ in range(len(pNodes))]
        if playersHNodes:
            s.playerHistoricalTabs = [ttk.Frame(s.tabParent) for _ in playersHNodes[0]]
        else:
            s.playerHistoricalTabs = []

        s.teamTabs = [ttk.Frame(s.tabParent) for _ in range(len(tNodes))]

        print("Creating Tree")
        s.matchTree, s.matchScrollBar = s.CreateTree(mNodes, s.matchTab, aType)

        s.tabParent.add(s.matchTab, text= "Match")


        s.playerTrees = []
        s.playerScrollBars = []
        for i, playerTab in enumerate(s.playerTabs):
            playerTree, scrollBar = s.CreateTree(pNodes[i], playerTab, aType)
            s.playerTrees.append(playerTree)
            s.playerScrollBars.append(scrollBar)

            name = players[i].pList[3]
            s.tabParent.add(playerTab, text = name)
        
        s.playerHistoricalTrees = []
        s.playerHistoricalScrollBars = []

        for i, playerHistoricalTab in enumerate(s.playerHistoricalTabs):
            playerHTree, scrollBar = s.CreateTree(playersHNodes[0][i], playerHistoricalTab, "avg",
                                                  columnIDs = ("name", "relevancy", "value", "againstValue", "index", "analysisType",  "calculatedRelevancy"),
                                                  columnNames = ("Name", "Relevancy", "values", "Against Values", "Index", "AnalysisType", "Calculated Relevancy"), historical = True)
            s.playerHistoricalTrees.append(playerHTree)
            s.playerHistoricalScrollBars.append(scrollBar)

            name = f"{playersHNodes[1][i]} Historical"
            s.tabParent.add(playerHistoricalTab, text = name)

        s.teamTrees = []
        s.teamScrollBars = []
        for i, teamTab in enumerate(s.teamTabs):
            teamTree, scrollBar = s.CreateTree(tNodes[i], teamTab, aType)
            s.teamTrees.append(teamTree)
            s.teamScrollBars.append(scrollBar)


            teamColour = teams[i].players[0].pList[8]
            s.tabParent.add(teamTab, text = teamColour)

        s.tabParent.grid(column = 0, row = 0)

        
        print("Created Tree")    
    
    def DeleteIDEntries(s):
        s.idEntry.destroy()
        s.idButton.destroy()

if __name__ == "__main__":
    gui = ReplayGUI()