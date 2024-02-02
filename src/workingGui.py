"""Graphical User Interface for CS422, Group 7, Project 1 - EasyA (or JustPass)

Originally created by Darby Wright (daw) on 1/18

"""
from tkinter import *
from tkinter.ttk import *
import dataAccess as access
import data.naturalSci as naturalSci
import graphing


#------------------------------------------------------------------------------
# Create Window
window = Tk()
window.title('Grade Display')
window.config(bg='grey')
window.minsize(width=250, height=250)

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
    foreground = 'black')

style.configure(
    'TMenubutton',
    font = ('calibri', 12),
    foreground = 'black')

#------------------------------------------------------------------------------
# Functions
def enter_student_mode() -> None:
    """Bootstraps the Program. Begins asking the user for graphing parameters.
    
    Returns:
        None
    """
    departmentMenu["menu"].configure(font = ('calibri', 12))
    # Add Department Menu Frame
    parameterContainerFrame.pack(fill=BOTH, expand=True, side='left')
    departmentFrame.pack(fill=BOTH, expand=True)

def department_selected(self: str) -> None:
    """Called every time the user selects or changes the department menu option.
    
    Args:
        self (str): The department that was selected

    Returns:
        None
    """
    # Remove all frames below comparison option (x-axis) frame
    levelFrame.pack_forget()
    courseFrame.pack_forget()
    yAxisFrame.pack_forget()
    optionsFrame.pack_forget()
    generateFrame.pack_forget()
    clearFrame.pack_forget()

    # Add Comparison Option (X-Axis) Frame
    xAxisVar.set(-1) # Set or reset default value to nothing
    xAxisFrame.pack(fill=BOTH, expand=True)

def compare_option_selected(choice: str) -> None:
    """Called every time the user selects or changes a comparison option.
    
    Args:
        choice (str): the choice the user selected, either "instructor" or "courses"

    Returns:
        None
    """
    # Clear all frames below the level menu selection frame
    courseFrame.pack_forget()
    yAxisFrame.pack_forget()
    optionsFrame.pack_forget()
    generateFrame.pack_forget()

    levels = []
    if choice == "instructors":
        levels.append("All") # Only allow "All" levels as an option when comparing instructors

    levels += get_levels()
    change_menu(levelMenu, levelVar, levels)
    levelVar.set("")

    # print(levelMenu["menu"].keys())
    levelMenu["menu"].configure(font = ('calibri', 12))
    # Add Level Menu Frame
    levelFrame.pack(fill=BOTH, expand=True)    

def level_selected(a: str=None, b: str=None, c: str=None) -> None:
    """Called every time the level selected variable is changed.
    This happens whenever the set() method is called on the levelVar
    variable, or when the user selects or changes the level menu option.

    Input: All inputs are dummy inputs and don't do anything. The nature
        of a trace callback requires a callback function that takes 3
        strings as input.

    Returns:
        None
    """
    if levelVar.get() == "":
        # Only continue if the level variable has been set
        return
    
    # Clear all frames below the level frame
    courseFrame.pack_forget()
    yAxisFrame.pack_forget()
    optionsFrame.pack_forget()
    generateFrame.pack_forget()
    
    if xAxisVar.get() == 1 or levelVar.get() == "All":
        # If compare by courses selected, or if compare by instructor w/ "All" levels selected,
        # theres no need to pack the course frame since no individual course will be selected
        course_selected()
        return
    
    courses = ["All"] + get_courses()
    change_menu(courseMenu, courseVar, courses)
    courseVar.set("")

    courseMenu["menu"].configure(font = ('calibri', 12))
    # Add Course Menu Frame
    courseFrame.pack(fill=BOTH, expand=True)

