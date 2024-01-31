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
# Setting up Styles
style = Style()
 
# This will be adding style, and naming that style variable as W.Tbutton (TButton is used for ttk.Button).
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
# Helper Functions
def enter_student_mode():
    departmentLabel.pack()
    departmentMenu.pack()
    departmentFrame.pack(fill=BOTH, expand=True)

def department_selected(self):
    # After a department is selected, the user selects a level
    get_levels()
    levelLabel.pack()
    levelMenu.pack()
    levelFrame.pack(fill=BOTH, expand=True)

    # User also selects whther to compare Instructors or Courses
    xAxisLabel.pack()
    instructorButton.pack()
    courseButton.pack()
    xAxisFrame.pack(fill=BOTH, expand=True)

# def level_selected(self):
#     # After a level is selected, the user chooses between comparing instructors or courses
#     xAxisLabel.pack()
#     instructorButton.pack()
#     courseButton.pack()
#     xAxisFrame.pack(fill=BOTH, expand=True)

def instructor_selected(self):
    # After instructor is selected, the user needs to specify which course to compare
    get_courses()
    courseLabel.pack()
    courseMenu.pack()
    courseFrame.pack(fill=BOTH, expand=True)

def course_selected(choice):
    # After course is selected (either through instructor or directly), the user chooses the data
    if choice == "Course":
         courseFrame.pack_forget() # Remove the Course Selector Frame if comparing all courses

    yAxisLabel.pack()
    aButton.pack()
    dfButton.pack()
    yAxisFrame.pack(fill=BOTH, expand=True)

def grades_selected():
    # Once Y-Axis has been selected, add Faculty/Count checkboxes to the window
    optionsLabel.pack()
    facultyCheckbox.pack()
    countCheckbox.pack()
    optionsFrame.pack(fill=BOTH, expand=True)

    # Also include Generate button since all required variables have been assigned
    generateButton.pack()
    generateFrame.pack(fill=BOTH, expand=True)

def get_levels():
    dept = departmentVar.get()
    menu = levelMenu["menu"]

    new_menu = ["All"] + data.get_course_levels_by_department(naturalSci.depts_dict[dept])

    for item in new_menu:
        menu.add_command(label=item, command= lambda value=item: levelVar.set(value))

    levelVar.set("All")

def get_courses():
    dept = departmentVar.get()
    lvl = levelVar.get()
    menu = courseMenu("menu")

    new_menu = ["All"] + data.get_course_numbers_by_department_level(naturalSci.depts_dict[dept], lvl)

    for item in new_menu:
        menu.add_command(label=item, command= lambda value=item: levelVar.set(value))

    levelVar.set("All")

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
# Department Selection and Level Dropdown Menu Frame
# These are combined to make it easier to dynamically populate the levels menu
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

levelFrame = Frame(window)
levelVar = StringVar()
levels = []
levelLabel = Label(
    levelFrame,
    text="Select a Level")
levelMenu = OptionMenu(
    levelFrame,
    levelVar, 
    *levels)#,
    #command=level_selected)

#------------------------------------------------------------------------------
# X-Axis Selection Frame (Instructors or Courses)
xAxisFrame = Frame(window)
xAxisVar = IntVar()
xAxisVar.set(-1)
xAxisLabel = Label(
    xAxisFrame,
    text="Compare Instructors or Courses")
instructorButton = Radiobutton(
    xAxisFrame,
    text = "Instructor",
    variable=xAxisVar,
    value=0,
    style='TRadiobutton',
    command=lambda: instructor_selected("Instructor"))
courseButton = Radiobutton(
    xAxisFrame,
    text = "Course",
    variable=xAxisVar,
    value=1,
    command= lambda: course_selected("Course"))

#------------------------------------------------------------------------------
# Course Selection Frame
courseFrame = Frame(xAxisFrame)
courseVar = StringVar()
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
# Y-Axis Selection Frame (A's or D's/F's)
yAxisFrame = Frame(window)
yAxisVar = IntVar()
yAxisVar.set(-1)
yAxisLabel = Label(
    yAxisFrame,
    text="Compare Percentage of A's or D's/F's")
aButton = Radiobutton(
    yAxisFrame,
    text="A's",
    variable=yAxisVar,
    value=0,
    command=grades_selected)
dfButton = Radiobutton(
    yAxisFrame,
    text="D's/F's",
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
    text="Only Include Regular Faculty",
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