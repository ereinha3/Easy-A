"""
Web Scraper Module
2024-01-20
by ear, ajps

Scrapes web archive of UO Catalog to find names of full-time faculty.
"""

from bs4 import BeautifulSoup
import requests
import re
import time
from data.naturalSci import depts_dict

# constants
CATALOG_URL = "https://web.archive.org/web/20140901091007/http://catalog.uoregon.edu/arts_sciences/"
URL_DOMAIN_PREFIX = "https://web.archive.org"
INTERNET_REQUEST_DELAY = 1


def get_dept_url_list(catalog_url: str) -> list[str]:
    """
    Given the URL for the Catalog from the UO College of Arts and Sciences
    And the path to a file containing the names of desired departments,
    Populate and return list of URLs for those departments.
    """
    # get page content in BeautifulSoup
    try:
        page = requests.get(CATALOG_URL)
    except requests.exceptions.ConnectionError:
        print("The web server denied service to the web scraper. Try again later.")
        exit(1)
    soup = BeautifulSoup(page.content, "html.parser")

    # get target departments (natural sciences
    target_depts_list = depts_dict.keys()

    # list of department pages
    dept_list_container = soup.find("ul", id="/arts_sciences/", class_="nav")
    dept_list = [website.a for website in dept_list_container.find_all("li")]

    # get urls for desired departments
    dept_url_list = []
    for dept in dept_list:
        if dept.text not in target_depts_list:
            continue
        dept_url = URL_DOMAIN_PREFIX + dept["href"]
        dept_url_list.append(dept_url)

    return dept_url_list


def get_names_from_dept(dept_url: str) -> list[str]:
    """
    Given the URL to the webpage of a department,
    Return list of names of full-time faculty in that department.
    """
    # get page content in BeautifulSoup
    try:
        page = requests.get(dept_url)
    except requests.exceptions.ConnectionError:
        print("The web server denied service to the web scraper. Try again later.")
        exit(1)
    soup = BeautifulSoup(page.content, "html.parser")

    # go to the header text for the faculty list 
    text_container = soup.find("div", id="facultytextcontainer")
    faculty_list = []

    if text_container:
        # collect names until we hit the next header
        curr_element = text_container.find_next('p')
        while curr_element.get("class") == ['facultylist']:
            # Last element starts with this and is not needed
            if curr_element.text.startswith("The date in parentheses"):
                curr_element = curr_element.find_next('p')
                continue
            faculty_list.append(curr_element.text.split(',')[0])
            curr_element = curr_element.find_next('p')

    return faculty_list


def scrape_faculty_names() -> list[str]:
    """
    Run the web scraper, scraping all faculty names and returning a list of scraped names.
    """

    # get department URLs
    print("Getting department URLs...")
    dept_url_list = get_dept_url_list(CATALOG_URL)

    # find the professors from each department page
    print("Collecting faculty names from each department page...")
    names_list = []
    for url in dept_url_list:
        print(url)
        time.sleep(INTERNET_REQUEST_DELAY)
        names_list += get_names_from_dept(url)

    print(f"Found a total of {len(names_list)} names")

    return names_list


if __name__ == "__main__":
    names_list = scrape_faculty_names()
    print(names_list)
