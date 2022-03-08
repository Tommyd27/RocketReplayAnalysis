import sqlite3

from string import ascii_letters
from collections import Counter
from tkinter import ttk
from os import remove

import kivy
kivy.require('2.1.0') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.label import Label

def RoundToX(num, base):
    return base * round(num / base)
def CalculateMedian(values, medianType = 0.5, sort = True):
    lenValues = len(values)
    midValue = (lenValues + 1) * medianType
    if sort:
        values.sort()
    if midValue % 1 == 0:
        return values[int(midValue)]
    else:
        midValue = int(midValue)
        return (values[midValue] + values[midValue + 1]) / 2
def CalculateStandardDeviation(values, mean = False):
    lenValues = len(values)
    if not mean:
        mean = sum(values) / lenValues
    sumSquared = sum([x ** 2 for x in values])

    variation = (sumSquared / lenValues) - mean ** 2
    standardDeviation = variation ** 0.5

    return standardDeviation   
def sign(val):
    if val == 0:
        return 0
    else:
        return 1 if val > 0 else -1


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
                          "carName" : {"analysisType" : 1},
                          "scoredFirst" : {"analysisType" : 2},
                          
                         }
punishDuplicatesAvg = {"default" : 0.2}
statNodes = {}
percentageAccountValues = {"default" : [0.7, 0.2]}


tagsDictionary = {}

class ValueNode:
    def __init__(self, name, percentage = False, calculation = False, teamStat = True, default = -1, valueType = "Player", valueRangeType = 0, tag = None) -> None:
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
        
        self.tag = tag
    def __eq__(self, __o: object) -> bool:
        return self.n == __o.n
    def __repr__(s) -> str:
        output = f"Name: {s.n}, Percentage: {s.p}"
        if "rawValue" in s.__dict__:
            output += f", Raw Value: {s.rawValue}, Percentage Of: {s.percentageOf}, Calculated Value: {s.calculatedValue}"
        return output
    def GiveValue(s, rawValue, percentageOf = None, calculationValues = None, individualPlayers = None, teamCalculation = False):
        node = ValueNode(s.n, s.p, s.c, s.tS, s.default, s.valueType, s.valueRangeType, s.tag) 
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
                cachedValue = -1
        node.calculatedValue = cachedValue
        return node
