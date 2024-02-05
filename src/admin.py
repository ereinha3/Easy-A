"""
Admin Command Line Interface
2024-02-04
by ajps
"""

# resolve filepaths relative to project src directory
import context
from context import src_dir

# for gradedata.js replacement
import processData
# for scraping faculty names
import scraper
# for generating dict
import nameMatch
# for getting set of instructor names for name matching comparison
import dataAccess

# modules
import os


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


def find_match_discrepancies():
    """
    Compare the instructor names from the grade data and the scraped data.
    Generate and display information about discrepancies, namely:
    - Scraped names not matched to any grade data names
    - Grade data names matched to multiple scraped names
    - Scraped names matched to multiple grade data names
    """
    # check that faculty_names.py exists and get names from it
    try:
        assert(os.path.exists("./data/faculty_names.py"))
        from data.faculty_names import faculty_names
    except (AssertionError, ImportError):
        print("No scraped faculty names found. Please run the web scraper first.")
        exit(1)

    # check that gradeDict.py exists
    try:
        assert(os.path.exists("./data/gradeDict.py"))
    except AssertionError:
        print("No grade data found. Please import a grade data file first.")
        exit(1)

    # get set containing instructor names
    gradedata_names = dataAccess.get_all_instructors()
    # keep number of hits for each gradedata name in a dict
    gradedata_names_hits = {}
    for name in gradedata_names:
        gradedata_names_hits[name] = 0
    scraped_names_hits = {}
    # keep number of hits for each scraped name in a dict
    for name_list in faculty_names.values():
        for name in name_list:
            scraped_names_hits[name] = 0

    # go through each instructor name from gradedata names and match
    for name in gradedata_names:
        # skip empty names
        if name.strip() == "":
            continue
        matches = nameMatch.match_name(name)
        # update hits for gradedata name
        gradedata_names_hits[name] = len(matches)
        # update hits for matching scraped names
        for match in matches:
            if scraped_names_hits.get(match):
                scraped_names_hits[match] +=1
            else:
                scraped_names_hits[match] = 1

    # prepare results for gradedata names
    gradedata_no_match_list = []
    gradedata_one_match_list = []
    gradedata_multi_match_list = []
    for name, hits in gradedata_names_hits.items():
        if hits == 0:
            gradedata_no_match_list.append((name, hits))
        if hits == 1:
            gradedata_one_match_list.append((name, hits))
        if hits > 1:
            gradedata_multi_match_list.append((name, hits))

    # prepare results for scraped names
    scraped_no_match_list = []
    scraped_one_match_list = []
    scraped_multi_match_list = []
    for name, hits in scraped_names_hits.items():
        if hits == 0:
            scraped_no_match_list.append((name, hits))
        if hits == 1:
            scraped_one_match_list.append((name, hits))
        if hits > 1:
            scraped_multi_match_list.append((name, hits))

    # print results
    print(f"Found {len(gradedata_no_match_list)} grade data names without a match.")
    print(f"Found {len(gradedata_one_match_list)} grade data names with exactly one match.")
    print(f"Found {len(gradedata_multi_match_list)} grade data names with multiple matches.")
    print(f"Found {len(scraped_no_match_list)} scraped names without a match.")
    print(f"Found {len(scraped_one_match_list)} scraped names with exactly one match.")
    print(f"Found {len(scraped_multi_match_list)} scraped names without multiple matches.")

    # log lists of names to file ./data/name_match_results.py
    results_file = open("./data/name_match_results.py", "w")
    results_lists =  [gradedata_no_match_list, gradedata_one_match_list, gradedata_multi_match_list,
                      scraped_no_match_list, scraped_one_match_list, scraped_multi_match_list]
    results_lists_names =  ["gradedata_no_match_list", "gradedata_one_match_list", "gradedata_multi_match_list",
                            "scraped_no_match_list", "scraped_one_match_list", "scraped_multi_match_list"]
    for i in range(len(results_lists)):
        results_file.write(f"{results_lists_names[i]} = ")
        results_file.write(str(results_lists[i]))
        results_file.write("\n")
    results_file.close()
    print("Saved lists of names for each category to the following path:")
    print(os.path.abspath("./data/name_match_results.py"))

def main():
    # prompt next action
    choice = prompt_start()
    # decide what to do based on user response
    if choice == 1:
        run_gradedata_converter()
    elif choice == 2:
        run_scraper()
    elif choice == 3:
        find_match_discrepancies()
    exit(0)


if __name__ == "__main__":
    main()
