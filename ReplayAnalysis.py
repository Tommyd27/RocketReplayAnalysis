import sqlite3
from sqlite3.dbapi2 import Error
import tkinter as tk

from tkinter import ttk
from typing import List, Type

class AnalysisNode:
    def __init__(self, name, tag, analysisType, relevancy = {}, percentage = False, calculation = False, accountForDuplicates = True, punishDuplicates = False, teamStat = True, index = -1, default = -1) -> None:
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
    def __eq__(self, __o: object) -> bool:
        return self.n == __o.n
    def copy(self):
        return AnalysisNode(self.n, self.t, self.aT, self.r, self.p, self.c, self.aFD, self.pD, self.tS, self.i, self.default)
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
        return output

class Player:
    allNodes = ["playerID", "match", "gameID", "pBallchasingID", "pCalculatedId", "pName", "pPlatform", "pTier", 
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
    analysisNodes =[AnalysisNode('carName', '', 1, index = retrievalNodes.index("carName"), relevancy = 0, teamStat = False), 
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
                    AnalysisNode('qOverfillStolen', 'boost', 0, index = retrievalNodes.index("qOverfillStolen")),
                    AnalysisNode('qWasted', 'boost', 0, index = retrievalNodes.index("qWasted")),
                    AnalysisNode('tZeroBoost', 'boost', 0, index = retrievalNodes.index("tZeroBoost")),
                    AnalysisNode('tFullBoost', 'boost', 0, index = retrievalNodes.index("tFullBoost")),
                    AnalysisNode('tBZeroQuarter', 'boost', 0, index = retrievalNodes.index("tBZeroQuarter")),
                    AnalysisNode('tBQuaterHalf', 'boost', 0, index = retrievalNodes.index("tBQuaterHalf")),
                    AnalysisNode('tBHalfUpperQuater', 'boost', 0, index = retrievalNodes.index("tBHalfUpperQuater")),
                    AnalysisNode('tBUpperQuaterFull', 'boost', 0, index = retrievalNodes.index("tBUpperQuaterFull")),
                    AnalysisNode('aSpeed', 'speed', 0, index = retrievalNodes.index("aSpeed")),
                    AnalysisNode('aHitDistance', 'hits', 0, index = retrievalNodes.index("aHitDistance")),
                    AnalysisNode('aDistanceFromCentre', 'positioning', 0, index = retrievalNodes.index("aDistanceFromCentre")),
                    AnalysisNode('dTotal', 'speed', 0, index = retrievalNodes.index("dTotal")),
                    AnalysisNode('tSonicS', 'speed', 0, index = retrievalNodes.index("tSonicS")),
                    AnalysisNode('tBoostS', 'speed', 0, index = retrievalNodes.index("tBoostS")),
                    AnalysisNode('tSlowS', 'speed', 0, index = retrievalNodes.index("tSlowS")),
                    AnalysisNode('tGround', 'playstyle', 0, index = retrievalNodes.index("tGround")),
                    AnalysisNode('tLowAir', 'playstyle', 0, index = retrievalNodes.index("tLowAir")),
                    AnalysisNode('tHighAir', 'playstyle', 0, index = retrievalNodes.index("tHighAir")),
                    AnalysisNode('tPowerslide', 'speed', 0, index = retrievalNodes.index("tPowerslide")),
                    AnalysisNode('nPowerslide', 'speed', 0, index = retrievalNodes.index("nPowerslide")),
                    AnalysisNode('aPowerslideDuration', 'speed', 0, index = retrievalNodes.index("aPowerslideDuration")),
                    AnalysisNode('aSpeedPercentage', 'speed', 0, index = retrievalNodes.index("aSpeedPercentage")),
                    AnalysisNode('aDBall', 'positioning', 0, index = retrievalNodes.index("aDBall")),
                    AnalysisNode('aDBallPossession', 'positioning', 0, index = retrievalNodes.index("aDBallPossession")),
                    AnalysisNode('aDBallNoPossession', 'positioning', 0, index = retrievalNodes.index("aDBallNoPossession")),
                    AnalysisNode('aDMates', 'positioning', 0, index = retrievalNodes.index("aDMates")),
                    AnalysisNode('tDefensiveThird', 'positioning', 0, index = retrievalNodes.index("tDefensiveThird")),
                    AnalysisNode('tNeutralThird', 'positioning', 0, index = retrievalNodes.index("tNeutralThird")),
                    AnalysisNode('tOffensiveThird', 'positioning', 0, index = retrievalNodes.index("tOffensiveThird")),
                    AnalysisNode('tDefensiveHalf', 'positioning', 0, index = retrievalNodes.index("tDefensiveHalf")),
                    AnalysisNode('tOffensiveHalf', 'positioning', 0, index = retrievalNodes.index("tOffensiveHalf")),
                    AnalysisNode('tBehindBall', 'playstyle', 0, index = retrievalNodes.index("tBehindBall")),
                    AnalysisNode('tInFrontBall', 'playstyle', 0, index = retrievalNodes.index("tInFrontBall")),
                    AnalysisNode('tMostBack', 'playstyle', 0, index = retrievalNodes.index("tMostBack")),
                    AnalysisNode('tMostForward', 'playstyle', 0, index = retrievalNodes.index("tMostForward")),
                    AnalysisNode('goalsConcededLast', 'defense', 0, index = retrievalNodes.index("goalsConcededLast")),
                    AnalysisNode('tClosestBall', 'playstyle', 0, index = retrievalNodes.index("tClosestBall")),
                    AnalysisNode('tFarthestBall', 'playstyle', 0, index = retrievalNodes.index("tFarthestBall")),
                    AnalysisNode('tCloseBall', 'playstyle', 0, index = retrievalNodes.index("tCloseBall")),
                    AnalysisNode('tNearWall', 'positioning', 0, index = retrievalNodes.index("tNearWall")),
                    AnalysisNode('tInCorner', 'positioning', 0, index = retrievalNodes.index("tInCorner")),
                    AnalysisNode('tOnWall', 'positioning', 0, index = retrievalNodes.index("tOnWall")),
                    AnalysisNode('dHitForward', 'hits', 0, index = retrievalNodes.index("dHitForward")),
                    AnalysisNode('dHitBackward', 'hits', 0, index = retrievalNodes.index("dHitBackward")),
                    AnalysisNode('pTime', 'possession', 0, index = retrievalNodes.index("pTime")),
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
                    AnalysisNode('mvp', 'core', 0, index = retrievalNodes.index("mvp")),
                    AnalysisNode('shootingP', 'offense', 0, index = retrievalNodes.index("shootingP")),
                    AnalysisNode('totalHits', 'playstyle', 0, index = retrievalNodes.index("totalHits")),
                    AnalysisNode('totalPasses', 'playstyle', 0, index = retrievalNodes.index("totalPasses")),
                    AnalysisNode('totalDribbles', 'playstyle', 0, index = retrievalNodes.index("totalDribbles")),
                    AnalysisNode('totalDribblesConts', 'playstyle', 0, index = retrievalNodes.index("totalDribblesConts")),
                    AnalysisNode('totalAerials', 'playstyle', 0, index = retrievalNodes.index("totalAerials")),
                    AnalysisNode('totalClears', 'playstyle', 0, index = retrievalNodes.index("totalClears")),
                    AnalysisNode('tBallCam', 'misc', 0, index = retrievalNodes.index("tBallCam")),
                    AnalysisNode('qCarries', 'playstyle', 0, index = retrievalNodes.index("qCarries")),
                    AnalysisNode('qFlicks', 'playstyle', 0, index = retrievalNodes.index("qFlicks")),
                    AnalysisNode('totalCarryT', 'playstyle', 0, index = retrievalNodes.index("totalCarryT")),
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
                    AnalysisNode('goalParticipation', "playstyle", 0, percentage = "teamGoals", calculation = ["@ + @", "goals", "assists"]),
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
                else:
                    calcString : str = node.c[0]
                    variableList = [x.rV for x in self.nodes.values() if x.n in node.c[1:]]
                    for var in variableList:
                        calcString = calcString.replace("@", str(var), 1)
                    node.rV = eval(calcString)
            else:
                node.rV = playerList[node.i]
            if node.p:
                if node.p in Player.retrievalNodes:
                    divValue = playerList[Player.retrievalNodes.index(node.p)]
                else:
                    match node.p:
                        case "teamGoals":
                            teamGoalsIndex = 9 if playerList[8] == "blue" else 10
                            divValue = matchList[teamGoalsIndex]
                node.v = node.rV / (divValue if divValue > 0 else 1)
            else:
                try:
                    node.v = node.rV
                except AttributeError as e:
                    print(node.n)
                    raise e
            if node.default != -1 and node.v == -1:
                node.v = node.default          
            
            self.nodes[node.n] = node
            
class Team:
    analysisNodes = [AnalysisNode("maxLead", "lead", 0),
                     AnalysisNode("maxDeficit", "lead", 0),
                     AnalysisNode("finalLead", "lead", 0),
                     AnalysisNode("comeback", "lead", 0),
                     AnalysisNode("choke", "lead", 0),
                    ]

    def __init__(self, players, matchList) -> None:
        self.players = players
        self.nodes = {}
        self.mL = matchList
        for i, node in enumerate([x.copy for x in Player.analysisNodes if x.tS]):
            try:
                playerSum = sum([x[i] for x in players])
                node.v = playerSum / len(players)
            except TypeError:
                match node.n:
                    case "scoredFirst":
                        node.v = True in [x[i] for x in players]
            
            self.nodes[node.n] = node
        teamColour = players[0][8]

        teamScore = matchList[9] if teamColour == "orange" else matchList[10]
        oppositionScore = matchList[10] if teamColour == "orange" else matchList[9]
        teamPlayerIDs = [x[0] for x in players]

        currentScores = [0]
        goalSequence = matchList[11]
        for goal in goalSequence:
            currentScore = currentScores[-1]
            currentScore += 1 if goal in teamPlayerIDs else -1
            currentScores.append(currentScores)
        maxLeadNode = Team.analysisNodes[0].copy()
        minLeadNode = Team.analysisNodes[1].copy()
        finalLeadNode = Team.analysisNodes[2].copy()
        comebackNode = Team.analysisNodes[3].copy()
        chokeNode = Team.analysisNodes[5].copy()
        if goalSequence not in [0, -1, "NULL", None]:
            maxLeadNode.rV = max(currentScores)
            minLeadNode.rV = min(currentScores)
            finalLeadNode.rV = currentScores[-1]

            comebackNode.rV = minLeadNode.rV if minLeadNode.rV < 0 and finalLeadNode.rV > 0 else 0
            chokeNode.rV = maxLeadNode.rV if maxLeadNode.rV > 1 and finalLeadNode.rV < 0 else 0
        leadNodes = [maxLeadNode, minLeadNode, finalLeadNode, comebackNode, chokeNode]
        for node in leadNodes:
            node.v = node.rV
            self.nodes[node.n] = node
            
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
        for node in Match.analysisNodes:
            node.rV = matchList[node.i]
            if node.p:
                divValue = matchList[Match.retrievalNodes.index(node.p)]
                node.v = node.rV / (divValue if divValue > 0 else 1)
            else:
                node.v = node.rV
            if node.default != -1 and node.v == -1:
                node.v = node.default   
            self.nodes[node.n] = node
    def __repr__(self) -> str:
        output = ""
        for node in self.nodes:
            output += f"{node} : {self.nodes[node]}\n"
        return output

class ReplayAnalysis:
    def __init__(self, loadReplays = True, tagsToLoad = None):
        self.dbFile = r"d:\Users\tom\Documents\Visual Studio Code\Python Files\RocketReplayAnalysis\Database\replayDatabase.db"
        self.CreateConnection(self.dbFile)
        self.replays = []
        if loadReplays:
            self.LoadReplays(tagsToLoad)
    def CreateConnection(self, dbFile):
        self.conn = sqlite3.connect(dbFile)
        self.c = self.conn.cursor()
        print(f"SQLite3 Version: {sqlite3.version}")
    def LoadReplays(self, tagsToLoad = None, num = -1, loadTeams = True):
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
        self.matches = [Match(x) for x in matchLists]
        self.matchesDict = {x.mL[0] : x for x in self.matches}
        #print(self.matchesDict)
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
            self.teams = []
            for players in self.teamsD.values():
                try:
                    self.teams.append(players["orange"])
                except KeyError:
                    pass
                try:
                    self.teams.append(players["blue"])
                except KeyError:
                    pass
    def AnalyseNode(self, analyseNode, nodesList, aType = "top", extraTopRelevance = 5, onlyTags = False):
        #type : top%, average
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
            match node.aT:
                case 0:
                    nodesAll = [xPlayer.nodes[node.n].v for xPlayer in nodesList if xPlayer.nodes[node.n].v not in [-1, "NaN"]]
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

                        node.rR = valueIndex / (listLength - 1)
                        node.cR = node.rV
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
                        




                    else:
                        raise NotImplementedError(f"What type: {type}")
                case _:
                    node.rR = 0
                    node.cR = 0
        return analyseNode
        

gui = ReplayGUI()