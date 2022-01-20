import gspread
from oauth2client.service_account import ServiceAccountCredentials
from ReplayAnalysis import Player, Team, Match
import sqlite3

class SheetsLink:
    def __init__(s) -> None:
        s.scope = ['https://spreadsheets.google.com/feeds',
                      'https://www.googleapis.com/auth/drive']
        s.creds = ServiceAccountCredentials.from_json_keyfile_name('sheetsKey.json', s.scope)
        s.c = gspread.authorize(s.creds)
        s.sheets = {}
    def SetSheet(s, sheet):
        s.s = s.c.open(sheet)
    def AddSheet(s, sheet):
        s.sheets[sheet] = s.c.open[sheet]

class Cell:
    def __init__(self, x, y, nodeN, location = "Match") -> None:
        self.x = x
        self.y = y
        self.n = nodeN
        self.l = location

class RRAProject:
    def __init__(self, cells, tags, replayTargets = 0) -> None:
        self.c = cells
        locations = [x.l for x in cells]
        self.rP = "Player"
        self.rT = "Team"
        self.rT = replayTargets
        self.t = tags

class RRALink:
    def __init__(s, lDB) -> None:
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
        if p.rT == 0:
            pass
        else:
            pass
