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

def get_grade_data_from_crn(crn: int):
    return crnData[crn]

def get_instructors_by_crns(crns: {int}):
    return { crnData[crn]["instructor"] for crn in crns }

def filter_by_faculty_only():
    return True

def accum(currentDict, newDict):
    if not currentDict:
        currentDict = newDict
        return currentDict

    for key in currentDict.keys():
        if key in newDict:
            currentDict[key] += newDict[key]
    return currentDict

def group_by(groupKey: str, crns: {int}):
    groupByData = {}
    for crn in crns:
        entryName = crnData[crn][groupKey]
        gradeData = {"courseCount": 1} | {key: float(value) for key, value in crnData[crn].items() if 'prec' in key}
        if entryName not in groupByData:
            groupByData[entryName] = gradeData
        else:
            groupByData[entryName] = accum(groupByData[entryName], gradeData)
    return groupByData

def agg_data(groupByData):
    for key, value in groupByData.items():
        courseCount = groupByData[key]["courseCount"]
        groupByData[key].update({key: value / courseCount for key, value in groupByData[key].items() if "prec" in key})
    return groupByData

def query_graphing_data(department: str, level: int, groupKey: str, filterFaculty: bool):
    courses = get_courses_by_department(department)
    if (level % 100 == 0):
        courses = filter_courses_by_level(courses, level)
    elif (level % 100 > 0):
        courses = set(courses[level])
    crns = get_crns_from_courses(courses)
    crns = filterByFacultyOnly(crns) if filterFaculty else crns
    return agg_data(group_by(groupKey, crns))

#Entry Point Functions for Main Data Get
#Fetch gradeData by instructor
#Get crn set of courses (getCrnsByDepartment, byDepartmentLevel or byBource)
#Filter by faculty only (if true)

if __name__ == "__main__":
    data = query_graphing_data("math", 100, "course_name", False)
    for key, value in data.items():
        print(key, value)
'''
math = get_courses_by_department("math")
    math100 = filter_courses_by_level(math, 100)
    math100instructors = group_by("instructor", get_crns_from_courses(math100))
    agg = agg_data(math100instructors)
    for key, value in agg.items():
        if value["courseCount"] > 1:
            print(key, value)
#print(get_crns_from_courses(math100))
'''
