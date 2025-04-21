# EasyA (JustPass) Application

## Overview
EasyA is a GUI application designed to help students analyze and compare grade distributions across different classes. This tool enables students to:
- Observe relative grade percentages for different classes
- Compare classes to determine which ones have historically been easier
- Make informed decisions about course selection and instructor choices
- Predict their likelihood of success in different courses

## Project Information
- **Created:** January 29, 2024
- **Last Updated:** February 4, 2024
- **Course:** CS422 at the University of Oregon
- **Instructor:** Professor Anthony Hornoff
- **Term:** Winter 2024

## Contributors
- Alex J.
- Morgan Jones
- Andrew Rehmann
- Ethan Reinhart
- Darby Wright

## Getting Started

### Prerequisites
Before using the application, ensure you have:
1. Python 3.10 or higher installed
2. All required modules installed (see Installation_Instructions.pdf)
3. Navigated to the application directory:
```bash
cd /user/Downloads/CS422Group7Project1
```

### Running the Application

#### Student Mode
To launch the student interface:
```bash
python3 src/gui.py
```
The application comes pre-populated with data files, allowing you to immediately interact with the GUI and generate comparison graphs.

#### Admin Mode
To access administrative features:
```bash
python3 src/admin.py
```

The admin interface provides the following options:

1. **Update Database**
   - Add new `gradedata.js` file to `src/data/` folder
   - File must follow the original format (function definitions optional)

2. **Run Web Scraper**
   - Gathers faculty names from UO department pages
   - Outputs to `facultyNames.py`
   - Note: May encounter connection refused errors if run repeatedly

3. **Print Name Matching Discrepancies**
   - Evaluates faculty name matching quality
   - Outputs results to terminal and saves to `src/data/name_match_results.py`
   - Categories:
     - Grade data names without matches
     - Grade data names with exact matches
     - Grade data names with multiple matches
     - Scraped names without matches
     - Scraped names with exact matches
     - Scraped names with multiple matches

4. **Update Department List**
   - View current departments
   - Add new departments
   - Remove existing departments

## Project Structure

### Documentation (`/docs`)
- `Programmer_Documentation.txt`: Technical documentation for developers
- `Schedule.txt`: Project timeline and task allocation
- `Roles.txt`: Team member roles and responsibilities
- `Installation_Instructions.pdf`: Setup guide for Python and dependencies
- `User_Documentation.pdf`: End-user guide

### Source Code (`/src`)
#### Core Files
- `dataAccess.py`: Dataset access functions
- `scraper.py`: Web scraping functionality
- `admin.py`: Administrative tools
- `graphFramePacker.py`: GUI graph generation
- `context.py`: File path assertions
- `nameMatch.py`: Name matching algorithms
- `workingGui.py`: Main GUI interface
- `processData.py`: Data processing utilities

#### Test Directory (`/src/test`)
- `gradeDataNames.py`: Instructor name list
- `scrapedNames.py`: Scraped faculty names
- `testNameMatch.py`: Name matching tests

#### Data Directory (`/src/data`)
- `gradeDict.py`: Processed grade data
- `name_match_results.py`: Name matching results
- `faculty_names.py`: Faculty name dictionary
- `gradedata.js`: Source grade data
- `naturalSci.py`: Natural Science department data

## Installation
For detailed installation instructions, including Python version requirements and module dependencies, please refer to the `Installation_Instructions.pdf` file in the `docs` directory.


Prior to the use of this program, it is required that you follow the steps outlined in the Installation_Instructions.pdf file. This elucidates the modules needed to compile the program and the Python version support for this project, as well as how to download it. 

#Software Dependencies
- Compiler: The Python compiler is required to be run on version 3.10 and above to application support. More information regarding how to check your current version and how to update can be found in the Installation_Instructions.pdf
- Moduels: There are a variety of modules required to be downloaded for this application to work properly. Again, more information regarding these modules and how to download them can be found in the Installation_Instructions.pdf

#Directory Structure:
This README file is contained in the parent directory along with two subdirectories, docs and src.
- docs:
	- Programmer_Documentation.txt : materials that provide guidance to how the software works from the perspective of a person who could write or modify the source code for the project
	- Schedule.txt : a tentative schedule highlighting how tasks were designated and the relative completion times for each task
	- Roles.txt : a list of group member names and roles assigned to each member
	- Installation_Instructions.pdf : a tutorial to follow on how to download Python, update your version to the supported version, and download all required modules for the application
	- User_Documentation.pdf : explains to the the person with the human need that motivated the construction of the system — the student - how to accomplish specific tasks with the system
- src:
	- dataAcess.py : contains functions to access information from the dataset for use in the GUI and graphing module
	- scraper.py : methods for running the webscraper and updating the faculty names list
	- admin.py : program to allow use of variety of admin tools ("Enter Admin Mode")
	- graphFramePacker.py : methods to read in data from the GUI and generate a graph to be place in a Frame in the GUI
	- context.py : assert file paths
	- nameMatch.py : utilize created name matching functions to compare elements of the scraped faculty list with the provided .js file and search for discrepancies
	- workingGui.py : program that contains the entire GUI interface and all logic for user interactions
	- processData.py : program that processes the .js input file into a dictionary for better indexing
	
	- test
		- gradeDataNames.py : a list of all instructor names from the input .js file
		- scrapedNames.py : a list of all faculty names that have been scraped from the way back machine
		- testNameMatch.py : a testing program to test the efficacy of the name match program
	- data
		- gradeDict.py : a large dictionary containing sorted information from the .js file
		- name_match_results.py : a list of tuples containing the name and a boolean regarding whether or not it was matched
		- faculty_names.py : a dictionary with last names as keys and a list of full names with the same last name as values
		- gradedata.js : the inputted .js file in the specified format, initally the source file
		- naturalSci.py : a dictionary of all relevant Natural Science departments with department names as keys and codes and values
	
	
