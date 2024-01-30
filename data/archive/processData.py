from gradeData import courseDict

def get_course_department(courseName: str) -> str:
    """Parses and returns the department potion of the coursename: i.e. MATH111 -> MATH"""
    return ''.join((char for char in courseName if not char.isdigit()))

def get_course_level(courseName: str) -> int:
    """Parses and returns the course level from the coursename: i.e. MATH111 -> 111"""
    return int(''.join((char for char in courseName if char.isdigit())))

def format_course_instance(courseInstances, courseName):
    """Return a course instance with grade percentage values converted to floats, and with course_name inserted for convenience of grouping by coursename."""
    return [{ key : float(value) for key, value in courseInstance.items() if "prec" in key} | { key: value for key, value in courseInstance.items() if "prec" not in key } | { "course_name": courseName } for courseInstance in courseInstances]

def create_grade_dict() -> dict[str, dict[int, list[int]]]:
    """
    Returns a dictionary with heirarchical information by department -> [ courseNumbers ] -> [ courseInstances ].
    """
    gradeDict = { get_course_department(key): [] for key in courseDict.keys() }
    for key, value in courseDict.items():
        gradeDict[get_course_department(key)].append({get_course_level(key) : format_course_instance(value, key)})
    return gradeDict

def write_dict_to_file(dataName: str, dataBody: dict, filename: str):
    """Writes a dictionary to a file."""
    f = open(filename, 'w')
    f.write(dataName + " = " + str(dataBody))
    f.close()

write_dict_to_file("gradeDict", create_grade_dict(), "gradeDict.py")