def course_selected(a: str=None, b: str=None, c: str=None) -> None:
    """Called every time the course selected variable is changed.
    This happens whenever the set() method is called on the courseVar
    variable, or when the user selects or changes the course menu option.

    Input: All inputs are dummy inputs and don't do anything. The nature
        of a trace callback requires a callback function that takes 3
        strings as input.

    Returns:
        None
    """
    if courseVar.get() == "" and levelVar.get() != "All" and xAxisVar.get() == 0:
        # Only continue if either the course variable has been set, the level variable
        # is not set to "All", or the comparison option is set to "instructors"
        return
    
    # Clear all frames below the grade selection (y-axis) frame
    optionsFrame.pack_forget()
    generateFrame.pack_forget()
    
    # Add Grade access Frame (A's or D/F's)
    yAxisVar.set(0)
    yAxisFrame.pack(fill=BOTH, expand=True)
    grades_selected()

def grades_selected() -> None:
    """Called every time the user selects or changes the grade option."""
    # Add Options Frame
    facultyVar.set(0)
    countVar.set(0)
    optionsFrame.pack(fill=BOTH, expand=True)

    # Add Generate Button Frame
    generateFrame.pack(fill=BOTH, expand=True)

def clear_graph_selected() -> None:
    # Remove All Frames Other Than Department Menu Frame
    graphContainerFrame.pack_forget()
    xAxisFrame.pack_forget()
    levelFrame.pack_forget()
    courseFrame.pack_forget()
    yAxisFrame.pack_forget()
    optionsFrame.pack_forget()
    generateFrame.pack_forget()
    clearFrame.pack_forget()

    departmentVar.set("")

def change_menu(menuWidget: OptionMenu, variable: StringVar, newMenu: list) -> None:
    """Replaces the menu options for an OptionMenu with the values in a list.
    
    Args:
        menuWidget (ttk.OptionMenu): the OptionMenu object whose menu you'd like to replace
        variable (ttk.StringVar): the StringVar objects that stores the menu selection
        newMenu (list): the list of items youd like to replace the current menu options

    Returns:
        None
    """
    # This technique for changing option menus dynamic comes from Stack Overflow
    menu = menuWidget["menu"]
    menu.delete(0, "end")
    for item in newMenu:
        menu.add_command(label=item, command= lambda value=item: variable.set(value))

def get_levels() -> list:
    """Getter function to retreive the levels associated with the current department
    
    Returns:
        list: strings representing levels
    """
    return access.get_course_levels_by_department(naturalSci.depts_dict[departmentVar.get()])

def get_courses() -> list:
    """Getter function to retreive the courses associated with the current department and level
    
    Return:
        list: strings representing courses
    """
    return access.get_course_numbers_by_department_level(naturalSci.depts_dict[departmentVar.get()], int(levelVar.get()))

def clear_frame(frame: Frame) -> None:
   for widgets in frame.winfo_children():
      widgets.destroy()

def generate_graph() -> None:
    # Gathering Parameters
    department = naturalSci.depts_dict[departmentVar.get()]
    xVariable = xAxisVar.get()
    if xVariable == 0:
        xVariable = "instructor"
    else:
        xVariable = "course_name"

    level = levelVar.get()
    if level == "All":
        level = -1
    else:
        level = int(level)

    course = courseVar.get()
    if course == "All" or course == "":
        course = -1
    else:
        course = int(course)

    course = courseVar.get()
    yVariable = yAxisVar.get()
    faculty = facultyVar.get()
    count = countVar.get()
    print(f'\nDepartment: {department}\n X-Axis: {xVariable}\n Level: {level}\n Course: {course}\n Y-Axis: {yVariable}\n Include Only Faculty?: {faculty}\n Include Count?: {count}')

    # Remove Generate Button Frame
    generateFrame.pack_forget()
    # Add Clear Graph Button Frame
    clearFrame.pack(fill='both', expand=True)
    # Add the Graph Frame
    clear_frame(graph1Frame)
    graphing.graph_in_frame(graph1Frame, department, level, course, faculty, xVariable, yVariable)
    graph1Frame.pack(fill='both', expand=True, side="left")
    graphContainerFrame.pack(fill=BOTH, expand=True, side="right")

