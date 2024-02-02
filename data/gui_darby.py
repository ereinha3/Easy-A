"""Graphical User Interface for CS422, Group 7, Project 1 - EasyA (or JustPass)

Originally created by Darby Wright (daw) on 1/18



"""

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
    foreground = 'black')

style.configure(
    'TMenubutton',
    font = ('calibri', 12),
    foreground = 'black')

#------------------------------------------------------------------------------
# Functions
def enter_student_mode() -> None:
    """Bootstraps the process of asking the user for graphing parameters.
    
    Returns:
        None
    """
    # print(departmentMenu["menu"].keys())
    departmentMenu["menu"].configure(font = ('calibri', 12))
    # Add Department Menu Frame
    departmentLabel.pack()
    departmentMenu.pack()
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

    # Add Comparison Option Frame
    xAxisLabel.pack()
    instructorButton.pack()
    courseButton.pack()
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
    levelLabel.pack()
    levelMenu.pack()
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

    # print(courseMenu["menu"].keys())
    courseMenu["menu"].configure(font = ('calibri', 12))
    # Add Course Menu Frame
    courseLabel.pack()
    courseMenu.pack()
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
    
    # Add Grade Data Frame (A's or D/F's)
    yAxisLabel.pack()
    aButton.pack()
    dfButton.pack()
    yAxisVar.set(0)
    yAxisFrame.pack(fill=BOTH, expand=True)
    grades_selected()

def grades_selected() -> None:
    """Called every time the user selects or changes the grade option."""
    # Add Options Frame
    optionsLabel.pack()
    facultyCheckbox.pack()
    facultyVar.set(0)
    countCheckbox.pack()
    countVar.set(0)
    optionsFrame.pack(fill=BOTH, expand=True)

    # Add Generate Button Frame
    generateButton.pack()
    generateFrame.pack(fill=BOTH, expand=True)

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
    return data.get_course_levels_by_department(naturalSci.depts_dict[departmentVar.get()])

def get_courses() -> list:
    """Getter function to retreive the courses associated with the current department and level
    
    Return:
        list: strings representing courses
    """
    return data.get_course_numbers_by_department_level(naturalSci.depts_dict[departmentVar.get()], int(levelVar.get()))

def generate_graph() -> None:
    department = departmentVar.get()
    xVariable = xAxisVar.get()
    level = levelVar.get()
    course = courseVar.get()
    yVariable = yAxisVar.get()
    faculty = facultyVar.get()
    count = countVar.get()
    print(f'\nDepartment: {department}\n X-Axis: {xVariable}\n Level: {level}\n Course: {course}\n Y-Axis: {yVariable}\n Include Only Faculty?: {faculty}\n Include Count?: {count}')

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
    style='TMenubutton',
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


enter_student_mode() # bootstrap 1st frame
window.mainloop() # endless loop