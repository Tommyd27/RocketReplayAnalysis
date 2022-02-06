import sqlite3
import tkinter as tk

from collections import Counter
from tkinter import ttk


class AnalysisNode:
    def __init__(self, name, tag, analysisType, relevancy = {}, percentage = False, calculation = False, accountForDuplicates = True, punishDuplicates = False, teamStat = True, index = -1, default = -1, percentageAccountForValue = False) -> None:
        self.n = name
        self.t = tag
        self.aT = analysisType
        self.r = relevancy
        self.p = percentage
        self.c = calculation

        self.aFD = accountForDuplicates
        self.pD = punishDuplicates
        self.tS = teamStat
        self.i = index

        self.default = default
        
        self.pAccountForV = percentageAccountForValue
    def __eq__(self, __o: object) -> bool:
        return self.n == __o.n
    def copy(self):
        return AnalysisNode(self.n, self.t, self.aT, self.r, self.p, self.c, self.aFD, self.pD, self.tS, self.i, self.default, self.pAccountForV)
    def __repr__(self) -> str:
        output = f"Name: {self.n}\nRelevance: {self.r}\nIndex: {self.i}"
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
            s.cR = againstValue[value] / len(againstValue)
            s.cR -= 0.5
            s.cR *= relevancy
        elif s.aT == 2:
            s.cR = againstValue[value] / len(againstValue)
            s.cR *= relevancy
        else:
            print("cunt")

