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
    # Does the initial mode selection between Student/Admin
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
    print("Entered Student Mode")
    frame.destroy()
    deptLabel.grid(row=0, column=0, sticky="news")
    deptMenu.grid(row=1, column=0, sticky="news")
    deptFrame.grid(row=0, column=0, sticky="news")
    
def enter_admin_mode(frame):
    print("Entered Admin Mode")
    frame.destroy()
    adminFrame = Frame(window)
    adminFrame.columnconfigure(0, weight=1)
    adminFrame.rowconfigure(0, weight=1)

    adminLabel = Label(
        adminFrame,
        text="Entered Admin Mode")
    
    adminLabel.grid(row=0, column=0, sticky="news")
    adminFrame.grid(row=0, column=0, sticky="news")

def display_level(choice):
    levelLabel.grid(row=0)
    levelMenu.grid(row=1)
    levelFrame.grid(row=1, column=0, sticky="news")

def display_x_axis_choices(choice):
    xAxisLabel.grid(row=0, column=0, columnspan=1)
    instructorButton.grid(row=1, column=0)
    courseButton.grid(row=2, column=0)
    xAxisFrame.grid(row=2, column=0, sticky="news")

def generate_graph():
    print("Gathering Data...This is what we need to graph:")
    department = departmentVar.get()
    level = levelVar.get()
    xVariable = xAxisVar.get()
    yVariable = yAxisVar.get()
    faculty = facultyVar.get()
    count = countVar.get()
    print(f'Department: {department}\n Level: {level}\n X-Axis: {xVariable}\n Y-Axis: {yVariable}\n Include Only Faculty?: {faculty}\n Include Count?: {count}')

def selection(choice):
    if choice == "Instructor" or choice == "Course":
        # Once Instructor/Course has been selected, add Y-Axis Selector to the Window
        yAxisLabel.grid(row=0, column=0, columnspan=1)
        aButton.grid(row=1, column=0)
        dfButton.grid(row=2, column=0)
        yAxisFrame.grid(row=3, column=0, sticky="news")

    if choice == "A" or choice == "D/F":
        # Once Y-Axis has been selected, add Faculty/Count checkboxes to the window
        facultyCheckbox.grid(row=0, column=0)
        countCheckbox.grid(row=1, column=0)
        checkboxFrame.grid(row=4, column=0, sticky="news")

        # Also include Generate button since all required variables have been assigned
        generateButton.grid(row=0, column=0)
        generateFrame.grid(row=5, column=0, sticky="news")

    # if choice == "Faculty Selected":
    #     print(choice)
    # if choice == "Count Selected":
    #     print(choice)


# All Frames are Created Below. They are not added to the Grid until they are needed
#------------------------------------------------------------------------------
# Department Selection Dropdown Menu Frame
deptFrame = Frame(window, background="ivory3")
deptFrame.columnconfigure(0, weight=1)
deptFrame.rowconfigure(0, weight=1)

deptLabel = Label(
    deptFrame,
    text="Select a Department",
)

departmentVar = StringVar()
science_depts = list(naturalSci.depts_dict.values())
departmentVar.set(science_depts[0])

deptMenu = OptionMenu(
    deptFrame, 
    departmentVar, 
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

levelVar = StringVar()
levels = ["All", "100-Level", "200-Level", "300-Level", "400-Level", "500-Level", "600-Level", "700-Level"]
levelVar.set(levels[0])

levelMenu = OptionMenu(
    levelFrame,
    levelVar, 
    *levels,
    command=display_x_axis_choices)

#------------------------------------------------------------------------------
# X-Axis Selection Frame (Instructors or Courses)
xAxisFrame = Frame(window, background="ivory3")
xAxisFrame.columnconfigure(0, weight=1)
xAxisFrame.rowconfigure(0, weight=1)

xAxisVar = IntVar()

xAxisLabel = Label(
    xAxisFrame,
    text="Compare Instructors or Courses")

instructorButton = Radiobutton(
    xAxisFrame,
    text = "Instructor",
    variable=xAxisVar,
    value=0,
    command=lambda: selection("Instructor"))

courseButton = Radiobutton(
    xAxisFrame,
    text = "Course",
    variable=xAxisVar,
    value=1,
    command= lambda: selection("Course"))

#------------------------------------------------------------------------------
# Y-Axis Selection Frame (A's or D's/F's)
yAxisFrame = Frame(window, background="ivory2")
yAxisFrame.columnconfigure(0, weight=1)
yAxisFrame.rowconfigure(0, weight=1)

yAxisVar = IntVar()

yAxisLabel = Label(
    yAxisFrame,
    text="Compare Percentage of A's or D's/F's")

aButton = Radiobutton(
    yAxisFrame,
    text="A's",
    variable=yAxisVar,
    value=0,
    command=lambda: selection("A"))

dfButton = Radiobutton(
    yAxisFrame,
    text="D's/F's",
    variable=yAxisVar,
    value=1,
    command= lambda: selection("D/F"))

#------------------------------------------------------------------------------
# Regular Faculty and Count Frame
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
    offvalue=0)
    #command=lambda: selection("Faculty Selected"))

countCheckbox = Checkbutton(
    checkboxFrame,
    text="Display Count",
    variable=countVar,
    onvalue=1,
    offvalue=0)
    #command=lambda: selection("Count Selected"))

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

#------------------------------------------------------------------------------

mode_selection()
# infinite loop 
window.mainloop()