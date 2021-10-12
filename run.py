import gspread
from google.oauth2.service_account import Credentials

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
    Get sales information from the user about the hot products
    """
    print("Please enter daily sales numbers for all Hot Corner products separated with a comma\n")
    print("NOTE: Order of products is Jumbo HotDog, Messy HotDog, Waffle Dog, Cheesy Nachos, Messy Nachos, Messy Fries\n")

    info_str = input("Enter required figures:")
    print(f"You have entered {info_str}")

get_sales_info()