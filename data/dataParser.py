
from archive.gradeData import courseDict
import os
from naturalSci import depts_dict
from tkinter import *

depts = set()
# Getting the department abbreviations from the data set
for key in courseDict.keys():
    name = ''.join(char for char in key if not char.isdigit())
    depts.add(name)

science_depts = []
 
for dept in depts:
    if dept in depts_dict.keys():
        science_depts.append(depts_dict[dept]) 
        