class Player:
    allNodes = ["playerID", "matchID", "gameID", "pBallchasingID", "pCalculatedId", "pName", "pPlatform", "pTier", 
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
                "ballchasingStartTime", "ballchasingEndTime", "ballchasingBoostTime", "ballchasingStatTime", "calculatedFirstFrame", "calculatedTimeInGame"]
    retrievalNodes = ["playerID", "pBallchasingID", "pCalculatedId", "pName", "pPlatform", "pTier", 
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
                "ballchasingStartTime", "ballchasingEndTime", "ballchasingBoostTime", "ballchasingStatTime", "calculatedFirstFrame", "calculatedTimeInGame", "matchID"]
    analysisNodes =[AnalysisNode('carName', '', 1, index = retrievalNodes.index("carName"), relevancy = {"top" : 0.1, "average" : 0.1}, teamStat = False), 
                    AnalysisNode('bUsage', 'boost', 0, index = retrievalNodes.index("bUsage")),
                    AnalysisNode('bPerMinute', 'boost', 0, index = retrievalNodes.index("bPerMinute")),
                    AnalysisNode('bConsumptionPerMinute', 'boost', 0, index = retrievalNodes.index("bConsumptionPerMinute")),
                    AnalysisNode('aAmount', 'boost', 0, index = retrievalNodes.index("aAmount")),
                    AnalysisNode('qCollected', 'boost', 0, index = retrievalNodes.index("qCollected")),
                    AnalysisNode('qStolen', 'boost', 0, index = retrievalNodes.index("qStolen")),
                    AnalysisNode('qCollectedBig', 'boost', 0, index = retrievalNodes.index("qCollectedBig")),
                    AnalysisNode('qCollectedSmall', 'boost', 0, index = retrievalNodes.index("qCollectedSmall")),
                    AnalysisNode('qStolenBig', 'boost', 0, index = retrievalNodes.index("qStolenBig")),
                    AnalysisNode('qStolenSmall', 'boost', 0, index = retrievalNodes.index("qStolenSmall")),
                    AnalysisNode('nCollectedBig', 'boost', 0, index = retrievalNodes.index("nCollectedBig")),
                    AnalysisNode('nCollectedSmall', 'boost', 0, index = retrievalNodes.index("nCollectedSmall")),
                    AnalysisNode('nStolenBig', 'boost', 0, index = retrievalNodes.index("nStolenBig")),
                    AnalysisNode('nStolenSmall', 'boost', 0, index = retrievalNodes.index("nStolenSmall")),
                    AnalysisNode('qOverfill', 'boost', 0, index = retrievalNodes.index("qOverfill")),
                    AnalysisNode('qOverfillStolen', 'boost', 0, index = retrievalNodes.index("qOverfillStolen"), punishDuplicates = True),
                    AnalysisNode('qWasted', 'boost', 0, index = retrievalNodes.index("qWasted")),
                    AnalysisNode('tZeroBoost', 'boost', 0, index = retrievalNodes.index("tZeroBoost"), percentage = "ballchasingBoostTime"),
                    AnalysisNode('tFullBoost', 'boost', 0, index = retrievalNodes.index("tFullBoost"), percentage = "ballchasingBoostTime"),
                    AnalysisNode('tBZeroQuarter', 'boost', 0, index = retrievalNodes.index("tBZeroQuarter"), percentage = "ballchasingBoostTime"),
                    AnalysisNode('tBQuaterHalf', 'boost', 0, index = retrievalNodes.index("tBQuaterHalf"), percentage = "ballchasingBoostTime"),
                    AnalysisNode('tBHalfUpperQuater', 'boost', 0, index = retrievalNodes.index("tBHalfUpperQuater"), percentage = "ballchasingBoostTime"),
                    AnalysisNode('tBUpperQuaterFull', 'boost', 0, index = retrievalNodes.index("tBUpperQuaterFull"), percentage = "ballchasingBoostTime"),
                    AnalysisNode('aSpeed', 'speed', 0, index = retrievalNodes.index("aSpeed")),
                    AnalysisNode('aHitDistance', 'hits', 0, index = retrievalNodes.index("aHitDistance")),
                    AnalysisNode('aDistanceFromCentre', 'positioning', 0, index = retrievalNodes.index("aDistanceFromCentre")),
                    AnalysisNode('dTotal', 'speed', 0, index = retrievalNodes.index("dTotal")),
                    AnalysisNode('tSonicS', 'speed', 0, index = retrievalNodes.index("tSonicS"), percentage = "ballchasingStatTime"),
                    AnalysisNode('tBoostS', 'speed', 0, index = retrievalNodes.index("tBoostS"), percentage = "ballchasingStatTime"),
                    AnalysisNode('tSlowS', 'speed', 0, index = retrievalNodes.index("tSlowS"), percentage = "ballchasingStatTime"),
                    AnalysisNode('tGround', 'playstyle', 0, index = retrievalNodes.index("tGround"), percentage = "ballchasingStatTime"),
                    AnalysisNode('tLowAir', 'playstyle', 0, index = retrievalNodes.index("tLowAir"), percentage = "ballchasingStatTime"),
                    AnalysisNode('tHighAir', 'playstyle', 0, index = retrievalNodes.index("tHighAir"), percentage = "ballchasingStatTime"),
                    AnalysisNode('tPowerslide', 'speed', 0, index = retrievalNodes.index("tPowerslide"), percentage = "ballchasingStatTime"),
                    AnalysisNode('nPowerslide', 'speed', 0, index = retrievalNodes.index("nPowerslide")),
                    AnalysisNode('aPowerslideDuration', 'speed', 0, index = retrievalNodes.index("aPowerslideDuration")),
                    AnalysisNode('aSpeedPercentage', 'speed', 0, index = retrievalNodes.index("aSpeedPercentage")),
                    AnalysisNode('aDBall', 'positioning', 0, index = retrievalNodes.index("aDBall")),
                    AnalysisNode('aDBallPossession', 'positioning', 0, index = retrievalNodes.index("aDBallPossession")),
                    AnalysisNode('aDBallNoPossession', 'positioning', 0, index = retrievalNodes.index("aDBallNoPossession")),
                    AnalysisNode('aDMates', 'positioning', 0, index = retrievalNodes.index("aDMates")),
                    AnalysisNode('tDefensiveThird', 'positioning', 0, index = retrievalNodes.index("tDefensiveThird"), percentage = "ballchasingStatTime"),
                    AnalysisNode('tNeutralThird', 'positioning', 0, index = retrievalNodes.index("tNeutralThird"), percentage = "ballchasingStatTime"),
                    AnalysisNode('tOffensiveThird', 'positioning', 0, index = retrievalNodes.index("tOffensiveThird"), percentage = "ballchasingStatTime"),
                    AnalysisNode('tDefensiveHalf', 'positioning', 0, index = retrievalNodes.index("tDefensiveHalf"), percentage = "ballchasingStatTime"),
                    AnalysisNode('tOffensiveHalf', 'positioning', 0, index = retrievalNodes.index("tOffensiveHalf"), percentage = "ballchasingStatTime"),
                    AnalysisNode('tBehindBall', 'playstyle', 0, index = retrievalNodes.index("tBehindBall"), percentage = "ballchasingStatTime"),
                    AnalysisNode('tInFrontBall', 'playstyle', 0, index = retrievalNodes.index("tInFrontBall"), percentage = "ballchasingStatTime"),
                    AnalysisNode('tMostBack', 'playstyle', 0, index = retrievalNodes.index("tMostBack"), percentage = "ballchasingStatTime"),
                    AnalysisNode('tMostForward', 'playstyle', 0, index = retrievalNodes.index("tMostForward"), percentage = "ballchasingStatTime"),
                    AnalysisNode('goalsConcededLast', 'defense', 0, index = retrievalNodes.index("goalsConcededLast"), teamStat = False),
                    AnalysisNode('tClosestBall', 'playstyle', 0, index = retrievalNodes.index("tClosestBall"), percentage = "ballchasingStatTime"),
                    AnalysisNode('tFarthestBall', 'playstyle', 0, index = retrievalNodes.index("tFarthestBall"), percentage = "ballchasingStatTime"),
                    AnalysisNode('tCloseBall', 'playstyle', 0, index = retrievalNodes.index("tCloseBall"), percentage = "ballchasingStatTime"),
                    AnalysisNode('tNearWall', 'positioning', 0, index = retrievalNodes.index("tNearWall"), percentage = "ballchasingStatTime"),
                    AnalysisNode('tInCorner', 'positioning', 0, index = retrievalNodes.index("tInCorner"), percentage = "ballchasingStatTime"),
                    AnalysisNode('tOnWall', 'positioning', 0, index = retrievalNodes.index("tOnWall"), percentage = "ballchasingStatTime"),
                    AnalysisNode('dHitForward', 'hits', 0, index = retrievalNodes.index("dHitForward")),
                    AnalysisNode('dHitBackward', 'hits', 0, index = retrievalNodes.index("dHitBackward")),
                    AnalysisNode('pTime', 'possession', 0, index = retrievalNodes.index("pTime"), percentage = "ballchasingStatTime"),
                    AnalysisNode('turnovers', 'possession', 0, index = retrievalNodes.index("turnovers")),
                    AnalysisNode('turnoversMyHalf', 'possession', 0, index = retrievalNodes.index("turnoversMyHalf")),
                    AnalysisNode('turnoversTheirHalf', 'possession', 0, index = retrievalNodes.index("turnoversTheirHalf")),
                    AnalysisNode('wonTurnovers', 'possession', 0, index = retrievalNodes.index("wonTurnovers")),
                    AnalysisNode('aPDuration', 'possession', 0, index = retrievalNodes.index("aPDuration")),
                    AnalysisNode('aPHits', 'possession', 0, index = retrievalNodes.index("aPHits")),
                    AnalysisNode('qPossession', 'possession', 0, index = retrievalNodes.index("qPossession")),
                    AnalysisNode('demoInflicted', 'demo', 0, index = retrievalNodes.index("demoInflicted")),
                    AnalysisNode('demoTaken', 'demo', 0, index = retrievalNodes.index("demoTaken")),
                    AnalysisNode('score', 'core', 0, index = retrievalNodes.index("score")),
                    AnalysisNode('goals', 'core', 0, index = retrievalNodes.index("goals")),
                    AnalysisNode('assists', 'core', 0, index = retrievalNodes.index("assists")),
                    AnalysisNode('saves', 'core', 0, index = retrievalNodes.index("saves")),
                    AnalysisNode('shots', 'core', 0, index = retrievalNodes.index("shots")),
                    AnalysisNode('mvp', 'core', 1, index = retrievalNodes.index("mvp"), punishDuplicates = True),
                    AnalysisNode('shootingP', 'offense', 0, index = retrievalNodes.index("shootingP")),
                    AnalysisNode('totalHits', 'playstyle', 0, index = retrievalNodes.index("totalHits")),
                    AnalysisNode('totalPasses', 'playstyle', 0, index = retrievalNodes.index("totalPasses")),
                    AnalysisNode('totalDribbles', 'playstyle', 0, index = retrievalNodes.index("totalDribbles")),
                    AnalysisNode('totalDribblesConts', 'playstyle', 0, index = retrievalNodes.index("totalDribblesConts")),
                    AnalysisNode('totalAerials', 'playstyle', 0, index = retrievalNodes.index("totalAerials")),
                    AnalysisNode('totalClears', 'playstyle', 0, index = retrievalNodes.index("totalClears")),
                    AnalysisNode('tBallCam', 'misc', 0, index = retrievalNodes.index("tBallCam"), percentage = "ballchasingStatTime"),
                    AnalysisNode('qCarries', 'playstyle', 0, index = retrievalNodes.index("qCarries")),
                    AnalysisNode('qFlicks', 'playstyle', 0, index = retrievalNodes.index("qFlicks")),
                    AnalysisNode('totalCarryT', 'playstyle', 0, index = retrievalNodes.index("totalCarryT"), percentage = "ballchasingStatTime"),
                    AnalysisNode('totalCarryD', 'playstyle', 0, index = retrievalNodes.index("totalCarryD")),
                    AnalysisNode('aCarryT', 'playstyle', 0, index = retrievalNodes.index("aCarryT")),
                    AnalysisNode('totalKickoffs', 'kickoffs', 0, index = retrievalNodes.index("totalKickoffs")),
                    AnalysisNode('numGoBoost', 'kickoffs', 0, index = retrievalNodes.index("numGoBoost")),
                    AnalysisNode('numnGoFollow', 'kickoffs', 0, index = retrievalNodes.index("numnGoFollow")),
                    AnalysisNode('numGoBall', 'kickoffs', 0, index = retrievalNodes.index("numGoBall")),
                    AnalysisNode('numFirstTouch', 'kickoffs', 0, index = retrievalNodes.index("numFirstTouch")),
                    AnalysisNode('aBoostUsed', 'kickoffs', 0, index = retrievalNodes.index("aBoostUsed")),
                    AnalysisNode('fiftyWins', 'fifties', 0, index = retrievalNodes.index("fiftyWins")),
                    AnalysisNode('fiftyLosses', 'fifties', 0, index = retrievalNodes.index("fiftyLosses")),
                    AnalysisNode('fiftyDraws', 'fifties', 0, index = retrievalNodes.index("fiftyDraws")),
                    AnalysisNode("fiftyWinRate", "fifties", 0, percentage = "totalFifties", index = retrievalNodes.index("fiftyWins"), percentageAccountForValue = (0.2, 0.5)),
                    AnalysisNode("fiftyNotLossRate", "fifties", 0, percentage = "totalFifties", calculation = ["@ + @", "fiftyWins", "fiftyDraws"], percentageAccountForValue = (0.2, 0.5)),
                    AnalysisNode('goalParticipation', "playstyle", 0, percentage = "teamGoals", calculation = ["@ + @", "goals", "assists"], percentageAccountForValue = (0.2, 0.5)),
                    AnalysisNode('scoredFirst', "playstyle", 2, calculation = True),
                        ]
    def __init__(self, playerList, matchList):
        nodesCopy = [x.copy() for x in Player.analysisNodes]
        self.pList = playerList
        self.nodes = {}
        self.mL = matchList
        for node in nodesCopy:
            if node.c:
                if node.c == True:
                    match node.n:
                        case "scoredFirst":
                            try:
                                node.rV = playerList[0] == matchList[11][0]
                            except TypeError:
                                node.rV = -1
                            except IndexError:
                                node.rV = -1
                else:
                    calcString : str = node.c[0]
                    variableList = [x.rV if x.rV != None else -1 for x in self.nodes.values() if x.n in node.c[1:]]
                    if variableList.count(-1) == len(variableList):
                        node.rV = -1
                    else:
                        variableList = [x if x != -1 else 0 for x in variableList]
                        for var in variableList:
                            calcString = calcString.replace("@", str(var), 1)
                        try:
                            node.rV = eval(calcString)
                        except SyntaxError:
                            print(calcString)
            else:
                node.rV = playerList[node.i]
                if not node.rV and node.rV != 0:
                    node.rV = node.default
            if node.p:
                if node.rV != -1:
                    if node.p in Player.retrievalNodes:
                        divValue = playerList[Player.retrievalNodes.index(node.p)]
                    else:
                        match node.p:
                            case "teamGoals":
                                teamGoalsIndex = 10 if playerList[8] == "blue" else 9
                                divValue = matchList[teamGoalsIndex]
                            case "totalFifties":
                                divValue = playerList[Player.retrievalNodes.index("fiftyWins")] + playerList[Player.retrievalNodes.index("fiftyLosses")] + playerList[Player.retrievalNodes.index("fiftyDraws")]
                    node.v = node.rV / (divValue if isinstance(divValue, (int, float)) and divValue > 0 else 1)
                    node.dV = divValue
                else:
                    node.v = -1
                    node.dV = True
                
                if node.pAccountForV:
                    node.v *= node.pAccountForV[1]
                    node.v += node.rV * node.pAccountForV[0]
            else:
                node.dV = False
                try:
                    node.v = node.rV
                except AttributeError as e:
                    print(node.n)
                    raise e
            if node.default != -1 and node.v == -1:
                node.v = node.default          
            
            self.nodes[node.n] = node

