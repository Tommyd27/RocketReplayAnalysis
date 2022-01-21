import gspread
from oauth2client.service_account import ServiceAccountCredentials
from ReplayAnalysis import Player, Team, Match
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
    def __init__(self, sheet, cells, tags, pageIndex, replayTargets = 0, indexCol = 1) -> None:
        if sheet:
            self.s = sheet
        else:
            self.s = "Rocket League Replay Analysis"
        self.c = cells
        locations = [x.l for x in cells]
        self.rPl = "Player" in locations
        self.rTm = "Team" in locations
        self.rT = replayTargets
        self.p = pageIndex
        self.t = tags
        self.iC = indexCol


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
        s.Sheets.SetSheet(p.s)
        s.Sheets.SetPage(p.p)
        if p.rT == 0:
            s.c.execute(f"SELECT matchID FROM matchTable ORDER BY matchID DESC;")
            latestID = s.c.fetchone()[0]
            sleep(5)
            while True:
                s.c.execute(f"SELECT matchID FROM matchTable ORDER BY matchID DESC;")
                newID = s.c.fetchone()[0]
                if latestID != newID:
                    latestID = newID
                    s.c.execute(f"SELECT * FROM matchTable WHERE matchID = {latestID};")
                    match = s.c.fetchone()[0]
                    if p.rPl:
                        s.c.execute(f"SELECT * FROM playerMatchTable WHERE matchID = {latestID};")
                        players = s.c.fetchall()
                    if p.rTm:
                        raise NotImplementedError("Required Teams Not Implemented")
                    for cell in p.c:
                        cell : Cell
                        if cell.l == "Match":
                            value = match[Match.allNodes.index(cell.n)]
                            if cell.y == -1:
                                y = len(s.Sheets.p.col_values(p.iC)) + 1
                            else:
                                y = cell.y
                            if cell.o:
                                s.Sheets.p.update_cell(y, cell.x, value)
                            else:
                                if not s.Sheets.p.cell(y, cell.x).value:
                                    s.Sheets.p.update_cell(y, cell.x, value)
                        else:
                            for player in players:
                                value = player[Player.allNodes.index(cell.n)]
                                if cell.y == -1:
                                    y = len(s.Sheets.p.col_values(p.iC)) + 1
                                else:
                                    y = cell.y
                                if cell.o:
                                    s.Sheets.p.update_cell(y, cell.x, value)
                                else:
                                    if not s.Sheets.p.cell(y, cell.x).value:
                                        s.Sheets.p.update_cell(y, cell.x, value)
        else:
            pass
