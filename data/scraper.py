"""
Web Scraper Module
2024-01-20
by ear, ajps

Scrapes web archive of UO Catalog to find names of full-time faculty.
"""

from bs4 import BeautifulSoup
import requests
import re

# constants
NATURAL_SCI_FILE = "naturalSci.txt"
CATALOG_URL = "https://web.archive.org/web/20140901091007/http://catalog.uoregon.edu/arts_sciences/"

# get page content in BeautifulSoup
page= requests.get(CATALOG_URL)
soup = BeautifulSoup(page.content, "html.parser")

# get names of natural sciences
natural_sci_list = open(NATURAL_SCI_FILE, "r").readlines()
natural_sci_list = [item.strip() for item in natural_sci_list]

# list of department pages
dept_list_container = soup.find("ul", id="/arts_sciences/", class_="nav")
dept_list = [website.a for website in dept_list_container.find_all("li")]

# get urls for natural science departments
dept_url_list = []
for dept in dept_list:
    if dept.text not in natural_sci_list:
        continue
    dept_url = "https://web.archive.org" + dept["href"]
    dept_url_list.append(dept_url)

# (temporary) print department URLs
print("Departament URL list:")
for url in dept_url_list:
    print(url)