class PlayerHistoric(Player):
    countForHistoric = 3
    def __init__(s, players, intensiveStats = False):
        s.players = players
        s.n = {}
        s.nApp = len(players)
        s.iS = intensiveStats
        s.id = players[0].pList[1]
        for stat in PlayerHistoric.analysisNodes:
            match stat.aT:
                case 0:
                    aList = [x.nodes[stat.n].v for x in players if stat.n in x.nodes and x.nodes[stat.n].v not in [None, "NaN", -1]]
                    try:
                        aSum = sum(aList)
                    except TypeError as e:
                        print(aList)
                        raise e
                    try:
                        aAvg = aSum / len(aList)
                    except ZeroDivisionError:
                        aAvg = -1

                    s.n[stat.n] = [aAvg, aList]
                case [1, 2]:
                    allValues = [p[stat.n] for p in players if stat.n in p.nodes]
                    s.n[stat.n] = Counter(allValues)
                    
        if intensiveStats:
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
class Team:
    analysisNodes = [AnalysisNode("maxLead", "lead", 0),
                     AnalysisNode("maxDeficit", "lead", 0),
                     AnalysisNode("finalLead", "lead", 0),
                     AnalysisNode("comeback", "lead", 0),
                     AnalysisNode("choke", "lead", 0),
                    ]

    def __init__(self, players, matchList) -> None:
        debugLen = len(players)
        self.players = players
        self.nodes = {}
        self.mL = matchList
        playersValues = [list(x.nodes.values()) for x in players]
        for i, node in enumerate([x.copy() for x in Player.analysisNodes]):
            if not node.tS:
                continue
            try:
                playerSum = sum([x[i].v for x in playersValues if x[i].v not in [-1, None, "NaN"]])
                node.v = playerSum / len(players)
            except TypeError as e:
                match node.n:
                    case "scoredFirst":
                        node.v = True in [x[i] for x in playersValues]
                    case _:
                        print("Error")
                        print(node.n)
                        print(debugLen)
                        print([x[i].v for x in playersValues if x[i].v not in [-1, None]])
                        raise e
            if not "rV" in node.__dict__:
                node.rV = node.v
            self.nodes[node.n] = node
            if "dV" not in node.__dict__:
                node.dV = False
        teamColour = players[0].pList[8]

        teamScore = matchList[9] if teamColour == "orange" else matchList[10]
        oppositionScore = matchList[10] if teamColour == "orange" else matchList[9]
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
            maxLeadNode = Team.analysisNodes[0].copy()
            minLeadNode = Team.analysisNodes[1].copy()
            finalLeadNode = Team.analysisNodes[2].copy()
            comebackNode = Team.analysisNodes[3].copy()
            chokeNode = Team.analysisNodes[4].copy()

            maxLeadNode.rV = max(currentScores)
            minLeadNode.rV = min(currentScores)
            finalLeadNode.rV = currentScores[-1]

            comebackNode.rV = minLeadNode.rV if minLeadNode.rV < 0 and finalLeadNode.rV > 0 else 0
            chokeNode.rV = maxLeadNode.rV if maxLeadNode.rV > 1 and finalLeadNode.rV < 0 else 0
            leadNodes = [maxLeadNode, minLeadNode, finalLeadNode, comebackNode, chokeNode]
            for node in leadNodes:
                node.v = node.rV
                self.nodes[node.n] = node
        else:
            pass

