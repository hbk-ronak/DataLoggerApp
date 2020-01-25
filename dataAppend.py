import gspread
from oauth2client.service_account import ServiceAccountCredentials
# from pprint import pprint

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)

client = gspread.authorize(creds)

sheet = client.open("Tracking Template").sheet1  # Open the spreadhseet

# data = sheet.get_all_records()  # Get a list of all records


def insert_row(value):
	numRows = sheet.row_count 
	sheet.insert_row(value, index = numRows - 1000 + 2)