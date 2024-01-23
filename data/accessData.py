from departmentData import departmentData
from crnData import crnData

def getCoursesByDepartment(departmentName):
    return departmentData[departmentName.upper()]

def filterCoursesByLevel(courses, level):
    return { key: value for key, value in courses.items() if key // 100 == level // 100 }

def getCrnsFromCourse(course):
    return { crn for crn in course }

def getCrnsFromCourses(courses):
    crns = set()
    for value in courses.values():
        for crn in value:
            crns.add(crn)
    return crns

def getGradeDataFromCrn(crn: int):
    return crnData[crn]

def getInstructorsByCrns(crns: {int}):
    return { crnData[crn]["instructor"] for crn in crns }

def accum(currentDict, newDict):
    if not currentDict:
        currentDict = newDict
        return currentDict

    for key in currentDict.keys():
        if key in newDict:
            currentDict[key] += newDict[key]
    return currentDict

def groupByInstructor(crns: {int}):
    instructors = {}
    for crn in crns:
        instructorName = crnData[crn]["instructor"]
        gradeData = {"courseCount": 1} | {key: float(value) for key, value in crnData[crn].items() if 'prec' in key}
        if instructorName not in instructors:
            instructors[instructorName] = gradeData
        else:
            instructors[instructorName] = accum(instructors[instructorName], gradeData)
    return instructors

def aggData(groupByData):
    for key, value in groupByData.items():
        courseCount = groupByData[key]["courseCount"]
        groupByData[key].update({key: value / courseCount for key, value in groupByData[key].items() if "prec" in key})
    return groupByData

math = getCoursesByDepartment("math")
math100 = filterCoursesByLevel(math, 100)
math100instructors = groupByInstructor(getCrnsFromCourses(math100))
agg = aggData(math100instructors)
for key, value in agg.items():
    if value["courseCount"] > 1:
        print(key, value)
#print(getCrnsFromCourses(math100))