class TeamHistoric(Team):
    countForHistoric = 3 

class Match:
    allNodes = ["matchID", "gameID", "replayName", "ballchasingLink", "map", "matchType", 
                "teamSize", "playlistID", "durationCalculated", "durationBallchasing", 
                "overtime", "season", "seasonType", "date", "time", "mmr", "nFrames", "orangeScore", "blueScore", 
                "goalSequence", "neutralPossessionTime", "bTimeGround", "bTimeLowAir", "bTimeHighAir", "bTimeBlueHalf", 
                "bTimeOrangeHalf", "bTimeBlueThird", "bTimeNeutralThird", "bTimeOrangeThird", "bTimeNearWall", "bTimeInCorner", 
                "bTimeOnWall", "bAverageSpeed", "bType", "gameMutatorIndex", "tBlueClumped", "tOrangeClumped", "tBlueIsolated", 
                "tOrangeIsolated", "tBluePossession", "tOrangePossession", "replayTagOne", "replayTagTwo", "replayTagThree", 
                "replayTagFour", "replayTagFive", "startPlayerIndex"]
    retrievalNodes = ["matchID", "gameID", "map", "matchType", 
                "teamSize", "durationCalculated", "durationBallchasing", 
                "overtime", "nFrames", "orangeScore", "blueScore", 
                "goalSequence", "neutralPossessionTime", "bTimeGround", "bTimeLowAir", "bTimeHighAir", "bTimeBlueHalf", 
                "bTimeOrangeHalf", "bTimeBlueThird", "bTimeNeutralThird", "bTimeOrangeThird", "bTimeNearWall", "bTimeInCorner", 
                "bTimeOnWall", "bAverageSpeed", "bType", "gameMutatorIndex", "tBlueClumped", "tOrangeClumped", "tBlueIsolated", 
                "tOrangeIsolated", "tBluePossession", "tOrangePossession", "replayTagOne", "replayTagTwo", "replayTagThree", 
                "replayTagFour", "replayTagFive", "startPlayerIndex"]
    analysisNodes =[AnalysisNode('overtime', 'length', 0, index = retrievalNodes.index("overtime")), 
                    AnalysisNode('neutralPossessionTime', 'possession', 0, index = retrievalNodes.index("neutralPossessionTime"), percentage = "durationCalculated"),
                    AnalysisNode('bTimeGround', 'ball', 0, index = retrievalNodes.index("bTimeGround"), percentage = "durationCalculated"),
                    AnalysisNode('bTimeLowAir', 'ball', 0, index = retrievalNodes.index("bTimeLowAir"), percentage = "durationCalculated"),
                    AnalysisNode('bTimeHighAir', 'ball', 0, index = retrievalNodes.index("bTimeHighAir"), percentage = "durationCalculated"),
                    AnalysisNode('bTimeNeutralThird', 'ball', 0, index = retrievalNodes.index("bTimeNeutralThird"), percentage = "durationCalculated"),
                    AnalysisNode('bTimeNearWall', 'ball', 0, index = retrievalNodes.index("bTimeNearWall"), percentage = "durationCalculated"),
                    AnalysisNode('bTimeInCorner', 'ball', 0, index = retrievalNodes.index("bTimeInCorner"), percentage = "durationCalculated"),
                    AnalysisNode('bTimeOnWall', 'ball', 0, index = retrievalNodes.index("bTimeOnWall"), percentage = "durationCalculated"),
                    AnalysisNode('bAverageSpeed', 'ball', 0, index = retrievalNodes.index("bAverageSpeed")),
                    ]
    def __init__(self, matchList) -> None:
        self.mL = matchList
        self.nodes = {}
        analysisNodes = [x.copy() for x in Match.analysisNodes]
        for node in analysisNodes:
            node.rV = matchList[node.i]
            if node.p:
                divValue = matchList[Match.retrievalNodes.index(node.p)]
                node.v = node.rV / (divValue if isinstance(divValue, (int, float)) and divValue > 0 else 1)
                node.dV = divValue
            else:
                node.v = node.rV
                node.dV = False
            if node.default != -1 and node.v == -1:
                print("Updating to default")
                node.v = node.default   
            self.nodes[node.n] = node

    def __repr__(self) -> str:
        output = ""
        for node in self.nodes:
            output += f"{node} : {self.nodes[node]}\n"
        return output

