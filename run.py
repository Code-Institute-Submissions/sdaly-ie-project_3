# Write your code to expect a terminal of 80 characters wide and 24 rows high
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

# Authorized gspread client with scoped credentials
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
        # Option 1: Add new information to the database
        try:
            # Prompts user for required information sequentially 
            year = input("Enter the Year (yyyy): ")
            quarter = input("Enter the Quarter (1-4): ")
            nationally = input("Enter the value for Nationally: ")
            dublin = input("Enter the value for Dublin: ")
            cork = input("Enter the value for Cork: ")
            galway = input("Enter the value for Galway: ")
            limerick = input("Enter the value for Limerick: ")
            waterford = input("Enter the value for Waterford: ")
            other_counties = input("Enter the value for Other Counties: ")

            # Ensure the year is valid
            if not year.isdigit() or len(year) != 4:
                print("Invalid year format. Please try again.")
                continue
                  
            # Ensure the quarter is valid
            if not quarter.isdigit() or not 1 <= int(quarter) <= 4:
                print("Invalid quarter. Please try again.")
                continue

            # Create a summary of the entered data
            row = [year, quarter, nationally, dublin, cork, galway, limerick, waterford, other_counties]
            print("\nSummary of the data entered:")
            print(f"Year: {year}")
            print(f"Quarter: {quarter}")
            print(f"Nationally: {nationally}")
            print(f"Dublin: {dublin}")
            print(f"Cork: {cork}")
            print(f"Galway: {galway}")
            print(f"Limerick: {limerick}")
            print(f"Waterford: {waterford}")
            print(f"Other Counties: {other_counties}\n")

            # Ask for confirmation before saving the data
            confirm = input("Is the entered data correct? (yes/no): ")
            if confirm.lower().startswith('y'):
                # Insert the data into the worksheet
                worksheet.append_row(row)
                print("New information added successfully.")
            else:
                print("Data entry cancelled. No data was added.")
                continue

        except Exception as e:
            print("An error occurred when trying to add information to the database.")
            print(e)

    elif choice == '2':
        # Option 2: Perform analysis on the existing dataset
        print("TBC")
        # Placeholder for code to follow
        pass

    elif choice == '3':
        # Option 3: Exit the program
        print("Exiting program... Thanks for using this Application, hope to see you again soon!")
        break  # This will exit the loop, thus ending the program

    else:
        # Error message if neither option is selected
        print("Invalid choice, numbers can only be 1 to 3, please try again.")