def generate_compare_graph():
    # Gathering Parameters
    department = naturalSci.depts_dict[departmentVar.get()]
    xVariable = xAxisVar.get()
    if xVariable == 0:
        xVariable = "instructor"
    else:
        xVariable = "course_name"

    level = levelVar.get()
    if level == "All":
        level = -1
    else:
        level = int(level)

    course = courseVar.get()
    if course == "All" or course == "":
        course = -1
    else:
        course = int(course)

    course = courseVar.get()
    yVariable = yAxisVar.get()
    faculty = facultyVar.get()
    count = countVar.get()
    print(f'\nDepartment: {department}\n X-Axis: {xVariable}\n Level: {level}\n Course: {course}\n Y-Axis: {yVariable}\n Include Only Faculty?: {faculty}\n Include Count?: {count}')

    # Remove Generate Button Frame
    generateFrame.pack_forget()
    # Add Clear Graph Button Frame
    clearFrame.pack(fill='both', expand=True)
    # Add the Graph Frame
    clear_frame(graph2Frame)
    graphing.graph_in_frame(graph2Frame, department, level, course, faculty, xVariable, yVariable)
    graph2Frame.pack(fill='both', expand=True, side="right")
    # graphContainerFrame.pack(fill=BOTH, expand=True, side="right")

# All Frames are Created Below. They are not packed until they are needed
#------------------------------------------------------------------------------
# Container Frames
parameterContainerFrame = Frame(window)
graphContainerFrame = Frame(window)

#------------------------------------------------------------------------------
# Graph Frames
graph1Frame = Frame(graphContainerFrame)
graph2Frame = Frame(graphContainerFrame)

#------------------------------------------------------------------------------
# Department Selection Dropdown Menu Frame
departmentFrame = Frame(parameterContainerFrame)
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
    style='TMenubutton',
    command=department_selected)
 
departmentLabel.pack()
departmentMenu.pack()

#------------------------------------------------------------------------------
# Comparison Option (X-Axis) Selection Frame (Instructors or Courses)
xAxisFrame = Frame(parameterContainerFrame)
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

xAxisLabel.pack()
instructorButton.pack()
courseButton.pack()

#------------------------------------------------------------------------------
# Level Selection Dropdown Menu Frame
levelFrame = Frame(parameterContainerFrame)
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

levelLabel.pack()
levelMenu.pack()

#------------------------------------------------------------------------------
# Course Selection Frame
courseFrame = Frame(parameterContainerFrame)
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

courseLabel.pack()
courseMenu.pack()

#------------------------------------------------------------------------------
# Y-Axis Selection Frame (A's or D/F's)
yAxisFrame = Frame(parameterContainerFrame)
yAxisVar = IntVar()
yAxisVar.set(0)
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

yAxisLabel.pack()
aButton.pack()
dfButton.pack()

#------------------------------------------------------------------------------
# Options - Regular Faculty and Count Frame
optionsFrame = Frame(parameterContainerFrame)
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

optionsLabel.pack()
facultyCheckbox.pack()
countCheckbox.pack()

#------------------------------------------------------------------------------
# Generate Button Frame
generateFrame = Frame(parameterContainerFrame)
generateButton = Button(
    generateFrame,
    text="Generate Graph",
    style='W.TButton',
    command=generate_graph)

generateButton.pack()

#------------------------------------------------------------------------------
# Clear Graph / New Graph For Compairson Frame
clearFrame = Frame(parameterContainerFrame)
clearButton = Button(
    clearFrame,
    text="Clear Graph",
    style='W.TButton',
    command=clear_graph_selected)
compareButton = Button(
    clearFrame,
    text="Generate Additional Graph",
    style='W.TButton',
    command=generate_compare_graph)

clearButton.pack()
compareButton.pack()

#------------------------------------------------------------------------------


enter_student_mode() # bootstrap 1st frame
window.mainloop() # endless loop