class StatNode:
    def __init__(self, valueNode : ValueNode, values) -> None:
        self.name = valueNode.n
        self.valueNode = valueNode
        self.values = [x for x in values if x.calculatedValue != -1]
        self.numValues = len(self.values)
        self.calculatedValues = [x.calculatedValue for x in self.values]

        self.CalculateStats(self.calculatedValues)

        if valueNode.p:
            self.rawValues = [x.rawValue for x in self.values]
            self.CalculateStats(self.rawValues, "raw")        
    def CalculateStats(self, values, prefix = ""):
        values.sort()
        name = self.valueNode.n
        if self.valueNode.valueRangeType == 0:
            self.__dict__[f"{prefix}Mean"] = sum(values) / len(values)
            self.__dict__[f"{prefix}Quartiles"] = [CalculateMedian(values, x, False) for x in (0.25, 0.5, 0.75)]
            self.__dict__[f"{prefix}Mode"] = max(values, key = values.count)
            self.__dict__[f"{prefix}ValuesCounter"] = Counter(values)
            self.__dict__[f"{prefix}StandardDeviation"] = CalculateStandardDeviation(values, self.__dict__[f"{prefix}Mean"])
            try:
                groupValue = statNodes[name]["groupValue"]
            except KeyError:
                if self.__dict__[f"{prefix}Quartiles"][1] > 10:
                    groupValue = round(0.1 * (self.__dict__[f"{prefix}Quartiles"][2] - self.__dict__[f"{prefix}Quartiles"][0]))
                elif self.__dict__[f"{prefix}Quartiles"][1] > 1:
                    #groupValue = round(0.1 * (self.__dict__[f"{prefix}Quartiles"][2] - self.__dict__[f"{prefix}Quartiles"][0]), 2)
                    groupValue = round(0.1 * (self.__dict__[f"{prefix}Quartiles"][2] - self.__dict__[f"{prefix}Quartiles"][0]), 1)
                else:
                    groupValue = 0.01
                if groupValue == 0:
                    print(name)
                    print(values)
                    print(self.rawQuartiles)
                    print(self.__dict__[f"{prefix}Quartiles"])
                    print(prefix)
                    print(0.1 * (self.__dict__[f"{prefix}Quartiles"][2] - self.__dict__[f"{prefix}Quartiles"][0]))
                    input()  
            self.__dict__[f"{prefix}GroupValue"] = groupValue
            self.__dict__[f"{prefix}GroupedValues"] = [RoundToX(x, groupValue) for x in values]
            self.__dict__[f"{prefix}GroupedMode"] = max(self.__dict__[f"{prefix}GroupedValues"], key = self.__dict__[f"{prefix}GroupedValues"].count)
            self.__dict__[f"{prefix}GroupedValuesCounter"] = Counter(self.__dict__[f"{prefix}GroupedValues"])
        else:
            counterValues = Counter(values)
            self.__dict__[f"{prefix}Mode"] = max(counterValues, key = lambda x : counterValues[x])
            self.__dict__[f"{prefix}Mean"] = self.__dict__[f"{prefix}Mode"]
            self.__dict__[f"{prefix}ValuesCounter"] = counterValues
    def OutputValuesStr(s, prefix = ""):
        output = "\n"
        
        if s.valueNode.valueRangeType == 0:
            output += f"\nMean : {round(s.__dict__[f'{prefix}Mean'], 2)}"
            output += f"\nMode : {round(s.__dict__[f'{prefix}Mode'], 2)}"
            output += f"\nQuartiles: {[round(x, 2) for x in s.__dict__[f'{prefix}Quartiles']]}"
            output += f"\nStandard Deviation: {round(s.__dict__[f'{prefix}StandardDeviation'], 2)}"
            output += f"\nGrouped Mode: {round(s.__dict__[f'{prefix}GroupedMode'], 2)}"
            output += f"\nGroup Value: {round(s.__dict__[f'{prefix}GroupValue'], 2)}"
        else:
            output += f"\nMean : {s.__dict__[f'{prefix}Mean']}"
            output += f"\nMode : {s.__dict__[f'{prefix}Mode']}"
        return output
    def __repr__(s) -> str:
        output = f"{s.name.title()}:"
        output += f"\nAnalysis Type : {s.valueNode.valueRangeType}"
        output += s.OutputValuesStr()
        if s.valueNode.p:
            output += s.OutputValuesStr("raw")
        return output
