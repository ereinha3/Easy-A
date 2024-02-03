"""
Author: Morgan Jones
Last Updated: 02/02/2024

This module provides an interface through which to efficiently and easily query data from the gradeDict.py data file. This includes a series of simple, standalone helper functions to fetch specific data sets for GUI user input display, for tests (such as faculty name matching tests) and more complicated functions for grouping and aggregating data.
"""

from data.gradeDict import gradeDict
from nameMatch import match_name

def get_courses_by_department(departmentName: str) -> dict[dict]:
	"""Returns all courses in a department."""
	return gradeDict[departmentName.upper()]

def filter_courses_by_level(courses: dict[dict], level: int) -> dict[dict]:
	"""Returns a filtered set of courses within a department to include only those within the given level."""
	return { key: value for key, value in courses.items() if key // 100 == level // 100 }

def get_course_numbers_by_department(departmentName: str) -> list[int]:
	"""Returns a list of all course numbers (i.e. 111, 112, 221...) that exist within a department."""
	return [ courseNumber for courseNumber in gradeDict[departmentName].keys() ]

def get_course_levels_by_department(departmentName: str) -> list[int]:
	"""Returns a list of all course levels (i.e. 100, 200, 300...) that exist within a department."""
	levels = set()
	for courseNumber in gradeDict[departmentName].keys():
		levels.add(courseNumber // 100 * 100)
	return list(levels)

def get_course_numbers_by_department_level(departmentName: str, level: int) -> list[int]:
	"""Returns a list of all course numbers that exist with a department, filtered by a specific level."""
	return [ courseNumber for courseNumber in gradeDict[departmentName].keys() if courseNumber // 100 == level // 100 ]

def get_department_names() -> list[str]:
	"""Return the code names for all departments."""
	return [ name for name in gradeDict.keys() ]

def get_all_instructors() -> set[str]:
	"""Returns a set of instructor names across all departments."""
	names = set()
	for department, course in gradeDict.items():
		for entry in course.values():
			for instance in entry:
				names.add(instance.get("instructor"))
	return names

def get_instructors_by_department(department: str) -> set[str]:
	"""Returns a set of instructor names across all departments."""
	names = set()
	for course, entries in gradeDict[department].items():
		for instance in entries:
			names.add(instance.get("instructor"))
	return names

def get_instructors_from_courses(courses: dict[list[dict]]) -> set[str]:
	"""Return a set of instructors who have taught some filtered subset of courses."""
	instructors = set()
	for course, entries in courses.items():
		for instance in entries:
			instructors.add(instance["instructor"])
	return instructors

def filter_by_faculty_only(courses: dict[dict]) -> dict[dict]:
	"""Returns a dictionary of courses, where the course instances have been filtered only to include those instances taught by a permanent faculty member."""
	return { course : [ instance for instance in entries if match_name(instance["instructor"]) ] for course, entries in courses.items() }

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

def group_by(groupKey: str, courses: dict[dict]) -> dict[dict]:
	"""Returns a dictionary of course grade information, grouped by any valid key within the courses dict."""
	groupByData = {}
	for number, instances in courses.items():
		for courseInstance in instances:
			entryName = courseInstance[groupKey]
			gradeData = {"course_count": 1} | {key: float(value) for key, value in courseInstance.items() if 'prec' in key}
			if entryName not in groupByData:
				groupByData[entryName] = gradeData
			else:
				groupByData[entryName] = accum(groupByData[entryName], gradeData)
	return groupByData

def agg_data(groupByData) -> dict[dict]:
	"""Normalizes accumulated grade data by course_count and returns a dictionary with only the group key, the course_count and the grade data."""
	for key, value in groupByData.items():
		courseCount = groupByData[key]["course_count"]
		groupByData[key].update({key: value / courseCount for key, value in groupByData[key].items() if "prec" in key})
	return groupByData

def query_graphing_data(department: str, level: int = -1, groupKey: str = "instructor", filterFaculty: bool = False) -> dict[dict]:
	"""
	Return a dictionary of the following format:
	'groupName': {
	'course_count':  int(total number of courses in the group) 
		'aprec':		 mean(aprec aggregated by groupKey)
		'bprec':		 mean(bprec aggregated by groupKey)
		'cprec':		 mean(cprec aggregated by groupKey)
		'dprec':		 ...
		'fprec':		 ...
	}

	Keyword arguments:
	department	 -- name of the department to query data from
	groupKey	   -- name of the data field to group by, options include 'instructor' and 'course_name'
	filterFaculty  -- whether or not to apply the faculty only filter before aggregating data
	level		  -- level of the course to query data from, if the course level is 100, 200, 300, 400, 500 or 600
					  you will instead query all data from all courses at that level
					  leave the default (-1) if you want to query all courses in the department (choose not to filter by level)
	"""
	courses = get_courses_by_department(department)

	#if level does not exist, is not an int or is negative then no filtering is done, just keep all courses in the department
	if not level or type(level) != int or level < 0:
		pass

	#get all courses in the given level
	elif level % 100 == 0:
		courses = filter_courses_by_level(courses, level)

	#get only the specified course
	else:
		courses = { level: courses[level] }

	#apply faculty only filter if given
	courses = filter_by_faculty_only(courses) if filterFaculty else courses
	
	return agg_data(group_by(groupKey, courses))

if __name__ == "__main__":
	#Example use for demonstration
	dep = get_courses_by_department("MATH")
	#print(get_all_instructors())
	facultyDep = filter_by_faculty_only(dep)
	print(get_instructors_from_courses(dep))
	print(get_instructors_from_courses(facultyDep))
	#data = query_graphing_data("math", -1, "instructor", False)
	#for key, value in data.items():
	#	print(key, value)
