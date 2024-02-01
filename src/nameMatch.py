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
    last_names_list = instructor_name.split(",")[0].strip().split(" ")
    # get last word of last name and canonicalize for search key
    last_last_name = last_names_list[-1]
    search_key = "".join(char for char in last_last_name if char.isalpha()).lower()
    names_at_key = gradedata_names_dict.get(search_key)

    # make sure all last names match (account for multiple last names)
    result = []
    # canonicalize last names to enable comparison
    for i in range(len(last_names_list)):
        last_names_list[i] = "".join(char for char in last_names_list[i] if char.isalpha()).lower()
    for candidate_name in names_at_key:
        accept_candidate = True
        candidate_names_list = candidate_name.split(" ")
        for i in range(1, len(last_names_list) + 1):
            # canonicalize candidate names to enable comparison
            candidate_names_list[-i] = "".join(char for char in candidate_names_list[-i] if char.isalpha()).lower()
            # accept if every word of last names watch
            if last_names_list[-i] != candidate_names_list[-i]:
                accept_candidate = False
        if accept_candidate:
            result.append(candidate_name)
    return result


def match_nth_name(instructor_name: str, n: int, candidate_names: list[str]) -> list[str]:
    """
    This is the next step for matching a name, after last_name_match()
    Given a name from gradedata and candidate names from last_name_match(),
    Return list of candidate names with matching nth name (first or middle).
    """
    # get nth name and canonicalize
    nth_name = instructor_name.split(",")[1].strip().split(" ")[n]
    nth_name = "".join(char for char in nth_name if char.isalpha()).lower()
    # only check initials if full first name not provided
    initial_only = True if len(nth_name) == 1 else False

    # get number of last names
    num_last_names = len(instructor_name.split(",")[0].strip().split(" "))

    # keep list of matching candidate names
    result = []
    for candidate_name in candidate_names:
        num_candidate_names = len(candidate_name.split(" "))
        if n >= num_candidate_names - num_last_names:
            # do not reject a candidate for not having nth name
            result.append(candidate_name)
            continue
        # get nth name of candidate name and canonicalize
        candidate_nth_name = candidate_name.split(" ")[n]
        candidate_nth_name = "".join(char for char in candidate_nth_name if char.isalpha()).lower()
        # check for a match
        if initial_only or len(candidate_nth_name) == 1 and nth_name[0] == candidate_nth_name[0]:
            # one or both names only have first initial, and the initials match
            result.append(candidate_name)
        elif nth_name == candidate_nth_name:
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

def match_name(instructor_name: str, names_dict: dict[str, list[str]]) -> list[str]:
    """
    Given an instructor name from gradedata, return a list of matching scraped names.
    The list may be empty (no matches) or have multiple names (equally likely matches).
    This function assumes you ran scraped_names_to_dict() to get names_dict.
    """
    # first, filter out by last name
    candidates = match_last_name(instructor_name, names_dict)
    # then, filter out by given names (first or middle)
    num_given_names = len(instructor_name.split(",")[1].strip().split(" "))
    for n in range(num_given_names):
        candidates = match_nth_name(instructor_name, n, candidates)
    return candidates
