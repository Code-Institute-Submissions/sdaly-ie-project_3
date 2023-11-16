# REMINDER: Expected output terminal of 80 characters wide and 24 rows high
# Lines 7 - 24 Source code from 'Code Institute', Lesson: 'LoveSandwiches Walkthrough Project - Getting Setup'
# The following code imports the necessary module for interacting with Google Sheets API.
import gspread
from google.oauth2.service_account import Credentials

# Define scope
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

# Path used to access Spreadsheet credentials
CREDS = Credentials.from_service_account_file("creds.json")

# Scoped Credentials
SCOPED_CREDS = CREDS.with_scopes(SCOPE)

# Authorized gspread client with scoped credentials
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)

# Command to open spreadsheet by filename
SHEET = GSPREAD_CLIENT.open("new_property_price")

# Selects first worksheet
worksheet = SHEET.get_worksheet(0)

# Function prompts the user to input valid data in integer form
def get_integer_input(prompt, range_min=None, range_max=None):
    while True:
        try:
            value = int(input(prompt))

             # Checks if entered integer is within the provided range
            if (range_min is not None and value < range_min) or (range_max is not None and value > range_max):
                print(f" Please enter a numeric value between {range_min} and {range_max}.")
            else:
                return value

        except ValueError:
            print(" Invalid input. Please enter a valid integer (i.e. whole number).")

