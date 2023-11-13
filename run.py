# REMINDER: Expect output terminal of 80 characters wide and 24 rows high
# Lines 4 - 24 Modified Source code from 'Code Institute', Lesson: 'LoveSandwiches Walkthrough Project - Getting Setup'
# The following code imports the necessary modules for interacting with the Google Sheets API.
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

# Function prompts the user to input valid data in integer form
def get_integer_input(prompt, range_min=None, range_max=None):
    while True:
        try:
            value = int(input(prompt))
             # Checks if entered integer is within the provided range
            if (range_min is not None and value < range_min) or (range_max is not None and value > range_max):
                print(f"Please enter a numeric value between {range_min} and {range_max}.")
            else:
                return value

        except ValueError:
            print("Invalid input. Please enter a valid integer (i.e. whole number).")

# Creates user choices
while True:
    # Displays welcome message and menu within expected terminal 80x24 limitation
    print("\nWelcome to 'Property Value', your friendly database application")
    print("used for keeping track of property value trends nationally.\n")
    print("Please 'press 1' and hit enter to 'add new information'")
    print("to the database\n")
    print("Please 'press 2' and hit enter to 'perform analysis'")
    print("on the existing dataset\n")
    print("Press '3' and hit enter to 'exit'.\n")

    # Starts a loop that will continue until the user chooses to exit
    choice = input("Enter your choice here: ")

    # Option 1: Add new information to the database
    if choice == '1':
        year = get_integer_input("Enter the Year (yyyy): ", 1900, 2100)
        quarter = get_integer_input("Enter the Quarter (1-4): ", 1, 4)
        nationally = get_integer_input("Enter the value for Nationally: €")
        dublin = get_integer_input("Enter the value for Dublin: €")
        cork = get_integer_input("Enter the value for Cork: €")
        galway = get_integer_input("Enter the value for Galway: €")
        limerick = get_integer_input("Enter the value for Limerick: €")
        waterford = get_integer_input("Enter the value for Waterford: €")
        other_counties = get_integer_input("Enter the value for Other Counties: €")

        # Create a summary of the entered data
        row = [year, quarter, nationally, dublin, cork, galway, limerick, waterford, other_counties]
        print("\nSummary of the data you've entered:")
        print(f"Year: {year}")
        print(f"Quarter: {quarter}")
        print(f"Nationally: €{nationally}")
        print(f"Dublin: €{dublin}")
        print(f"Cork: €{cork}")
        print(f"Galway: €{galway}")
        print(f"Limerick: €{limerick}")
        print(f"Waterford: €{waterford}")
        print(f"Other Counties: €{other_counties}\n")

        # Ask for confirmation before saving the data
        confirm = input("Is the entered data correct? (yes/no): ")
        if confirm.lower().startswith('y'):
            # Insert the data into the worksheet
            worksheet.append_row(row)
            print("\nNew information has been successfully added to the database.")
        else:
            print("\nData entry cancelled. No data was added.")
            continue

    elif choice == '2':
        # Option 2: Perform analysis on the existing dataset

        # Prompt user for year range
        start_year = get_integer_input("Enter the start Year (yyyy) for analysis: ", 1900, 2100)
        end_year = get_integer_input("Enter the end Year (yyyy) for analysis: ", start_year, 2100)
        
        # Prompt user for quarter range
        start_quarter = get_integer_input("Enter the start Quarter (1-4) for analysis: ", 1, 4)
        end_quarter = get_integer_input("Enter the end Quarter (1-4) for analysis: ", start_quarter, 4)

        # Prompt user for county
        print("Select the county for analysis:")
        print("1: Nationally")
        print("2: Dublin")
        print("3: Cork")
        print("4: Galway")
        print("5: Limerick")
        print("6: Waterford")
        print("7: Other_counties")
        county_choice = get_integer_input("Enter the number for selected county: ", 1, 7)
        
        # County choice is mapped to column header name in Google Sheets
        county_column_mapping = {
            1: 'Nationally',
            2: 'Dublin',
            3: 'Cork',
            4: 'Galway',
            5: 'Limerick',
            6: 'Waterford',
            7: 'Other_counties',
        }
        
        # Convert choice to a column header name
        selected_county = county_column_mapping[county_choice]
        
        # Retrieve the data from Google Sheet
        try:
            records = worksheet.get_all_records()
            data = []
            
            for record in records:    
                # Aligning fields with Google Sheet's column headers
                record_year = record.get('Year')
                record_quarter = record.get('Quarter')
                
                # Checking year and quarter are within specified range
                if start_year <= record_year <= end_year and start_quarter <= record_quarter <= end_quarter:
                    value = record.get(selected_county)
                    
                    if isinstance(value, str):
                        value = value.replace('€', '').replace(',', '')
                    
                    if value:
                        data.append(float(value))
                        
            if not data:
                print("No data found for the given range of years and quarters.")
            
            else:
                # Calculate descriptive statistics
                import statistics
                average = statistics.mean(data)
                median = statistics.median(data)
                
                # Display the results
                print(f"\nDescriptive Statistics from {start_year} Q{start_quarter} to {end_year} Q{end_quarter}:")
                print(f"Average: €{average:,.2f}")
                print(f"Median: €{median:,.2f}")
        
        except Exception as e:
            print(f"An error occurred: {e}")

    elif choice == '3':
        # Option 3: Exit the program
        print("Exiting program... Thanks for using this Application, hope to see you again soon!")
        break  # This will exit the loop, thus ending the program

    else:
        # Error message if neither option is selected
        print("Invalid choice, numbers can only be 1 to 3, please try again.")