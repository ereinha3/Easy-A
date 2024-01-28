from departmentData import departmentData
from crnData import crnData

def get_courses_by_department(departmentName: str) -> set[dict[int, set[int]]]:
    """Returns all crns in a department, organized into dicts by course level."""
    return departmentData[departmentName.upper()]

def filter_courses_by_level(courses: dict[int, set[int]], level: int) -> dict[int, set[int]]:
    """Returns a filtered set of courses within a department to include only those within the given level."""
    return { key: value for key, value in courses.items() if key // 100 == level // 100 }

def get_crns_from_course(course: dict[int, set[int]], level: int) -> set[int]:
    """Returns a set of crns associated with a course"""
    return { crn for crn in course }

def get_crns_from_courses(courses):
    """"""
    crns = set()
    for value in courses.values():
        for crn in value:
            crns.add(crn)
    return crns

def filter_by_faculty_only(crns: set[int]):
    """Not yet implemented"""
    return False

def accum(currentDict: dict[str, int], newDict: dict[str, int]) -> dict[str, int]:
    """
    Adds the values of two dictionaries together together.
    If the currentDict does not have the value instead instantialize it.
    """
    if not currentDict:
        currentDict = newDict
        return currentDict

    for key in currentDict.keys():
        if key in newDict:
            currentDict[key] += newDict[key]
    return currentDict

def group_by(groupKey: str, crns: set[int]):
    groupByData = {}
    for crn in crns:
        entryName = crnData[crn][groupKey]
        gradeData = {"course_count": 1} | {key: float(value) for key, value in crnData[crn].items() if 'prec' in key}
        if entryName not in groupByData:
            groupByData[entryName] = gradeData
        else:
            groupByData[entryName] = accum(groupByData[entryName], gradeData)
    return groupByData

def agg_data(groupByData):
    for key, value in groupByData.items():
        courseCount = groupByData[key]["course_count"]
        groupByData[key].update({key: value / courseCount for key, value in groupByData[key].items() if "prec" in key})
    return groupByData

def query_graphing_data(department: str, level: int = -1, groupKey: str = "instructor", filterFaculty: bool = False):
    """
    Return a dictionary of the following format:
    'groupName': {
        'course_count':  int(total number of courses in the group) 
        'aprec':         mean(aprec aggregated by groupKey)
        'bprec':         mean(bprec aggregated by groupKey)
        'cprec':         mean(cprec aggregated by groupKey)
        'dprec':         ...
        'fprec':         ...
    }

    Keyword arguments:
    department     -- name of the department to query data from
    groupKey       -- name of the data field to group by, options include 'instructor' and 'course_name'
    filterFaculty  -- whether or not to apply the faculty only filter before aggregating data
    level          -- level of the course to query data from, if the course level is 100, 200, 300, 400, 500 or 600
                      you will instead query all data from all courses at that level
                      leave the default (-1) if you want to query all courses in the department (choose not to filter by level)
    """
    courses = get_courses_by_department(department)
    crns = set()

    #get all courses in the given level
    if (level % 100 == 0):
        courses = filter_courses_by_level(courses, level)
        crns = get_crns_from_courses(courses)

    #get only the specified course
    elif (level % 100 > 0):
        courses = courses[level]
        crns = get_crns_from_course(courses)

    #if level is negative then no filtering is done, just keep all courses in the department

    #apply faculty only filter if given
    crns = filter_by_faculty_only(crns) if filterFaculty else crns
    return agg_data(group_by(groupKey, crns))

if __name__ == "__main__":
    #Example use for demonstration
    data = query_graphing_data("math", 100, "instructor", False)
    for key, value in data.items():
        print(key, value)
