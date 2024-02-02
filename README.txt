Contributors:

Alex J.
Andrew Rehmann
Darby Wright
Ethan Reinhart
Morgan Jones

#Python installation
If Python is already locally installed, continue to the next command. Otherwise navigate to the following website:
	https://www.python.org/downloads/

#Requirements verfication
Use of the python interpreter is essential to running this program. Run the following line of code to ensure Python is successfully installed.
	python --version

This program has been tested on Python versions 3.9 and above. If your python version is older than this, please visit the following website:
	https://www.python.org/downloads/	

Run the following line of code to ensure the package installer for Python (pip) is successfully installed.
	pip -V

#Installation of required modules
The Tkinter module creates the functionality of the UI in this program. Run the following command to install Tkinter.
	pip install tk

The matplotlib module is also necessary. Run the following command to ensure proper download.
	pip install matplotlib

The BeautifulSoup module allows the program to scrape the web for faculty names. This module can be installed with the following command.
	pip install beautifulsoup4

The requests module is also required. Please run the following command.
	pip install requests

#Running the software:
The data files necessary for running the software have been preopulated. To instantialize the interface type the following command:

	python3 src/gui.py

#Updating the software:
The source data files used in this project are found in the src/data/ folder and include: gradeData.py and facultyNames.py. The former file contains only data from the original gradedata.js file, the second file contains a set of faculty names acquired using the webscraper.

Creating a new gradeData.py file: 

1. 	Add a new gradedata.js file to the src/data/ folder (overwriting the original). This new gradedata.js file needs to follow the same format as the original. The only exception being the function definitions at the end of the file are superflous and can be included or excluded (it will be processed properly either way).

2. 	Run the following command: 
	
	python3 src/processData.py
	
	The processData script will convert the gradedata.js file into the gradeData.py file used in this project.

3.	You have successfully integrated a new data file into the program. If you wish to supplement your data file with new scraped faculty names, see running the webscraper.

#Running the webscraper
The webscraper gathers faculty names from the University of Oregon department pages. The output of the file is a facultyNames.py file, which includes a python set of faculty names (and nothing else). To update the set of faculty names, run the following command:

	python3 src/scraper.py

	The scraper will output updates to the terminal on what faculty pages it is reading from, and if there are any errors during runtime. It is possible that the webscraper will receive a connection refused errors from the host sites. This is more likely to occur if you run the scraper multiple times in a row. If you get a connection refused error, wait a few minutes and then run the scraper again.

If the output is successful, congratulations you have updated the faculty names list for this project.
