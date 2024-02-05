"""
Admin Command Line Interface
2024-02-04
by ajps
"""

# resolve filepaths relative to project src directory
import context
from context import src_dir

# import modules for gradedata replacement, web scraping, and name discrepancies
import processData
import scraper
import nameMatch


def prompt_start():
    """
    Prompt the user to decide which featuare of the admin CLI they wish to use.
    """
    prompt_string = """Welcome to the admin interface. What would you like to do?
1: Overwrite existing grade data using a new file
2: Overwrite existing faculty names with new internet data
3: Display information about discrepancies in name matching
Your choice: """
    user_response = input(prompt_string)
    while user_response.strip() not in ['1', '2', '3']:
        user_response = input("Invalid choice. Please try again: ")
    return int(user_response)

def run_gradedata_converter():
    desired_gradedata_path = f"{src_dir}/data/gradedata.js"
    input(f"""Please ensure the new file containing grade data is found at the following path:
{desired_gradedata_path}
Press enter to proceed: """)
    processData.process_gradedata()
    exit(0)


def run_scraper():
    """
    Run the webscraper to get faculty names from the internet.
    Then, run the resulting list through the nameMatch module to enable name matching.
    """
    names_list = scraper.scrape_faculty_names()
    nameMatch.scraped_names_to_dict(names_list)
    print("Successfully scraped faculty names. The program will now use this new data when filtering graph results.")
    exit(0)

def show_discrepancies():
    print("Not yet implemented")
    pass

def main():
    # prompt next action
    choice = prompt_start()
    # decide what to do based on user response
    if choice == 1:
        run_gradedata_converter()
    elif choice == 2:
        run_scraper()
    elif choice == 3:
        show_discrepancies()


if __name__ == "__main__":
   main()