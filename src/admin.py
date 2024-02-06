"""
Admin Command Line Interface
2024-02-04
by ajps, ear
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
# for updating department list
import data.naturalSci

# modules
import os
import importlib

NATURAL_SCI_FILEPATH = "./data/naturalSci.py"

def prompt(prompt_string):
    """
    Prompt the user to decide which feature of the admin CLI they wish to use.
    """
    user_response = input(prompt_string)
    while user_response.strip() not in ['0', '1', '2', '3', '4']:
        user_response = input("Invalid choice. Please try again: ")
    return int(user_response)

def update_departments():
    department_prompt_string = """
You may now append or remove a department from the list. 
If appending the department, please navigate to the instructions available in User_Instructions.pdf.
What would you like to do?
0: Return to main admin tools
1: View current departments in the system
2: Append a department
3: Remove a department
Your choice: """
    dept_input = prompt(department_prompt_string)
    while dept_input:
        if dept_input == 1:
            print()
            print("Departments in System:")
            for key in data.naturalSci.depts_dict.keys():
                print(key)
        if dept_input == 2:
            dept_add_prompt_string = """Please provide the name of the department you would like to add. 
Please be careful of spelling. 0 to exit. """
            dept_name = input(dept_add_prompt_string)
            if dept_name == '0':
                return
            department_code_prompt_string = "Please provide the corresponding department code. "
            dept_code = input(department_code_prompt_string).upper()
            if dept_code == '0':
                return
            f = open(NATURAL_SCI_FILEPATH, 'ab+')
            f.seek(-1, 2)
            f.truncate()
            f = open(NATURAL_SCI_FILEPATH, 'a')
            new_line = '    ' + f'"{dept_name}"' + ':' + f'"{dept_code}"' + ',\n}'
            f.write(new_line)
            f.close()
        if dept_input == 3:
            dept_remove_prompt_string = "Please provide the name of the department you would like to remove or 0 to exit (Please be careful of spelling and capitaliztaion): "
            dept_remove_input = input(dept_remove_prompt_string).strip()
            truth = 1
            count = 0
            while truth:
                if dept_remove_input == '0':
                    return
                f = open(NATURAL_SCI_FILEPATH, 'r')
                line = f.readline()
                while line:
                    print(line, count)
                    if dept_remove_input in line:
                        truth = 0
                        break
                    line = f.readline()
                    count += 1
                f.close()
                if truth:
                    dept_remove_input = input("Department not found. Please try again: ").strip()
                print(dept_remove_input)
            f = open(NATURAL_SCI_FILEPATH, 'r')
            line = f.readline()
            bytes = 0
            index = None
            while line:
                if dept_remove_input in line:
                    index = (bytes, bytes+len(line))
                bytes += len(line)
                line = f.readline()
            f = open(NATURAL_SCI_FILEPATH, 'r')
            file = f.read()
            f.close()
            new_file = open(NATURAL_SCI_FILEPATH, 'w')
            new_file_chars = file[:index[0]]+file[index[1]:]
            new_file.write(new_file_chars)
            new_file.close()
        dept_input = prompt(department_prompt_string)
    return



def run_gradedata_converter():
    desired_gradedata_path = f"{src_dir}/data/gradedata.js"
    input(f"""Please ensure the new file containing grade data is found at the following path:
{desired_gradedata_path}
Press enter to proceed: """)
    processData.process_gradedata()
    input("Press enter to return to menu: ")


def run_scraper():
    """
    Run the webscraper to get faculty names from the internet.
    Then, run the resulting list through the nameMatch module to enable name matching.
    """
    names_list = scraper.scrape_faculty_names()
    nameMatch.scraped_names_to_dict(names_list)
    print("Successfully scraped faculty names. The program will now use this new data when filtering graph results.")
    input("Press enter to return to menu: ")


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
        import data.faculty_names as faculty_names
        # reload in case web scraper was called earlier during runtime
        importlib.reload(faculty_names)
        faculty_names_dict = faculty_names.faculty_names
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
    for name_list in faculty_names_dict.values():
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
    print(f"Found {len(scraped_multi_match_list)} scraped names with multiple matches.")

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
    input("Press enter to return to menu: ")

def main():
    # prompt next action
    prompt_string = """
Welcome to the admin interface. What would you like to do?
0: Exit the admin tools interface
1: Overwrite existing grade data using a new file
2: Overwrite existing faculty names with new internet data
3: Display information about discrepancies in name matching
4: Update departments list
Your choice: """
    choice = prompt(prompt_string)
    # decide what to do based on user response
    
    while choice:
        if choice == 1:
            run_gradedata_converter()
        elif choice == 2:
            run_scraper()
        elif choice == 3:
            find_match_discrepancies()
        elif choice == 4:
            update_departments()
        choice = prompt(prompt_string)
    exit(0)


if __name__ == "__main__":
    main()