# Creates user choices
while True:
    
    # User options dictionary with key-value pair representing choices user can select
    options = {
        '1': "Add new information to database",
        '2': "Perform analysis on existing database",
        '3': "Exit"
    }

    # Menu header within terminal 80x24 limitation
    print("\n +--------------------------------------------------+")
    print("\n     Welcome to 'P r o p e r t y  T r a c k e r'\n")
    print("  Keeping you up-to-date with Irish property trends")
    
    # Menu table created using f-strings within terminal 80x24 limitation
    menu_table = f"""
 +--------------------------------------------------+
 | Press | Action                                   |
 +--------------------------------------------------+
 |   {'1':<3} | {options['1']:<40} |
 |   {'2':<3} | {options['2']:<40} |
 |   {'3':<3} | {options['3']:<40} |
 +--------------------------------------------------+
"""
    print(menu_table)
    choice = input(" Please select your choice and hit 'Enter': ")
    print("\n +--------------------------------------------------+")

    # Option 1: Add new information to the database
    if choice == '1':
        year = get_integer_input("\n Enter the Year (yyyy): ", 1900, 2100)
        quarter = get_integer_input(" Enter the Quarter (1-4): ", 1, 4)
        nationally = get_integer_input(" Enter the value for Nationally: €")
        dublin = get_integer_input(" Enter the value for Dublin: €")
        cork = get_integer_input(" Enter the value for Cork: €")
        galway = get_integer_input(" Enter the value for Galway: €")
        limerick = get_integer_input(" Enter the value for Limerick: €")
        waterford = get_integer_input(" Enter the value for Waterford: €")
        other_counties = get_integer_input(" Enter the value for Other Counties: €")

        # Create a summary of the entered data
        row = [year, quarter, nationally, dublin, cork, galway, limerick, waterford, other_counties]
        print("\n Summary of the data you've entered:")
        print(f" Year: {year}")
        print(f" Quarter: {quarter}")
        print(f" Nationally: €{nationally}")
        print(f" Dublin: €{dublin}")
        print(f" Cork: €{cork}")
        print(f" Galway: €{galway}")
        print(f" Limerick: €{limerick}")
        print(f" Waterford: €{waterford}")
        print(f" Other Counties: €{other_counties}\n")

        # Ask for confirmation before saving the data
        confirm = input("\n Is the entered data correct? (yes/no): ")
        if confirm.lower().startswith('y'):
            # Insert the data into the worksheet
            worksheet.append_row(row)
            print("\n New information has been successfully added to the database.")
        else:
            print("\n Data entry cancelled. No data was added.")
            continue

    elif choice == '2':
        # Option 2: Perform analysis on the existing dataset

        # Prompt user for year range
        start_year = get_integer_input("\n Enter the start Year (yyyy) for analysis: ", 1900, 2100)
        end_year = get_integer_input(" Enter the end Year (yyyy) for analysis: ", start_year, 2100)
        
        # Prompt user for quarter range
        start_quarter = get_integer_input(" Enter the start Quarter (1-4) for analysis: ", 1, 4)
        end_quarter = get_integer_input(" Enter the end Quarter (1-4) for analysis: ", start_quarter, 4)

        # Prompt user for county
        print(" Select the county for analysis:")
        print(" 1: Nationally")
        print(" 2: Dublin")
        print(" 3: Cork")
        print(" 4: Galway")
        print(" 5: Limerick")
        print(" 6: Waterford")
        print(" 7: Other counties")
        county_choice = get_integer_input("\n Enter the number for selected county: ", 1, 7)
        
        # County choice is mapped to column header name in Google Sheets
        county_column_mapping = {
            1: "Nationally",
            2: "Dublin",
            3: "Cork",
            4: "Galway",
            5: "Limerick",
            6: "Waterford",
            7: "Other_counties",
        }
        
        # Convert choice to a column header name
        selected_county = county_column_mapping[county_choice]
        
        # Retrieve the data from Google Sheet
        try:
            records = worksheet.get_all_records()
            data = []
            start_price = None
            end_price = None
            
            for record in records:    
                # Aligning fields with Google Sheet's column headers
                record_year = record.get("Year")
                record_quarter = record.get("Quarter")
                
                # Checking year and quarter are within specified range
                if start_year <= record_year <= end_year and start_quarter <= record_quarter <= end_quarter:
                    value = record.get(selected_county)
                    
                    if isinstance(value, str):
                        value = value.replace("€", "").replace(",", "")
                    
                    if value:
                        float_value = float(value)
                        data.append(float_value)
                        if record_year == start_year and record_quarter == start_quarter:
                            start_price = float_value
                        if record_year == end_year and record_quarter == end_quarter:
                            end_price = float_value
                        
            if not data:
                print("\n No data found for the given range of years and quarters.")   
            
            elif start_price is not None and end_price is not None:
                
                # Calculate and display percentage change 
                percentage_change = ((end_price - start_price) / start_price) * 100

                if abs(percentage_change) < 0.1:  # Threshold for no significant change which typically is considered negligible in most economical contexts
                    print(f"\n Prices have remained relatively stable with no significant change from {start_year} Q{start_quarter} to {end_year} Q{end_quarter}.")
                
                elif percentage_change > 0:
                    print(f"\n Prices have increased by {percentage_change:.2f}% from {start_year} Q{start_quarter} to {end_year} Q{end_quarter}.")
                
                else:
                    print(f"\n Prices have decreased by {abs(percentage_change):.2f}% from {start_year} Q{start_quarter} to {end_year} Q{end_quarter}.")

            else:
                print("\n Unable to calculate overall price changes - data might be incomplete for the selected range.")

            # Calculate descriptive statistic summary
            import statistics
            import numpy as np

            if data:
                average = statistics.mean(data)
                std_dev = statistics.stdev(data)
                min_value = min(data)
                median = statistics.median(data)
                max_value = max(data)
                data_range = max_value - min_value

                Q1 = np.percentile(data, 25)
                Q3 = np.percentile(data, 75)
                IQR = Q3 - Q1

                # Display results
                print(f"\n Descriptive Statistics from {start_year} Q{start_quarter} to {end_year} Q{end_quarter}:")
                
                print(f"\n Minimum Value: €{min_value:,.2f}")
                print(f" Maximum Value: €{max_value:,.2f}")
                print(f" Range: €{data_range:,.2f}")
                
                print(f"\n Lower Quartile (Q1): €{Q1:,.2f}")
                print(f" Median (Q2): €{median:,.2f}")
                print(f" Upper Quartile (Q3): €{Q3:,.2f}")
                print(f" Interquartile Range (IQR): €{IQR:,.2f}")

                print(f"\n Average (mean): €{average:,.2f}")
                print(f" Standard Deviation (+/-): €{std_dev:,.2f}")

        except Exception as e:
            print(f" An error occurred: {e}")

    elif choice == '3':
        # Option 3: Exit the program
        print("\n Exiting program... \n \n Thanks for using this 'App', Bye!")
        print("\n +--------------------------------------------------+")    
        break  # This will exit the loop, thus ending the program

    else:
        # Error message if neither option is selected
        print("\n Invalid choice, numbers can only be 1 to 3, please try again.")