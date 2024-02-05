EasyA or JustPass Application:

This application's purpose is to create a GUI environment allowing students to observe relative grade percentages for different classes. From here, they can compare with another class to determine the class which has historically been the easiest. This tool is beneficial for students deciding between which teacher to take the class under or students deciding between two classes. It allows them to get a relative prediction for how likely they are to do well in one class compared to another.

Contributors:

Alex J.
Morgan Jones
Andrew Rehmann
Ethan Reinhart
Darby Wright

Created on -- 01-29-2024
Updated on -- 02-04-2024

This application was created for the initial project of CS422 at the University of Oregon, taken under the teaching of Professor Anthony Hornoff in Winter 2024. The assignment was to improve on a previous system that perfomed a similar task yet lacked many features. This implementation creates a more streamlined GUI interface that allows students to better evaluate their course selections.

Prior to entering either application mode, you must first navigate to the folder containing the corresponding contents. This can be done with the following command:
	cd /user/Downloads/CS422Group7Project1

Now that you are in the application directory, you may enter either Student or Admin mode by following the instructions below.

#Student Mode
- Running the software:
The data files necessary for running the software have been preopulated. To instantialize the interface type the following command:

	python3 src/gui.py

From here you can interact with the GUI to receive an output graph of your own design.

#Admin Mode
In order to access admin mode, first run the following command:
	python3 src/admin.py

You will be prompted with 4 potential input options:

0: Exit the admin tools.

1: Updating the database:
The source data files used in this project are found in the src/data/ folder and include: gradeData.py and facultyNames.py. The former file contains only data from the original gradedata.js file, the second file contains a set of faculty names acquired using the webscraper.
	- Add a new gradedata.js file to the src/data/ folder (overwriting the original). This new gradedata.js file needs to follow the same format as the original. The only exception being the function definitions at the end of the file are superflous and can be included or excluded (it will be processed properly either way).
	- This new file needs to be inserted prior to running this admin tool

2: Running the webscraper
The webscraper gathers faculty names from the University of Oregon department pages. The output of the file is a facultyNames.py file, which includes a python set of faculty names (and nothing else). 
The scraper will output updates to the terminal on what faculty pages it is reading from, and if there are any errors during runtime. It is possible that the webscraper will receive a connection refused errors from the host sites. This is more likely to occur if you run the scraper multiple times in a row. If you get a connection refused error, wait a few minutes and then run the scraper again.
If the output is successful, congratulations you have updated the faculty names list for this project.

3: Print discrepancies in name matching
This command evaluates the quality of the faculty names compared with the input file names by using a name matching program.
This command will print a variety of results to the command line:
	- Grade data names without a match.
	- Grade data names with exactly one match.
	- Grade data names with multiple matches.
	- Scraped names without a match.
	- Scraped names with exactly one match.
	- Scraped names with multiple matches.
It will saved a lists of names for each category to the following file path:
	***/CS422Group7Project1/src/data/name_match_results.py

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
	
	
