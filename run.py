# REMINDER: Expected output terminal of 80 characters wide and 24 rows high
# Lines 11 - 30 Source code from 'Code Institute', Lesson: 'LoveSandwiches Walkthrough Project - Getting Setup'
# The following code imports the necessary module for interacting with Google Sheets API.
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import statistics
import numpy as np

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

# Function to calculate and format statistic variables
def calculate_statistics(data):
    stats = {
        'average': "N/A",
        'std_dev': "N/A",
        'min_value': "N/A",
        'max_value': "N/A",
        'data_range': "N/A",
        'Q1': "N/A",
        'median': "N/A",
        'Q3': "N/A",
        'IQR': "N/A"
    }
    
    if data:
        stats['min_value'] = f"{min(data):,.2f}"
        stats['max_value'] = f"{max(data):,.2f}"
        stats['data_range'] = f"{max(data) - min(data):,.2f}"
        stats['median'] = f"{statistics.median(data):,.2f}"
        
        if len(data) >= 2:
            stats['average'] = f"{statistics.mean(data):,.2f}"
            stats['std_dev'] = f"{statistics.stdev(data):,.2f}"
            stats['Q1'] = f"{np.percentile(data, 25):,.2f}"
            stats['Q3'] = f"{np.percentile(data, 75):,.2f}"
            stats['IQR'] = f"{np.percentile(data, 75) - np.percentile(data, 25):,.2f}"
    
    return stats

# Function prompts the user to input valid data in integer form
def get_integer_input(prompt, range_min=None, range_max=None):
    while True:
        try:
            records = worksheet.get_all_records() # Fetches records from the worksheet
            value = int(input(prompt))

             # Checks if entered integer is within the provided range
            if (range_min is not None and value < range_min) or (range_max is not None and value > range_max):
                print(f"\n Please enter a numeric value between {range_min} and {range_max}.\n")
            else:
                return value

        except ValueError:
            print("\n Invalid input. Please enter a valid integer (i.e. whole number).\n")

# Save function which takes analysis results and writes it to a text file
def save_to_text_file(data, summary_message, start_year, start_quarter, end_year, end_quarter, selected_county, std_dev=None):
    output_file_path = 'analysis_results.txt'

    # Initialize formatted variables as "N/A"
    average_formatted = "N/A"
    std_dev_formatted = "N/A"
    min_value_formatted = "N/A"
    max_value_formatted = "N/A"
    data_range_formatted = "N/A"
    Q1_formatted = "N/A"
    median_formatted = "N/A"
    Q3_formatted = "N/A"
    IQR_formatted = "N/A"

    # Check if there is any data to perform statistical calculations
    if data:
        min_value = min(data)
        max_value = max(data)
        data_range = max_value - min_value
        median = statistics.median(data)
        
        # Format values that can be computed with at least one data point
        min_value_formatted = f"{min_value:8,.2f}"
        max_value_formatted = f"{max_value:8,.2f}"
        data_range_formatted = f"{data_range:8,.2f}"
        median_formatted = f"{median:8,.2f}"
        
        # If there is more than one data point, calculate additional statistics
        if len(data) >= 2:
            average = statistics.mean(data)
            std_dev = statistics.stdev(data)
            Q1 = np.percentile(data, 25)
            Q3 = np.percentile(data, 75)
            IQR = Q3 - Q1
            
            # Format values that require at least two data points
            average_formatted = f"{average:8,.2f}"
            std_dev_formatted = f"{std_dev:8,.2f}"
            Q1_formatted = f"{Q1:8,.2f}"
            Q3_formatted = f"{Q3:8,.2f}"
            IQR_formatted = f"{IQR:8,.2f}"
    
            stats = calculate_statistics(data) 

    with open(output_file_path, 'w') as file:
    
        # Write the summary of price changes to text file
        file.write("\n +--------------------------------------------------+\n")
        file.write(" |              Summary of Price Changes            |\n")
        file.write(" +--------------------------------------------------+\n")
        file.write(f"\n                From {start_year} Q{start_quarter} to {end_year} Q{end_quarter}\n")
        file.write(f"            {summary_message}\n")
        file.write(f"               New Properity - {selected_county}\n")
        file.write("\n +--------------------------------------------------+\n")

        # Write the descriptive statistics to text file
        if data:
            
            file.write(" |                Summary Statistics:               |\n")
            file.write(" +--------------------------------------------------+\n")
            file.write(f"\n       Average (mean):               {average_formatted}\n")
            file.write(f"       Standard Deviation (+/-):     {std_dev_formatted}\n")  
            file.write("\n +--------------------------------------------------+\n")
            file.write(f"\n       Minimum Value:                {min_value_formatted}\n")
            file.write(f"       Maximum Value:                {max_value_formatted}\n")
            file.write(f"       Range:                        {data_range_formatted}\n")
            file.write("\n +--------------------------------------------------+\n")
            file.write(f"\n       Lower Quartile (Q1):          {Q1_formatted}\n")
            file.write(f"       Median (Q2):                  {median_formatted}\n")
            file.write(f"       Upper Quartile (Q3):          {Q3_formatted}\n")
            file.write(f"       IQR:                          {IQR_formatted}\n")
            file.write("\n +--------------------------------------------------+\n")

# Function to ask user if they want results saved
def save_results(data, summary_message, start_year, start_quarter, end_year, end_quarter, selected_county, std_dev=None):

    save_choice = input("\n  Q. Would you like to the export results? (yes/no): ").lower()

    if save_choice.lower().startswith('y'):
        save_to_text_file(data, summary_message, start_year, start_quarter, end_year, end_quarter, selected_county, std_dev)
        print("\n     Results have been saved to 'analysis_results.txt'\n")

    else:
        print("\n     These results have not been saved.\n")

