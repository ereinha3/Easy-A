"""
Graphical User Interface Module
CS422, Group 7, Project 1 - EasyA (or JustPass)

Created on 1/20/2024

Contributors:
Ethan R. (ear)
Darby W. (daw)

- partial implementation of object oriented version - ear 1/20/2024
- switched to functional rather than object oriented - daw 1/25/2024
- added styles to buttons and menus - daw 1/30/2024
- refactored to elminate repition within the code - daw 1/30/2024
- side-by-side comparison imlpemented - daw 1/31/2024

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
window.minsize(width=300, height=100)

#------------------------------------------------------------------------------
# Styles
style = Style()
 
style.configure(
    'G.TButton',
    font = ('calibri', 18, 'bold', 'underline'),
    foreground = 'green')

style.configure(
    'R.TButton',
    font = ('calibri', 18, 'bold', 'underline'),
    foreground = 'red')

style.configure(
    'B.TButton',
    font = ('calibri', 18, 'bold', 'underline'),
    foreground = 'blue')

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
# Command Functions
def enter_student_mode() -> None:
    """Begins asking the user for graphing parameters.
    
    Returns:
        None
    """
    # First parameter - pack the parameter container and the department selection frames
    parameterContainerFrame.pack(fill=BOTH, expand=True, side='left')
    departmentFrame.pack(fill=BOTH, expand=True)

def department_selected(self: str = None) -> None:
    """Called every time the user selects or changes the department menu option.

    Clears all parameter frames below the comparison option (x-axis) frame and
    resets the comparison option.
    
    Args:
        self (str): The department that was selected (unused)

    Returns:
        None
    """
    levelFrame.pack_forget()
    courseFrame.pack_forget()
    yAxisFrame.pack_forget()
    optionsFrame.pack_forget()
    generateFrame.pack_forget()

    xAxisVar.set(-1) # Set value to nothing
    # Second parameter - pack the compare option (x-axis) frame
    xAxisFrame.pack(fill=BOTH, expand=True)

def compare_option_selected(choice: str) -> None:
    """Called every time the user selects or changes a comparison option.

    Clears all parameter frames below the level selection frame.
    
    Args:
        choice (str): the choice the user selected, either "instructor" or "courses"

    Returns:
        None
    """
    courseFrame.pack_forget()
    yAxisFrame.pack_forget()
    optionsFrame.pack_forget()
    generateFrame.pack_forget()

    levels = []
    if choice == "instructors":
        levels.append("All") # Only allow "All" levels as an option when comparing instructors

    # Get levels for selected department, and update the level selection dropdown menu
    levels += get_levels()
    update_menu(levelMenu, levelVar, levels)
    levelVar.set("")

    # Third parameter - pack the level selection frame
    levelFrame.pack(fill=BOTH, expand=True)    

def level_selected(a: str = None, b: str = None, c: str = None) -> None:
    """Called every time the level selected variable is changed.
    This happens whenever the set() method is called on the levelVar
    variable, or when the user selects or changes the level menu option.

    Input: All inputs are dummy inputs and don't do anything. The nature
        of a trace callback requires a callback function that takes 3
        strings as input, representing qualities of the trace.

    Returns:
        None
    """
    if levelVar.get() == "":
        # Only continue if the level variable has been set
        return
    
    # Clear all parameter frames below the level frame
    courseFrame.pack_forget()
    yAxisFrame.pack_forget()
    optionsFrame.pack_forget()
    generateFrame.pack_forget()
    
    if xAxisVar.get() == 1 or levelVar.get() == "All":
        # If compare by courses selected, or if compare by instructor w/ "All" levels selected,
        # there is no need to pack the course frame since no individual course will be selected
        course_selected() # Continue as if a course has been selected
        return
    
    # Get courses for selected department and level, and update the course selection dropdown menu
    courses = ["All"] + get_courses()
    update_menu(courseMenu, courseVar, courses)
    courseVar.set("")

    # Fourth parameter - pack the course selection frame
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
    
    
    yAxisVar.set(0) # Comparing A's is the default grade (y-axis) option
    # Fifth parameter - pack the grade option (y-axis) frame
    yAxisFrame.pack(fill=BOTH, expand=True)

    # Since comparing A's is the default, we don't need to wait for user input.
    # The program will continue as if a grade option has been selected
    grades_selected()

def grades_selected() -> None:
    """Called every time the user selects or changes the grade option.
    
    Returns:
        None
    """
    facultyVar.set(0)
    countVar.set(0)
    # Sixth and seventh parameters - pack the options frame
    optionsFrame.pack(fill=BOTH, expand=True)

    # Pack generate graph frame
    generateFrame.pack(fill=BOTH, expand=True)

def generate_graph_selected() -> None:
    """Called every time the genereate graph button is pressed.

    Returns:
        None
    """
    generateFrame.pack_forget()
    # Clear the parameter container frame, allowing the graph to fill the window
    parameterContainerFrame.pack_forget()

    clearGraphsFrame.pack(fill='both', expand=True, side="bottom")

    if graph1Frame.winfo_ismapped(): # Check if first graph is already in the window
        # If so we need to generate and pack the second graph
        generate_graph_frame(graph2Frame)
        graph2Frame.pack(fill='both', expand=True, side="right")
    else:
        generate_graph_frame(graph1Frame)
        graph1Frame.pack(fill='both', expand=True, side="left")
        # Graph container needs to be packed when generating and packing the first graph
        graphContainerFrame.pack(fill=BOTH, expand=True, side="right")

def clear_graph_selected() -> None:
    """Called when the clear graph button is pressed.

    Clears the graphs from the screen and restores all frames to their original state.

    Returns:
        None
    """
    # Add the generate graph and side-by-side buttons back to their frames when the graphs are cleared
    generateButton.pack()
    sideBySideButton.pack()

    # Clear all graph frames, including the container
    graph1Frame.pack_forget()
    graph2Frame.pack_forget()
    graphContainerFrame.pack_forget()

    xAxisFrame.pack_forget()
    levelFrame.pack_forget()
    courseFrame.pack_forget()
    yAxisFrame.pack_forget()
    optionsFrame.pack_forget()
    generateFrame.pack_forget()
    clearGraphsFrame.pack_forget()

    departmentVar.set("") # Reset department selected
    enter_student_mode()
 
def side_by_side_selected() -> None:
    """Called every time the side-by-side comparison button is pressed.

    Clears all parameter frames below the department selection frame and resets
    the department selected, while keeping the graph container frame in tact and on screen.
    Then begins the process of asking for the parameters of the second graph.

    Returns:
        None
    """
    # Clear the side-by-side button so it can't be pressed again until the graphs are cleared
    sideBySideButton.pack_forget()

    xAxisFrame.pack_forget()
    levelFrame.pack_forget()
    courseFrame.pack_forget()
    yAxisFrame.pack_forget()
    optionsFrame.pack_forget()
    generateFrame.pack_forget()

    departmentVar.set("")
    enter_student_mode()

#------------------------------------------------------------------------------
# Helper Functions
def update_menu(menuWidget: OptionMenu, variable: StringVar, newMenu: list) -> None:
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

def generate_graph_frame(graphFrame: Frame) -> None:
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
    print(f"""
          Department: {department}
          X-Axis: {xVariable}
          Level: {level}
          Course: {course}
          Y-Axis: {yVariable}
          Include Only Faculty?:{faculty}
          Include Count?: {count}""")

    clear_frame(graphFrame)
    graphing.graph_in_frame(graphFrame, department, level, course, faculty, xVariable, yVariable, count)

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

departmentMenu["menu"].configure(font = ('calibri', 12)) # Styling the menu
 
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

levelMenu["menu"].configure(font = ('calibri', 12))

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

courseMenu["menu"].configure(font = ('calibri', 12))

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
    style='G.TButton',
    command=generate_graph_selected)

generateButton.pack()

#------------------------------------------------------------------------------
# Clear Graph Button Frame
clearGraphsFrame = Frame(window)
clearGraphsButton = Button(
    clearGraphsFrame,
    text="Clear Graph(s)",
    style='R.TButton',
    command=clear_graph_selected)

sideBySideButton = Button(
    clearGraphsFrame,
    text="Side-By-Side Comparison",
    style='B.TButton',
    command=side_by_side_selected)

clearGraphsButton.pack()
sideBySideButton.pack()

#------------------------------------------------------------------------------


enter_student_mode() # bootstrap first frame
window.mainloop() # endless loop