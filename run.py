# Write your code to expect a terminal of 80 characters wide and 24 rows high

# Lines 4 - 24 Modified Source code from 'Code Institute', Lesson: 'LoveSandwiches Walkthrough Project - Getting Setup'
import gspread
from google.oauth2.service_account import Credentials

# Define scope
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

# Path used to access Spreadsheet credentials
CREDS = Credentials.from_service_account_file('creds.json')

# Scoped Credentials
SCOPED_CREDS = CREDS.with_scopes(SCOPE)

# Authorized sgpread client with scoped credentials
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)

# Command to open spreadsheet by filename
SHEET = GSPREAD_CLIENT.open('new_property_price')

# Selects first worksheet
worksheet = SHEET.get_worksheet(0)

# Displays welcome message and offers app choices within expected terminal 80x24 limitation
print("Welcome to 'Property Value', your friendly database application")
print("used for keeping track of property value trends nationally.\n")
print("Please 'press 1' and hit enter to 'add new information'")
print("to the database\n")
print("or\n")
print("Please 'press 2' and hit enter to 'perform analysis'")
print("on the existing dataset\n")
print("Press '3' and hit enter to 'exit'.\n")

# Create users choices
while True:
    # Start a loop that will continue until the user chooses to exit
    choice = input("Enter your choice here: ")

    # Process the user's choice
    if choice == '1':
        # Option 1: Add new information to the database code
        print("TBC")
        # Placeholder for code to follow
        pass

    elif choice == '2':
        # Option 2: Perform analysis on the existing dataset
        print("TBC")
        # Placeholder for code to follow
        pass

    elif choice == '3':
        # Option 3: Exit the program
        print("Exiting program. Thanks for using, hope to see you again soon!")
        break  # This will exit the loop, thus ending the program

    else:
        # Error message if neither option is selected
        print("Invalid choice, numbers can only be 1 to 3, please try again.")

# Display columns headers
# headers = worksheet.row_values(1)
# print("Column headers are:", headers)