# Creates user choice loop
while True:
    
    # User options dictionary with key-value pair representing choices that can be selected
    options = {
        '1': "Add new information to database",
        '2': "Perform analysis on existing database",
        '3': "Exit"
    }

    # Menu header within terminal 80x24 limitation
    print(" +--------------------------------------------------+")
    print("\n     Welcome to 'P r o p e r t y  T r a c k e r'\n")
    print("  Keeping you up-to-date with Irish property trends")
    
    # Menu table created using f-strings within terminal 80x24 limitation
    menu_table = f"""
 +--------------------------------------------------+
 | Press |                 Action                   |
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
        print(f" Nationally: {nationally}")
        print(f" Dublin: {dublin}")
        print(f" Cork: {cork}")
        print(f" Galway: {galway}")
        print(f" Limerick: {limerick}")
        print(f" Waterford: {waterford}")
        print(f" Other Counties: {other_counties}\n")

        # Ask for confirmation before saving the data
        confirm = input("\n Is the entered data correct? (yes/no): ")
        if confirm.lower().startswith('y'):
            
            # Adds the data to the worksheet
            worksheet.append_row(row)
            print("\n New information has been successfully added to the database.\n")
        else:
            print("\n Data entry cancelled. No data was added.")
            continue

    elif choice == '2':
        # Initialize an empty list for data collection and variables to hold the starting and ending price points for analysis
        data = []
        start_price = None
        end_price = None
        summary_message = "No data available for that range!"  # Default message

        # Prompt user for start year and quarter, with the current year as the maximium
        print("\n Please enter the range for analysis...")
        start_year = get_integer_input("\n Enter the start Year (YYYY): ", 1975, datetime.now().year)
        start_quarter = get_integer_input(" Enter the start Quarter (1-4): ", 1, 4)
        
        # Prompt user for end year and quarter, with the current year as the maximium
        end_year = get_integer_input("\n Enter the end Year (YYYY): ", start_year, datetime.now().year)

        # Ensures end quarter is valid
        if end_year == start_year:
            end_quarter = get_integer_input(" Enter the end Quarter (1-4): ", start_quarter, 4)
    
        else:
            end_quarter = get_integer_input(" Enter the end Quarter (1-4): ", 1, 4)
  
        # Prompt user for county selection
        print("\n Select the county for analysis:")
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
        
        # Converts choice to a column header name
        selected_county = county_column_mapping[county_choice]
        
        # Retrieve the data from Google Sheet
        try:
            records = worksheet.get_all_records()
            data = []
            start_price = None
            end_price = None
            
            # Defines start and end period after getting user input
            start_period = int(f"{start_year}{start_quarter}")
            end_period = int(f"{end_year}{end_quarter}")

            for record in records:    
                
                # Aligning fields with Google Sheet's column headers
                record_year = int(record.get("Year"))
                record_quarter = int(record.get("Quarter"))

                # Convert year and quarter record into a single integer for simplified record period comparison
                record_period = int(f"{record_year}{record_quarter}")
                
                # Checking year and quarter are within specified range
                if start_period <= record_period <= end_period:
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
                print("\n +--------------------------------------------------+")
                print("       No data available for the range choosen\n") 
                print("                  Please try again!")
                print(" +--------------------------------------------------+\n")   
            
            else:
                
                # Calculates percentage summary
                if start_price is not None and end_price is not None:
                    percentage_change = ((end_price - start_price) / start_price) * 100
                    change_description = "increased" if percentage_change > 0 else "decreased"
                    summary_message = f"Prices have {change_description} by {abs(percentage_change):.2f}%"
                
                else:
                    summary_message = "Unable to calculate overall price changes\n Incomplete data, please try again!"

                # Displays percentage summary
                print("\n +--------------------------------------------------+")
                print(" |              Summary of Price Changes:           |")
                print(" +--------------------------------------------------+")
                
                print(f"                From {start_year} Q{start_quarter} to {end_year} Q{end_quarter}")
                print(f"            {summary_message}")
                print(f"               New Properity - {selected_county}")
                print(" +--------------------------------------------------+")

                # Calculates Summary Statistics
                if data:
                    stats = calculate_statistics(data)

                    # Displays Summary Statistics
                    print(" |                Summary Statistics:               |")
                    print(" +--------------------------------------------------+")
                    print(f"       Average (mean):              €{stats['average']}")
                    print(f"       Standard Deviation (+/-):    €{stats['std_dev']}")  
                    print(" +--------------------------------------------------+")
                    print(f"       Minimum Value:               €{stats['min_value']}")
                    print(f"       Maximum Value:               €{stats['max_value']}")
                    print(f"       Range:                       €{stats['data_range']}")
                    print(" +--------------------------------------------------+")
                    print(f"       Lower Quartile (Q1):         €{stats['Q1']}")
                    print(f"       Median (Q2):                 €{stats['median']}")
                    print(f"       Upper Quartile (Q3):         €{stats['Q3']}")
                    print(f"       IQR:                         €{stats['IQR']}")
                    print(" +--------------------------------------------------+\n")

        except Exception as e:
            print(f"\n An error occurred: {e}")

        save_results(data, summary_message, start_year, start_quarter, end_year, end_quarter, selected_county)
    
    elif choice == '3':
        # Option 3: Exit the program
        print("\n Exiting program... \n \n Thanks for using this 'App', Bye!")
        print("\n +--------------------------------------------------+")    
        break  # This will exit the loop, thus ending the program

    else:
        # Error message if neither option is selected
        print("\n Invalid choice, numbers can only be 1 to 3, please try again.\n")