class ReplayAnalysis:
    def __init__(self, loadReplays = True, tagsToLoad = None):
        self.dbFile = r"d:\Users\tom\Documents\Visual Studio Code\Python Files\RocketReplayAnalysis\RocketReplayAnalysis\Database\replayDatabase.db"
        #self.dbFile = r"D:\Users\tom\Documents\Programming Work\Python\RocketReplayAnalysis\Database\replayDatabase.db"
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
        matchNodesToSelectSTR = ", ".join(Match.retrievalNodes)
        playerNodesToSelectSTR = ", ".join(Player.retrievalNodes)

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
    def AnalyseNode(self, analyseNode, nodesList, aType = "top", extraTopRelevance = 5, onlyTags = False):
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
                        nIndex = "n/a"
                        try:
                            againstValues = hPlayer.n[node.n]
                        except KeyError:
                            againstValues = Counter([])

                    
                    analyseNode.againstNodes.append(HistoricalNode(node.n, node.r[nodeType] if nodeType in node.r else 1, node.v, againstValues, nIndex, node.aT))

        elif nodeType == "Team":
            pass

        return analyseNode
    def AnalyseReplay(self, replayID):
        executeSTR = f"SELECT * FROM matchTable WHERE matchID = {replayID}"
        executePlayerSTR = f"SELECT * FROM matchTable WHERE matchID = {replayID}"

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
                values = [node.n, node.t, node.r[aType] if aType in node.r else 1, node.aFD, node.dV, node.rV, node.v, node.rR, node.cR, node.pos]
            else:
                values = [node.n, node.r, node.v, node.aV, node.i, node.aT, node.cR]
            values = [round(x, 2) if isinstance(x, float) else x for x in values]
             
            tree.insert("", tk.END, values = values)
        
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
            playerHTree, scrollBar = s.CreateTree(playersHNodes[0], playerHistoricalTab, "avg",
                                                  columnIDs = ("name", "relevancy", "value", "againstValue", "index", "analysisType",  "calculatedRelevancy"),
                                                  columnNames = ("Name", "Relevancy", "values", "Against Values", "Index", "AnalysisType", "Calculated Relevancy"))
            s.playerHistoricalTrees.append(playerHTree)
            s.playerHistoricalScrollBars.append(scrollBar)

            name = playersHNodes[1][i]
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