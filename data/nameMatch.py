"""
Name Matching
2024-01-28
by ajps

Temporary file for name matching code
Would ideally be refactored into admin tools

Note:

Instructor names in gradedata follow this format:
"Last, First Middle"
Last: complete
First: initial or complete
Middle: initial, complete, or omitted

Instructor names in scraped data follow this format:
"First Middle Last"
First: initial or complete
Middle: initial or omitted
Last: complete

Last names are commonly more than one word long!
"""

# import modules
from typing import Union

# get scraped data and gradedata
# FIXME change to correct sources (currently using sample data)
import test.scrapedNames
import test.gradeDataNames

scraped_names = test.scrapedNames.scraped_names_sample
gradedata_names = test.gradeDataNames.gradedata_names_sample


def match_last_name(instructor_name: str, gradedata_names_dict: dict[str, list[str]]) -> list[str]:
    """
    This is the initial step for matching a name.
    Given a name from gradedata, find scraped names with the same last name.
    We work off of the last word of the last name (due to double last names).
    """
    # get last name and canonicalize to get dict search key
    last_name = instructor_name.split(",")[0].strip().split(" ")[-1]
    search_key = "".join(char for char in last_name if char.isalpha()).lower()
    # return list of names with matching last name
    value_at_key = gradedata_names_dict.get(search_key)
    return value_at_key if value_at_key else []

def match_first_name(instructor_name: str, candidate_names: list[str]) -> list[str]:
    """
    This is the next step for matching a name, after last_name_match()
    Given a name from gradedata and candidate names from last_name_match(),
    Return list of candidate names with matching first name or initial
    """
    # get first name or first initial and canonicalize
    first_name = instructor_name.split(",")[1].strip().split(" ")[0]
    first_name = "".join(char for char in first_name if char.isalpha()).lower()
    # only check initials if full first name not provided
    initial_only = True if len(first_name) == 1 else False
    result = []
    for candidate_name in candidate_names:
        # get first name of candidate name and canonicalize
        candidate_first_name = candidate_name.split(" ")[0]
        candidate_first_name = "".join(char for char in candidate_first_name if char.isalpha()).lower()
        # check for a match
        if initial_only or len(candidate_first_name) == 1 and first_name[0] == candidate_first_name[0]:
            # one or both names only have first initial, and the initials match
            result.append(candidate_name)
        elif first_name == candidate_first_name:
            # both first names are fully written out, and they match
            result.append(candidate_name)
    return result

def scraped_names_to_dict(scraped_names: Union[list[str], set[str]]) -> dict[str, list[str]]:
    """
    Given list or set of scraped faculty names of format "First Middle Last"
    Return dict mapping last word of last name -> list of faculty names
    e.g. "smith" -> ["John A. Smith", "Peter Shoemaker Smith"]
    """
    scraped_names_dict: dict[str, list[str]] = {}
    for name in scraped_names:
        # get last word of last name and canonicalize to get dict key
        last_name = name.split(" ")[-1]
        dict_key = "".join(char.lower() for char in last_name if char.isalpha())
        # append to list stored in dict at key
        if not scraped_names_dict.get(dict_key):
            scraped_names_dict[dict_key] = [name]
        else:
            scraped_names_dict[dict_key].append(name)
    return scraped_names_dict
