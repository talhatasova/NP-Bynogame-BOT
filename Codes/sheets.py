import pygsheets
import datetime

class GoogleSheets():
    AUTH_PATH = r"Settings/json Files/sheetAuth.json"
    SHEETS_URL = "https://docs.google.com/spreadsheets/d/1f56jkahCRb8RJDIYE13VHSWmj0Yt_JCnDGDsoTpY6tU/edit?gid=0#gid=0"
    SHEETS_NAME = "ByNo_Last_Items"
    
    def __init__(self, sheets_url:str=SHEETS_URL, sheets_name:str=SHEETS_NAME, auth_filepath:str=AUTH_PATH) -> None:
            self.auth_path = auth_filepath
            self.sheets_url = sheets_url
            self.sheets_name = sheets_name
        
    def setWorksheet(self):
        gc = pygsheets.authorize(service_file=self.auth_path)
        sh = gc.open_by_url(self.sheets_url)
        self.wks:pygsheets.Worksheet = sh.worksheet_by_title(self.sheets_name)

    def writeToSheets(self, data):
        df = [list(x.values()) for x in data]
        lastUpdate = datetime.datetime.now().replace(microsecond=0)
        self.wks.update_value("A1", f"LAST UPDATE\n{lastUpdate}")
        self.wks.insert_rows(row=3, number=len(df), values=df, inherit=False)
        
        total_rows = self.wks.rows
        if total_rows > 100:
            rows_to_delete = total_rows - 100
            self.wks.delete_rows(101, number=rows_to_delete)

        print(f"\n-----{lastUpdate}-----\n")