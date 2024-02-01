Contributors:

Alex J.
Andrew Rehmann
Darby Wright
Ethan Reinhart
Morgan Jones

#Running the software:
The data files necessary for running the software have been preopulated. To instantialize the interface type the following command:

python3 gui.py

#Updating the software:
The source data files used in this project are found in the data/src/ folder and include: gradeData.py and facultyNames.py. The former file contains only data from the original gradedata.js file, the second file contains a set of faculty names acquired using the webscraper.

Creating a new gradeData.py file: 

1. 	Add a new gradedata.js file to the data/src/ folder (overwriting the original). This new gradedata.js file needs to follow the same format as the original. The only exception being the function definitions at the end of the file are superflous and can be included or excluded (it will be processed properly either way).

2. 	Run the following command: 
	
	python3 processData.py
	
	The processData script will convert the gradedata.js file into the gradeData.py file used in this project.

3.	You have successfully integrated a new data file into the program. If you wish to supplement your data file with new scraped faculty names, see running the webscraper.

#Running the webscraper
The webscraper gathers faculty names from the University of Oregon department pages. The output of the file is a facultyNames.py file, which includes a python set of faculty names (and nothing else). To update the set of faculty names, run the following command:

	python3 scraper.py

	The scraper will output updates to the terminal on what faculty pages it is reading from, and if there are any errors during runtime. It is possible that the webscraper will receive a connection refused errors from the host sites. This is more likely to occur if you run the scraper multiple times in a row. If you get a connection refused error, wait a few minutes and then run the scraper again.

If the output is successful, congratulations you have updated the faculty names list for this project.
