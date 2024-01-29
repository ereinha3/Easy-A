from tkinter import *
import dataAccess as data
import naturalSci

#------------------------------------------------------------------------------
# Create Window
window = Tk()
window.title('Grade Display')
window.config(bg='grey')
# window.minsize(width=250, height=250)

window.columnconfigure(0, weight=1)
window.rowconfigure(0, weight=1)
window.rowconfigure(1, weight=1)
window.rowconfigure(2, weight=1)
window.rowconfigure(3, weight=1)
window.rowconfigure(4, weight=1)
window.rowconfigure(5, weight=1)

#------------------------------------------------------------------------------
# Helper Functions
def mode_selection():
    modeFrame = Frame(window, background="ivory2")
    modeFrame.columnconfigure(0, weight=1)
    modeFrame.rowconfigure(0, weight=1)

    modeLabel = Label(
        modeFrame,
        text="Are You a Student or an Administrator?")
    studentButton = Button(
        modeFrame,
        text="Student",
        highlightbackground='blue',
        relief="raised",
        command=lambda: enter_student_mode(modeFrame))
    adminButton = Button(
        modeFrame,
        text="Admin",
        highlightbackground="red",
        relief="raised",
        command=lambda: enter_admin_mode(modeFrame))
    
    modeLabel.grid(row=0, column=0)
    studentButton.grid(row=1, column=0, sticky="news")
    adminButton.grid(row=2, column=0, sticky="news")
    modeFrame.grid(row=0, column=0, sticky="news")

def enter_student_mode(frame):
    frame.destroy()
    # Arangement of Widgets within Frame
    deptLabel.grid(row=0, column=0, sticky="news")
    deptMenu.grid(row=1, column=0, sticky="news")
    # Arangement of Frame Itself
    deptFrame.grid(row=0, column=0, sticky="news")
    
def enter_admin_mode(frame):
    frame.destroy()
    adminFrame = Frame(window)
    adminFrame.columnconfigure(0, weight=1)
    adminFrame.rowconfigure(0, weight=1)
    print("Entered Admin Mode")

def display_level(choice):
    dept_choice = dept_selected.get()
    print(dept_choice)
    # Aragement of widgets within Frame
    levelLabel.grid(row=0)
    levelMenu.grid(row=1)
    # Arangement of Frame Itself
    levelFrame.grid(row=1, column=0, sticky="news")

def display_choices(choice):
    level_choice = level_selected.get()
    print(level_choice)
    # Aragement of widgets within Frame
    compareByLabel.grid(row=1, column=0, columnspan=1)
    instructorButton.grid(row=2, column=0)
    courseButton.grid(row=3, column=0)
    # Arangement of Frame within Window
    compareByFrame.grid(row=2, column=0, sticky="news")

def generate_graph():
    print("Data needs to be gathered and then its Graphing Time")

def pressed(choice):
    if choice == "Instructor" or choice == "Course":
        print(choice)
        # Aragement of widgets within Frame
        dataTypeLabel.grid(row=1, column=0, columnspan=1)
        aButton.grid(row=2, column=0)
        dfButton.grid(row=3, column=0)
        # Arangement of Frame within Window
        dataTypeFrame.grid(row=3, column=0, sticky="news")

    if choice == "A" or choice == "D/F":
        print(choice)
        # Aranging Widgets and Frame
        facultyCheckbox.grid(row=1, column=0)
        countCheckbox.grid(row=2, column=0)
        checkboxFrame.grid(row=4, column=0, sticky="news")

        # Also include Generate button since count/faculty is optional
        generateButton.grid(row=0, column=0)
        generateFrame.grid(row=5, column=0, sticky="news")

    if choice == "Faculty Selected":
        print(choice)
    if choice == "Count Selected":
        print(choice)


# All Frames are Created Below. They are not added to the Grid until they are needed
#------------------------------------------------------------------------------
# Department Selection Dropdown Menu
deptFrame = Frame(window, background="ivory3")
deptFrame.columnconfigure(0, weight=1)
deptFrame.rowconfigure(0, weight=1)

deptLabel = Label(
    deptFrame,
    text="Select a Department",
)
dept_selected = StringVar()
science_depts = list(naturalSci.depts_dict.values())
dept_selected.set(science_depts[0])
deptMenu = OptionMenu(
    deptFrame, 
    dept_selected, 
    *science_depts, 
    command=display_level)

#------------------------------------------------------------------------------
# Course Level Dropdown Menu Frame
levelFrame = Frame(window, background="ivory2")
levelFrame.columnconfigure(0, weight=1)
levelFrame.rowconfigure(0, weight=1)

levelLabel = Label(
    levelFrame,
    text="Select a Level")
level_selected = StringVar()
levels = ["100-Level", "200-Level", "300-Level", "400-Level", "500-Level", "600-Level", "700-Level", "All"]
level_selected.set("All")
levelMenu = OptionMenu(
    levelFrame,
    level_selected, 
    *levels,
    command=display_choices)

#------------------------------------------------------------------------------
# X-Axis Selection Frame
compareByFrame = Frame(window, background="ivory3")
compareByFrame.columnconfigure(0, weight=1)
compareByFrame.rowconfigure(0, weight=1)

compareByVar = IntVar()
compareByLabel = Label(
    compareByFrame,
    text="Compare Instructors or Courses"
)
instructorButton = Radiobutton(
    compareByFrame,
    text = "Instructor",
    variable=compareByVar,
    value=1,
    command=lambda: pressed("Instructor"))

courseButton = Radiobutton(
    compareByFrame,
    text = "Course",
    variable=compareByVar,
    value=2,
    command= lambda: pressed("Course"))

#------------------------------------------------------------------------------
# Y-Axis Selection Frame
dataTypeFrame = Frame(window, background="ivory2")
dataTypeFrame.columnconfigure(0, weight=1)
dataTypeFrame.rowconfigure(0, weight=1)

dataTypeVar = IntVar()
dataTypeLabel = Label(
    dataTypeFrame,
    text="Compare Percentage of A's or D's/F's")
aButton = Radiobutton(
    dataTypeFrame,
    text = "A's",
    variable=dataTypeVar,
    value=1,
    command=lambda: pressed("A"))

dfButton = Radiobutton(
    dataTypeFrame,
    text = "D's/F's",
    variable=dataTypeVar,
    value=2,
    command= lambda: pressed("D/F"))

#------------------------------------------------------------------------------
# Check for Regular Faculty vs All and Choice to Display Count Frame
checkboxFrame = Frame(window, background="ivory3")
checkboxFrame.columnconfigure(0, weight=1)
checkboxFrame.rowconfigure(0, weight=1)

facultyVar = IntVar()
countVar = IntVar()
facultyCheckbox = Checkbutton(
    checkboxFrame,
    text="Only Include Regular Faculty",
    variable=facultyVar,
    onvalue=1,
    offvalue=2,
    command=lambda: pressed("Faculty Selected"))
countCheckbox = Checkbutton(
    checkboxFrame,
    text="Display Count",
    variable=countVar,
    onvalue=1,
    offvalue=0,
    command=lambda: pressed("Count Selected"))

#------------------------------------------------------------------------------
# Generate Button Frame
generateFrame = Frame(window, background="ivory2")
generateFrame.columnconfigure(0, weight=1)
generateFrame.rowconfigure(0, weight=1)

generateButton = Button(
    generateFrame,
    text="Generate Graph",
    relief="raised",
    command=generate_graph)

mode_selection()
# infinite loop 
window.mainloop()