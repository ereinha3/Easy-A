from tkinter import *
from tkinter.ttk import *
import dataAccess as data
import naturalSci


#------------------------------------------------------------------------------
# Create Window
window = Tk()
window.title('Grade Display')
window.config(bg='grey')

#------------------------------------------------------------------------------
# Styles
style = Style()
 
style.configure(
    'W.TButton',
    font = ('calibri', 18, 'bold', 'underline'),
    foreground = 'green')

style.configure(
    'TLabel',
    font = ('calibri', 12, 'bold'),
    foreground = 'black')

style.configure(
    'TRadiobutton',
    font = ('calibri', 12),
    foreground = 'black',
    background= 'blue')


#------------------------------------------------------------------------------
# Functions
def enter_student_mode():
    # Add Department Menu Frame
    departmentLabel.pack()
    departmentMenu.pack()
    departmentFrame.pack(fill=BOTH, expand=True)

def department_selected(self):
    # Remove all frames below compare option (x-axis) frame
    levelFrame.pack_forget()
    courseFrame.pack_forget()
    yAxisFrame.pack_forget()
    optionsFrame.pack_forget()
    generateFrame.pack_forget()

    # Add Comparison Option Frame
    xAxisLabel.pack()
    instructorButton.pack()
    courseButton.pack()
    xAxisVar.set(-1)
    xAxisFrame.pack(fill=BOTH, expand=True)

def compare_option_selected(choice: str):
    # Clear all frames below the levels selection frame
    courseFrame.pack_forget()
    yAxisFrame.pack_forget()
    optionsFrame.pack_forget()
    generateFrame.pack_forget()

    levels = []
    if choice == "instructors":
        levels.append("All")

    levels += get_levels()
    change_menu(levelMenu, levels, levelVar)
    levelVar.set("")

    # Add Level Menu Frame
    levelLabel.pack()
    levelMenu.pack()
    levelFrame.pack(fill=BOTH, expand=True)    

def level_selected(a, b, c):
    # Trace Function for levelVar
    if levelVar.get() == "":
        print("Level Not Selected Yet")
        return
    
    # Clear all frames below the level frame
    yAxisFrame.pack_forget()
    optionsFrame.pack_forget()
    generateFrame.pack_forget()
    
    if xAxisVar.get() == 1: # Level Selected via Courses
        print("Level Selected via Courses")
        course_selected()
        return
    
    if levelVar.get() == "All":
        print("All levels selected. Skipping Course Selection")
        course_selected()
        return
    
    print("Level Selected")
    courses = ["All"] + get_courses()
    change_menu(courseMenu, courses, courseVar)
    courseVar.set("")

    # Add Course Menu Frame
    courseLabel.pack()
    courseMenu.pack()
    courseFrame.pack(fill=BOTH, expand=True)

def course_selected(a=None, b=None, c=None):
    # Trace Function for courseVar
    if courseVar.get() == "" and levelVar.get() != "All" and xAxisVar.get() == 0:
        print("Course Not Selected Yet")
        return
    
    # Add Grade Data Frame (A's or D/F's)
    yAxisLabel.pack()
    aButton.pack()
    dfButton.pack()
    yAxisVar.set(-1)
    yAxisFrame.pack(fill=BOTH, expand=True)

def grades_selected():
    # Add Options Frame
    optionsLabel.pack()
    facultyCheckbox.pack()
    facultyVar.set(-1)
    countCheckbox.pack()
    countVar.set(-1)
    optionsFrame.pack(fill=BOTH, expand=True)

    # Add Generate Button Frame
    generateButton.pack()
    generateFrame.pack(fill=BOTH, expand=True)

def change_menu(menuWidget: OptionMenu, newMenu: list, variable):
    menu = menuWidget["menu"]
    menu.delete(0, "end")
    for item in newMenu:
        menu.add_command(label=item, command= lambda value=item: variable.set(value))

def get_levels() -> list:
    department = departmentVar.get()
    levels = data.get_course_levels_by_department(naturalSci.depts_dict[department])
    return levels

