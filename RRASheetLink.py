import gspread
from oauth2client.service_account import ServiceAccountCredentials
from ReplayAnalysis import Player, Team, Match, allNodes
import sqlite3
from time import sleep

class SheetsLink:
    def __init__(s) -> None:
        s.scope = ['https://spreadsheets.google.com/feeds',
                      'https://www.googleapis.com/auth/drive']
        s.creds = ServiceAccountCredentials.from_json_keyfile_name('sheetsKey.json', s.scope)
        s.c = gspread.authorize(s.creds)
        s.sheets = {}
    def SetSheet(s, sheet):
        s.s = s.c.open(sheet)
    def SetPage(s, pageIndex):
        s.p = s.s.get_worksheet(pageIndex)

class Cell:
    def __init__(self, x, y, nodeN, location = "Match", overwrite = False) -> None:
        self.x = x
        self.y = y
        self.n = nodeN
        self.l = location
        self.o = overwrite

class RRAProject:
    def __init__(self, sheet, cells, tags, pageIndex, replayTargets = 0, indexCol = 1, iteratePlayers = False, ignorePlayers = None, name = "Default") -> None:
        if sheet:
            self.s = sheet
        else:
            self.s = "Rocket League Analysis"
        self.c = cells
        locations = [x.l for x in cells]
        self.rPl = "Player" in locations
        self.rTm = "Team" in locations
        self.rT = replayTargets
        self.p = pageIndex
        self.t = tags
        self.iC = indexCol
        self.iP = iteratePlayers
        self.iPlayers = ignorePlayers
        self.name = name

class RRALink:
    def __init__(s, lDB) -> None:
        s.Sheets = SheetsLink()
        if lDB:
            s.LoadDatabase()
    def LoadDatabase(s):
        s.dbFile = r"d:\Users\tom\Documents\Visual Studio Code\Python Files\RocketReplayAnalysis\RocketReplayAnalysis\Database\replayDatabase.db"
        #self.dbFile = r"D:\Users\tom\Documents\Programming Work\Python\RocketReplayAnalysis\Database\replayDatabase.db"
        print(f"Connected to {s.dbFile}")
        s.conn = sqlite3.connect(s.dbFile)
        s.c = s.conn.cursor()
        print(f"SQLite3 Version: {sqlite3.version}")
    def PerformProject(s, p : RRAProject):
        print(f"Performing Project {p.name}")
        s.Sheets.SetSheet(p.s)
        s.Sheets.SetPage(p.p)
        if p.rT == 0:
            s.c.execute(f"SELECT matchID FROM matchTable ORDER BY matchID DESC;")
            latestID = s.c.fetchone()[0]
            sleep(5)
            while True:
                s.c.execute(f"SELECT matchID FROM matchTable ORDER BY matchID DESC;")
                newID = s.c.fetchone()[0]
                print("Checking for new entry")
                if latestID != newID:
                    print("New Entry")
                    latestID = newID
                    s.c.execute(f"SELECT * FROM matchTable WHERE matchID = {latestID};")
                    match = s.c.fetchone()
                    if p.rPl:
                        s.c.execute(f"SELECT * FROM playerMatchTable WHERE matchID = {latestID};")
                        players = s.c.fetchall()
                    if p.rTm:
                        raise NotImplementedError("Required Teams Not Implemented")
                    if p.iP:
                        for player in players:
                            if p.iPlayers:
                                if player[3] in p.iPlayers:
                                    continue
                            for cell in p.c:
                                s.PlaceCell(cell, match, p.iC, player)
                    else:
                        for cell in p.c:
                            s.PlaceCell(cell, match, p.iC)
                    print("Finished")
                sleep(5)              
        else:
            pass
    def PlaceCell(s, cell, match, iC, player = []):
        try:
            if cell.l == "Match":
                value = match[allNodes["Match"].index(cell.n)]
            else:
                value = player[allNodes["Player"].index(cell.n)]
            if cell.y == -1:
                y = len(s.Sheets.p.col_values(iC)) + (1 if cell.x == iC else 0)
            else:
                y = cell.y
            if cell.o:
                s.Sheets.p.update_cell(y, cell.x, value)
            else:
                if not s.Sheets.p.cell(y, cell.x).value:
                    
                    s.Sheets.p.update_cell(y, cell.x, value)
            #print(f"Value: {value}\nX: {cell.x}\nY: {y}\n")
        except gspread.exceptions.APIError as e:
            print(f"Limit Error: {e}")
            sleep(30)
            s.PlaceCell(cell, match, iC, player)
project = RRAProject(None, [Cell(1, -1, "matchID"),
                            Cell(2, -1, "playerID", location = "Player"),
                            Cell(3, -1, "pName", location = "Player")], [], 1, iteratePlayers = True, #ignorePlayers = ["76561198142849050"]
							name = "PlayerAnalysis")
link = RRALink(True)
link.PerformProject(project)