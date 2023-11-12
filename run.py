# Write your code to expect a terminal of 80 characters wide and 24 rows high

# Source: Code Institute LoveSandwiches Walkthrough Project - Getting Setup
import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]
CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('new_property_price')

print(SHEET.title)

sales = SHEET.worksheet('new_property_price')

print(sales)

data = sales.get_all_values()

print(data)