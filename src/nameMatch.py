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

import context
import importlib

global faculty_names
faculty_names = None


def scraped_names_to_dict(scraped_names: list[str]) -> None:
    """
    Given list or set of scraped faculty names of format "First Middle Last",
    Create dict mapping last word of last name -> list of faculty names
    e.g. "smith" -> ["John A. Smith", "Peter Shoemaker Smith"]
    This dict is stored at ./data/faculty_names.py
    """
    scraped_names_dict: dict[str, list[str]] = {}
    for name in scraped_names:
        name = name.strip()
        # get last word of last name and canonicalize to get dict key
        last_name = name.strip().split(" ")[-1]
        dict_key = "".join(char.lower() for char in last_name if char.isalpha())
        # append to list stored in dict at key
        if not scraped_names_dict.get(dict_key):
            scraped_names_dict[dict_key] = [name]
        else:
            scraped_names_dict[dict_key].append(name)

    # store scraped names dict in faculty_names.py file
    faculty_names_file = open("./data/faculty_names.py", "w")
    faculty_names_file.write(f"faculty_names: dict[str, list[str]] = {str(scraped_names_dict)}")
    faculty_names_file.close()

    # reload these names for name matching
    _reload_names_dict()

def _reload_names_dict():
    """
    Force Python to re-import the data/faculty_names.py module.
    This ensures names are matched to the newest available data.
    This should be called by scraped_names_to_dict().
    """
    global faculty_names
    try:
        import data.faculty_names as faculty_names
        importlib.reload(faculty_names)
    except ImportError:
        faculty_names = None

def _match_last_name(instructor_name: str) -> list[str]:
    """
    This is the initial step for matching a name.
    Given a name from gradedata, find scraped names with the same last name.
    We work off of the last word of the last name (due to double last names).
    """
    # import faculty_names should be taken care of before calling this
    global faculty_names
    names_dict = faculty_names.faculty_names

    if not "," in instructor_name:
        # do not match name that is not in Last, First order
        return []
    last_names_list = instructor_name.strip().split(",")[0].strip().split(" ")
    # get last word of last name and canonicalize for search key
    last_last_name = last_names_list[-1]

    #trim non-alphanumeric characters from name
    search_key = "".join(char for char in last_last_name if char.isalpha()).lower()

    #get all names in dict whose key is the cleaned last name
    names_at_key = names_dict.get(search_key)
    if not names_at_key:
        return []

    # make sure all last names match (account for multiple last names)
    result = []
    # canonicalize last names to enable comparison
    for i in range(len(last_names_list)):
        last_names_list[i] = "".join(char for char in last_names_list[i] if char.isalpha()).lower()
    for candidate_name in names_at_key:
        candidate_names_list = candidate_name.strip().split(" ")
        if len(candidate_names_list) == 1:
            # avoid matchign empty or one-word names
            continue
        accept_candidate = True
        for i in range(1, len(last_names_list) + 1):
            # canonicalize candidate names to enable comparison
            candidate_names_list[-i] = "".join(char for char in candidate_names_list[-i] if char.isalpha()).lower()
            # accept if every word of last names watch
            if last_names_list[-i] != candidate_names_list[-i]:
                accept_candidate = False
        if accept_candidate:
            result.append(candidate_name)
    return result


def _match_nth_name(instructor_name: str, n: int, candidate_names: list[str]) -> list[str]:
    """
    This is the next step for matching a name, after last_name_match()
    Given a name from gradedata and candidate names from last_name_match(),
    Return list of candidate names with matching nth name (first or middle).
    """
    if not candidate_names:
        return []

    # get nth name and canonicalize
    nth_name = instructor_name.strip().split(",")[1].strip().split(" ")[n]
    nth_name = "".join(char for char in nth_name if char.isalpha()).lower()
    # only check initials if full first name not provided
    initial_only = True if len(nth_name) == 1 else False

    # get number of last names
    num_last_names = len(instructor_name.split(",")[0].strip().split(" "))

    # keep list of matching candidate names
    result = []
    for candidate_name in candidate_names:
        num_candidate_names = len(candidate_name.strip().split(" "))
        if num_candidate_names <= 1:
            # avoid matching empty or one-word names
            continue
        if n >= num_candidate_names - num_last_names:
            # do not reject a candidate for not having nth name
            result.append(candidate_name)
            continue
        # get nth name of candidate name and canonicalize
        candidate_nth_name = candidate_name.strip().split(" ")[n]
        candidate_nth_name = "".join(char for char in candidate_nth_name if char.isalpha()).lower()
        # check for a match
        if (initial_only or len(candidate_nth_name) == 1) and nth_name[0] == candidate_nth_name[0]:
            # one or both names only have first initial, and the initials match
            result.append(candidate_name)
        elif nth_name == candidate_nth_name:
            # both first names are fully written out, and they match
            result.append(candidate_name)
    return result

def match_name(instructor_name: str) -> list[str]:
    """
    Given an instructor name from gradedata, return a list of matching scraped names.
    The list may be empty (no matches) or have multiple names (equally likely matches).

    Keyword arguments:
    instructor_name -- the full name of an instructor
    """
    # make sure scraped faculty names are available
    global faculty_names
    if not faculty_names:
        _reload_names_dict()
    if not faculty_names:
        raise Exception("Tried to match name without a valid scraped faculty names dictionary")

    # do not match name if not in Last, First order
    if "," not in instructor_name:
        return []
    # first, filter out by last name
    candidates = _match_last_name(instructor_name)
    # then, filter out by given names (first or middle)
    num_given_names = len(instructor_name.strip().split(",")[1].strip().split(" "))
    for n in range(num_given_names):
        candidates = _match_nth_name(instructor_name, n, candidates)
    return candidates