""""""""""""""""""""""""""""""""""""""""""""""""
valueNodes = {"Match" : [ValueNode('overtime', valueType = "Match"), 
                    ValueNode('neutralPossessionTime', percentage = "durationCalculated", valueType = "Match"),
                    ValueNode('bTimeGround', percentage = "durationCalculated", valueType = "Match"),
                    ValueNode('bTimeLowAir', percentage = "durationCalculated", valueType = "Match"),
                    ValueNode('bTimeHighAir', percentage = "durationCalculated", valueType = "Match"),
                    ValueNode('bTimeNeutralThird', percentage = "durationCalculated", valueType = "Match"),
                    ValueNode('bTimeNearWall', percentage = "durationCalculated", valueType = "Match"),
                    ValueNode('bTimeInCorner', percentage = "durationCalculated", valueType = "Match"),
                    ValueNode('bTimeOnWall', percentage = "durationCalculated", valueType = "Match"),
                    ValueNode('bAverageSpeed', valueType= "Match"),],
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
    valuesForOutput = ["rawWeight", "alteredWeight", "equalisedWeight", "calculatedWeight"]
    valueValuesForOutput = ["rawValue", "percentageOf", "calculationValues", "calculatedValue"]
    def __init__(s, valueNode : ValueNode, againstValues = None, typeOfAnalysis = 0, **kwargs) -> None:
        #Account for Duplicates, Punish Duplicates, Relevancy, 
        keywordArgs = ["analysisType", "accountForDuplicates", "punishDuplicates", "relevancy", "percentageAccountForValue"] #Analysis Node Arguments
        s.valueNode = valueNode #Setting Value Node 
        s.againstValue = -1
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
        if valueNode.calculatedValue == -1:
            s.rawWeight, s.alteredWeight, s.equalisedWeight, s.calculatedWeight = -1, -1, -1, -1
            return
        
        if againstValues:
            s.valueIndex = againstValues.index(valueNode.calculatedValue)
            match s.analysisType:
                case 0:
                    if typeOfAnalysis == 0:
                        try:
                            average = sum(againstValues) / len(againstValues)
                        except TypeError as e:
                            print(againstValues)
                            raise e
                        s.againstValue = average
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
                    else:
                        "magic here"
                case 1 | 2:
                    relativeAppearances = againstValues.count(valueNode.calculatedValue) / len(againstValues)
                    s.rawWeight = (1 / pow(relativeAppearances, 0.5))

                    s.alteredWeight = s.rawWeight
                    s.equalisedWeight = s.rawWeight - 1
                    s.calculatedWeight = s.equalisedWeight * s.relevancy
    def __repr__(s) -> str:
        output = f"{s.valueNode}, Raw Weight: {s.rawWeight}, Calculated Weight: {s.calculatedWeight}"
        return output
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

        self.name = playerList[3]
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
    def __init__(s, players, intensiveStats = True):
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
        ["matchID", "gameID", "map", "matchType", 
                "teamSize", "durationCalculated", "durationBallchasing", 
                "overtime", "nFrames", "orangeScore", "blueScore", 
                "goalSequence", "neutralPossessionTime", "bTimeGround", "bTimeLowAir", "bTimeHighAir", "bTimeBlueHalf", 
                "bTimeOrangeHalf", "bTimeBlueThird", "bTimeNeutralThird", "bTimeOrangeThird", "bTimeNearWall", "bTimeInCorner", 
                "bTimeOnWall", "bAverageSpeed", "bType", "gameMutatorIndex", "tBlueClumped", "tOrangeClumped", "tBlueIsolated", 
                "tOrangeIsolated", "tBluePossession", "tOrangePossession", "replayTagOne", "replayTagTwo", "replayTagThree", 
                "replayTagFour", "replayTagFive", "startPlayerIndex"]
        ["playerID", "pBallchasingID", "pCalculatedId", "pName", "pPlatform", "pTier", 
                "carName", "titleID", "teamColour", "bUsage", "bPerMinute", "bConsumptionPerMinute", "aAmount"]            
        if intensiveStats:
            s.goalSequencesDictionary = {}
            for playerMatch in players:
                colour = playerMatch.mL[8]
                orangeWin = playerMatch.mL[9] > playerMatch.mL[10]
                win = int(orangeWin if colour == "orange" else not orangeWin)
                try:
                    goalSequence = [int (x) for x in playerMatch.mL[11].split(",")]
                except (TypeError, AttributeError):
                    continue
                except ValueError:
                    print(f"Invalid Goal Sequence Initiation: {playerMatch.mL[11]}")
                    continue
                teamSize = playerMatch.mL[4]
                if len(goalSequence) == 0:
                    print(f"Invalid Goal Sequence Len: {goalSequence}")
                    continue
                if goalSequence[0] > 8:
                    print(f"Goal Sequence IDs out of Bounds: {goalSequence}")
                    continue
                if colour == "orange":
                    goalSequence = [0 if x > teamSize else 1 for x in goalSequence]
                else:
                    goalSequence = [0 if x <= teamSize else 1 for x in goalSequence]
                #0 a goal for you, 1 a goal for them
                currentScore = [0, 0]
                for goal in goalSequence:
                    currentScore[goal] += 1
                    try:
                        s.goalSequencesDictionary[str(currentScore)][win] += 1
                    except KeyError:
                        s.goalSequencesDictionary[str(currentScore)] = [0, 0]
                        s.goalSequencesDictionary[str(currentScore)][win] += 1
                    except TypeError as e:
                        print(s.goalSequencesDictionary)
                        print(s.goalSequencesDictionary[currentScore])
                        print(s.goalSequencesDictionary[currentScore][win])
                        print(currentScore)
                        print(win)
                        raise e
                
                


            return
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
        self.colour = players[0].pList[8]
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
    def __init__(self, loadReplays = True, args = None):
        self.dbFile = r"d:\Users\tom\Documents\Visual Studio Code\Python Files\RocketReplayAnalysis\RocketReplayAnalysis\Database\replayDatabase.db"
        #self.dbFile = r"D:\Users\tom\Documents\Programming Work\Python\RocketReplayAnalysis\Database\replayDatabase.db"
        self.CreateConnection(self.dbFile)
        self.replays = []

        self.altdbFile = r"D:\Users\tom\Documents\Programming Work\Python\RocketReplayAnalysis\Database\analysisOutputDatabase.db"
        #self.altdbFile = r"d:\Users\tom\Documents\Visual Studio Code\Python Files\RocketReplayAnalysis\RocketReplayAnalysis\Database\analysisOutputDatabase.db"
        #self.altdbFile = ":memory:"
        self.altConn = False
        if loadReplays:
            self.LoadReplays(args)
    def CreateConnection(self, dbFile):
        print(f"Connected to {dbFile}")
        self.conn = sqlite3.connect(dbFile)
        self.c = self.conn.cursor()
        print(f"SQLite3 Version: {sqlite3.version}")
    def CreateAltConnection(self, dbFile, delete = True):
        print(f"Creating Alternate Connection to {dbFile}")
        if delete:
            remove(dbFile)
            f = open(dbFile, "w")
            f.close()
        self.altConn = sqlite3.connect(dbFile)
        self.altC = self.altConn.cursor()
    def GetReplay(self, replayID, getTeams = True):
        if replayID < 0:
            executeSTR = f"SELECT matchID FROM matchTable ORDER BY matchID DESC;"
            self.c.execute(executeSTR)
            replayID *= -1
            replayID = self.c.fetchmany(replayID)[replayID - 1][0]
        executeSTR = f"SELECT {', '.join(retrievalNodes['Match'])} from matchTable WHERE matchID = {replayID}"
        self.c.execute(executeSTR)
        matchDetails = self.c.fetchone()

        executeSTR = f"SELECT {', '.join(retrievalNodes['Player'])} from playerMatchTable WHERE matchID = {replayID}"
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
    def LoadReplays(self, tagsToLoad, num = -1, loadTeams = True, instantiateHistoricPlayers = True, instantiateHistoricTeams = True):
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
        self.statNodes = []

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
        
        for valueNode in list(valueNodes["Match"].values()) + list(valueNodes["Player"].values()):
            print(valueNode.n)
            if valueNode.c:
                continue
            valueNode : ValueNode
            if valueNode.valueType == "Player":
                allValues = [x.valueNodes[valueNode.n] for x in self.players]
            elif valueNode.valueType == "Match":
                allValues = [x.valueNodes[valueNode.n] for x in self.matches]
            self.statNodes.append(StatNode(valueNode, allValues))
    def CompareReplaySelf(s, gamePlayers, gameTeams):
        playerStats = {}
        for statName in valueNodes["Player"]:
            allStats = [x.valueNodes[statName].calculatedValue for x in gamePlayers] #Get All Player Stats
            allStats = [x for x in allStats if x != -1] #Remove Invalid Values
            if len(allStats) == 0:
                continue 
            for player in gamePlayers:
                if player.pList[0] not in playerStats:
                    playerStats[player.pList[0]] = {}
                playerStats[player.pList[0]][statName] = AnalysisNode(player.valueNodes[statName], allStats)
            if "average" not in playerStats:
                playerStats["average"] = {}
            try:
                playerStats["average"][statName] = sum(allStats) / len(allStats)
            except TypeError:
                playerStats["average"][statName] = max(allStats, key = allStats.count)

        teamStats = {"orange" : {}, "blue" : {}, "average" : {}}
        for statName in gameTeams[0].valueNodes:
            allStats = [x.valueNodes[statName].calculatedValue for x in gameTeams]
            allStats = [x for x in allStats if x != -1]
            if len(allStats) == 0:
                continue
            for team in gameTeams:
                teamStats[team.colour][statName] = AnalysisNode(team.valueNodes[statName], allStats)
            teamStats["average"][statName] = sum(allStats) / len(allStats)
        playerNames = [x.name for x in gamePlayers] + ["average"]
        teamNames = [team.colour for team in gameTeams] + ["average"]
        s.OutputAnalysis([(f"{playerNames[i]}_player", x) for i, x in enumerate(playerStats.values())] + [(f"{teamNames[i]}_team", x) for i, x in enumerate(teamStats.values())])
    def OutputAnalysis(s, args):
        if not s.altConn:
            s.CreateAltConnection(s.altdbFile)
        for output in args:
            name = output[0]
            if "average" not in name:
                altName = "".join([x for x in name if x in ascii_letters])
                valuesForOutput = ["rawWeight", "alteredWeight", "equalisedWeight", "calculatedWeight", "againstValue"]
                valueValuesForOutput = ["rawValue", "percentageOf", "calculationValues", "calculatedValue"]
                combinedValues = valueValuesForOutput + valuesForOutput
                valuesString = "\n\t".join([f"{x} float," for x in combinedValues])       
                s.altConn.execute(f"""CREATE TABLE {altName} (
\tid integer PRIMARY KEY,
\tname text,
\t""" + valuesString[:-1] + ");")
                for i, analysisNode in enumerate(output[1].values()):
                    try:
                        valuesOutputValues = [analysisNode.valueNode.__dict__[x] for x in valueValuesForOutput]
                    except AttributeError:
                        print(analysisNode)
                    analysisOutputValues = [analysisNode.__dict__[x] for x in valuesForOutput]

                    outputValuesCombined = valuesOutputValues + analysisOutputValues
                    try:
                        s.altConn.execute(f"""INSERT INTO {altName} VALUES({i}, '{analysisNode.valueNode.n}',  {', '.join([str(x) if isinstance(x, (float, int)) else "-1" for x in outputValuesCombined])})""")
                    except (TypeError, sqlite3.OperationalError) as e:
                        print(f"""INSERT INTO {altName} VALUES({i}, '{analysisNode.valueNode.n}',  {', '.join([str(x) if isinstance(x, (float, int)) else "-1" for x in outputValuesCombined])})""")
                        raise e
            else:
                continue
                s.altConn.execute(f"""CREATE TABLE {name} (
\tid integer PRIMARY KEY,
\tname text,
\tvalue float,
\tstrValue text);""")
                for i, analysisValue in enumerate(output[1]):
                    print(f"""INSERT INTO {name} VALUES({i}, '{analysisValue}',  {output[1][analysisValue]}), ''""")
                    if isinstance(output[1][analysisValue], str):
                        s.altConn.execute(f"""INSERT INTO {name} VALUES({i}, '{analysisValue}',  0, '{output[1][analysisValue]}')""")
                    else:
                        s.altConn.execute(f"""INSERT INTO {name} VALUES({i}, '{analysisValue}',  {output[1][analysisValue]}, '')""")
        s.altConn.commit()
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


class ReplayGUI(App):

    def build(self):
        return Label(text='Hello world')


if __name__ == '__main__':
    replayEngine = ReplayAnalysis(loadReplays = False)
    #for statNode in replayEngine.statNodes:
    #    print(statNode)
    #    input()
    ReplayGUI().run()
