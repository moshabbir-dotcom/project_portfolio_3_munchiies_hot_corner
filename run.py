import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("project_portfolio_3_munchiies_hot_corner")


def get_sales_info():
    """
    Get sales information from the user about the hot products and will continue to run until info entered is valid.
    """
    while True:
        print("Please enter daily sales numbers for all Hot Corner products separated with a comma\n")
        print("NOTE: Order of products is Jumbo HotDog, Messy HotDog, Waffle Dog, Cheesy Nachos, Messy Nachos, Messy Fries\n")

        info_str = input("Enter required figures:")
    
        sales_info = info_str.split(",")
        if check_input(sales_info):
            print("Thank You...")
            break

    return sales_info

def check_input(values):
    """
    Within the try part of the function converts all values within the string into integers and 
    raises a ValueError if this cannot be done or the required number of values is not met.
    """
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f"6 valid entries are required, you have entered {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data format: {e}, please try again using only numbers.\n")
        return False

    return True

def update_sales_tab(data):
    """
    Update sales worksheet in the master Google spreadsheet and add a new row relating to a daily entry with the data entered by the user
    """
    print("Sales tab updating on Google Drive...\n")
    sales_worksheet = SHEET.worksheet("sales")
    sales_worksheet.append_row(data)
    print("Sales tab updated on Google Drive!\n")

def update_overunder_tab(data):
    """
    Update overunder worksheet, add new row with the list data provided
    """
    print("Overunder tab updating on Google Drive...\n")
    overunder_worksheet = SHEET.worksheet("overunder")
    overunder_worksheet.append_row(data)
    print("Overunder tab updated on Google Drive!\n")

def calculate_over_under(sales_row):
    """
    Compare sales with amounts of product items prepared and calculate the over/underage to indicate wasted product vs wait time.
    The difference is the sales data subtracted from the prepared stock on hand:
    - Positive number indicates overage at the end of the day resulting in wastage.
    - Negative number indicates customers who had to wait for preparation after .
    """
    print("Generating over/underage data...\n")
    stock = SHEET.worksheet("stockonhand").get_all_values()
    stock_row = stock[-1]

    difference_data = []
    for stock, sales in zip(stock_row, sales_row):
        difference = int(stock) - sales
        difference_data.append(difference)

    return difference_data

def get_last_3_days_sales():
    """
    Collects columns of data from sales worksheet, collecting
    the last 3 days worth of sales for each of the 6 Hot Products and returns the data
    as a list of lists.
    """
    sales = SHEET.worksheet("sales")

    columns = []
    for ind in range(1, 7):
        column = sales.col_values(ind)
        columns.append(column[-3:])

    return columns

def main():
    """
    This is to run all program functions within one main function as per good practice
    """
    info = get_sales_info()
    sales_info = [int(num) for num in info]
    update_sales_tab(sales_info)
    new_difference_data = calculate_over_under(sales_info)
    update_overunder_tab(new_difference_data)

    print(new_difference_data)

print("Munchiies Stock Control System\n")
main()

average_3_days = get_last_3_days_sales()