from gradeData import courseDict
from departmentData import departmentData
from crnData import crnData

def get_course_department(courseName: str) -> str:
    """Parses and returns the department potion of the coursename: i.e. MATH111 -> MATH"""
    return ''.join((char for char in courseName if not char.isdigit()))

def get_course_level(courseName: str) -> int:
    """Parses and returns the course level from the coursename: i.e. MATH111 -> 111"""
    return int(''.join((char for char in courseName if char.isdigit())))

def get_all_departments() -> list[str]:
    """Returns a set of all department names in the courseDict"""
    return { get_course_department(key) for key in courseDict }

def get_crns_by_course(courseName: str) -> list[int]:
    """Returns a set of crn codes from course instances within a particular course"""
    return { int(courseInstance["crn"]) for courseInstance in courseDict[courseName] }

def create_department_level_dict() -> dict[str, dict[int, list[int]]]:
    """
    Returns a dictionary with heirarchical information by department -> courseLevel -> list[crns]
    This dictionary is used as a lookup table to get crns belonging to a particular department, department level, or individual 
    course.
    """
    return { department : { get_course_level(course) : { crn for crn in get_crns_by_course(course) } for course in courseDict } for department in get_all_departments() }

def get_grade_data(courseInstance: dict):
    """
    Parses and returns a dictionary for grade level information associated with a particular crn.
    """
    return {key.lower(): value for key, value in courseInstance.items() if key != "crn"}

def create_crn_dict() -> dict:
    """
    Return a dictionary of the following format:
    int(crn):
    {
        'term_desc': 'season, year',
        'course_name': 'courseName',
        'instructor': 'instructorName',
        'aprec': float(percentage),
        'bprec': float(percentage),
        'cprec': float(percentage),
        'dprec': float(percentage),
        'fprec': float(percentage)
    }
    The data is gathered and parsed from the courseDict. It is augmented with course_name to allow for course_name as a groupBy key.
    """
    crnDict = {}
    for courseName, courseListing in courseDict.items():
        for courseInstance in courseListing:
            crnDict[int(courseInstance["crn"])] = get_grade_data(courseInstance) | {"course_name": courseName}
    return crnDict

def write_dict_to_file(dataName: str, dataBody: dict, filename: str):
    """Writes a dictionary to a file."""
    f = open(filename, 'w')
    f.write(dataName + " = " + str(dataBody))
    f.close()

write_dict_to_file("departmentData", create_department_level_dict(), "departmentData.py")
write_dict_to_file("crnData", create_crn_dict(), "crnData.py")
