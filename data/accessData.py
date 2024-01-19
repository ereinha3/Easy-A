from gradeData import courseDict
from numpy import mean

def getCourseDepartment(courseName):
    return ''.join((x for x in courseName if not x.isdigit()))

def getCourseLevel(courseName):
    return int(''.join((x for x in courseName if x.isdigit())))

def getCoursesByDepartment(departmentName):
    courses = courseDict.keys()
    return [course for course in courses if getCourseDepartment(course) == departmentName]

def filterCoursesByLevel(courseList, level):
    return [course for course in courseList if getCourseLevel(course) // 100 == level // 100]

def getInstructorsByCourse(course):
    return [courseInstance["instructor"] for courseInstance in courseDict[course]]

def getCourseGrades(course):
    return { key : float(val) for key, val in course.items() if "prec" in key }

#Example for quick testing
MathCourses = getCoursesByDepartment("MATH")
Math200 = filterCoursesByLevel(MathCourses, 200)
getInstructorsByCourse(Math200[0])
print(getCourseGrades(courseDict[Math200[0]][0]))
