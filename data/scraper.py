"""
Web Scraper Module
2024-01-20
by ear, ajps

Scrapes web archive of UO Catalog to find names of full-time faculty.
"""

from bs4 import BeautifulSoup
import urllib.request
from urllib.request import Request, urlopen
import re
import time
from naturalSci import depts_dict

# constants
NATURAL_SCI_FILEPATH = "naturalSci.txt"
CATALOG_URL = "https://web.archive.org/web/20140901091007/http://catalog.uoregon.edu/arts_sciences/"
URL_DOMAIN_PREFIX = "https://web.archive.org"
FACULTY_MATCH_TEXT = re.compile(".*Faculty.*")
INTERNET_REQUEST_DELAY = 5

def get_html(url: str) -> str:
    """
    Given the URL, return the HTML content of a webpage.
    """
    # use a non-suspicious use agent to reduce chances of being denied
    request = Request(url, headers={
        'User-agent' : 'Mozilla/5.0 (X11; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0'})
    response = urlopen(request)
    response_content = response.read()
    html_content = response_content.decode("utf-8")
    response.close()
    return html_content

    """
    page = urllib.request.urlopen(url)
    return page.read()
    """
    """
    response = urllib.request.urlopen(url)
    response_contents = response.read()
    # decode bytearray type
    html_content = response_contents.decode("utf8")
    response.close()
    return html_content
    """


def get_dept_url_list(catalog_url: str, dept_names_filepath: str) -> list[str]:
    """
    Given the URL for the Catalog from the UO College of Arts and Sciences
    And the path to a file containing the names of desired departments,
    Populate and return list of URLs for those departments.
    """
    # get page content in BeautifulSoup
    page = get_html(CATALOG_URL)
    soup = BeautifulSoup(page, "html.parser")

    # get names of natural sciences
    #target_depts_list = open(dept_names_filepath, "r").readlines()
    #target_depts_list = [item.strip() for item in target_depts_list]
    target_depts_list = depts_dict.values()

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
    page = get_html(dept_url)
    soup = BeautifulSoup(page, "html.parser")

    # go to the header text for the faculty list 
    print(dept_url +  "...checking")
    text_container = soup.find("div", id="facultytextcontainer")
    faculty_list = []

    if text_container:
        faculty_header = text_container.find(["h2", "h3"], string=FACULTY_MATCH_TEXT)

        # collect names until we hit the next header
        curr_element = faculty_header.find_next()
        while (curr_element.get("class") == ["facultylist"]):
            faculty_list.append(curr_element.text.split(',')[0])
            curr_element = curr_element.find_next()

    return faculty_list

def main() -> None:
    """
    Call the web scraper
    """

    # get department URLs
    dept_url_list = get_dept_url_list(CATALOG_URL, NATURAL_SCI_FILEPATH)

    # (temporary) print department URLs
    print("Department URL list:")
    for url in dept_url_list:
        print(url)

    # find the professors from each department page
    print("Collecting faculty names from each department page...")
    names_list = []
    for url in dept_url_list:
        time.sleep(INTERNET_REQUEST_DELAY)
        names_list += get_names_from_dept(url)
    
    # (temporary) print all names
    print(names_list)
    print(f"Found a total of {len(names_list)} names")


if __name__ == "__main__":
    main()