def get_courses() -> list:
    dept = departmentVar.get()
    lvl = levelVar.get()
    courses = data.get_course_numbers_by_department_level(naturalSci.depts_dict[dept], int(lvl))
    return courses

def generate_graph():
    print("Gathering Data...This is what we need to graph:")
    department = departmentVar.get()
    level = levelVar.get()
    xVariable = xAxisVar.get()
    course = courseVar.get()
    yVariable = yAxisVar.get()
    faculty = facultyVar.get()
    count = countVar.get()
    print(f'Department: {department}\n Level: {level}\n X-Axis: {xVariable}\n Course: {course}\n Y-Axis: {yVariable}\n Include Only Faculty?: {faculty}\n Include Count?: {count}')

# All Frames are Created Below. They are not packed until they are needed
#------------------------------------------------------------------------------
# Department Selection Dropdown Menu Frame
departmentFrame = Frame(window)
departmentVar = StringVar()
departments = [""] + list(naturalSci.depts_dict.keys())
departmentLabel = Label(
    departmentFrame,
    text="Select a Department",
    style='TLabel')
departmentMenu = OptionMenu(
    departmentFrame,
    departmentVar,
    *departments,
    command=department_selected)

#------------------------------------------------------------------------------
# Comparison Option (X-Axis) Selection Frame (Instructors or Courses)
xAxisFrame = Frame(window)
xAxisVar = IntVar()
xAxisVar.set(-1)
xAxisLabel = Label(
    xAxisFrame,
    text="Compare Instructors or Courses")
instructorButton = Radiobutton(
    xAxisFrame,
    text = "Instructors",
    variable=xAxisVar,
    value=0,
    style='TRadiobutton',
    command=lambda: compare_option_selected("instructors"))
courseButton = Radiobutton(
    xAxisFrame,
    text = "Courses",
    variable=xAxisVar,
    value=1,
    command= lambda: compare_option_selected("courses"))


#------------------------------------------------------------------------------
# Level Selection Dropdown Menu Frame
levelFrame = Frame(window)
levelVar = StringVar()
levelVar.trace_add("write", level_selected)
levels = []
levelLabel = Label(
    levelFrame,
    text="Select a Level")
levelMenu = OptionMenu(
    levelFrame,
    levelVar, 
    *levels,
    command=level_selected)

#------------------------------------------------------------------------------
# Course Selection Frame
courseFrame = Frame(window)
courseVar = StringVar()
courseVar.trace_add("write", course_selected)
courses = []
courseLabel = Label(
    courseFrame,
    text="Select a Course")
courseMenu = OptionMenu(
    courseFrame,
    courseVar, 
    *courses,
    command=course_selected)

#------------------------------------------------------------------------------
# Y-Axis Selection Frame (A's or D/F's)
yAxisFrame = Frame(window)
yAxisVar = IntVar()
yAxisVar.set(-1)
yAxisLabel = Label(
    yAxisFrame,
    text="Compare Percentage of A's or D/F's")
aButton = Radiobutton(
    yAxisFrame,
    text="A's",
    variable=yAxisVar,
    value=0,
    command=grades_selected)
dfButton = Radiobutton(
    yAxisFrame,
    text="D/F's",
    variable=yAxisVar,
    value=1,
    command=grades_selected)

#------------------------------------------------------------------------------
# Options - Regular Faculty and Count Frame
optionsFrame = Frame(window)
facultyVar = IntVar()
countVar = IntVar()
optionsLabel = Label(
    optionsFrame,
    text="Options")
facultyCheckbox = Checkbutton(
    optionsFrame,
    text="Include Only Regular Faculty",
    variable=facultyVar,
    onvalue=1,
    offvalue=0)
countCheckbox = Checkbutton(
    optionsFrame,
    text="Display Count",
    variable=countVar,
    onvalue=1,
    offvalue=0)

#------------------------------------------------------------------------------
# Generate Button Frame
generateFrame = Frame(window)
generateButton = Button(
    generateFrame,
    text="Generate Graph",
    style='W.TButton',
    command=generate_graph)

#------------------------------------------------------------------------------


enter_student_mode()
window.mainloop()