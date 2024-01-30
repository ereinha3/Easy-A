from tkinter import *
from tkinter.ttk import *
import naturalSci

#------------------------------------------------------------------------------
# Create Window
window = Tk()
window.title('Grade Display')
window.config(bg='grey')
window.minsize(width=500, height=500)

window.columnconfigure(0, weight=1)
window.rowconfigure(0, weight=1)
window.rowconfigure(1, weight=2)
window.rowconfigure(2, weight=3)
window.rowconfigure(3, weight=4)
window.rowconfigure(4, weight=5)
window.rowconfigure(5, weight=6)

#------------------------------------------------------------------------------
# Setting up Different Styles
style = Style(window)
style.configure('new.TFrame', background='#7AC5CD')
style.configure('TLabel', background="green")

style.configure('Label1.TLabel', background="yellow")
# style.configure("Frame2.TFrame", foreground="blue")

#------------------------------------------------------------------------------
# Helper Functions
# def mode_selection():
#     # Displays initial Mode Selector Frame 
#     modeLabel.grid(row=0, column=0)
#     studentButton.grid(row=1, column=0, sticky="news")
#     adminButton.grid(row=2, column=0, sticky="news")
#     modeFrame.grid(row=0, column=0, sticky="news")

def enter_student_mode():
    print("Entered Student Mode")
    # frame.destroy()
    departmentLabel.grid(row=0)
    departmentMenu.grid(row=1)
    departmentFrame.grid(row=0, sticky="news")
    
# def enter_admin_mode(frame):
#     print("Entered Admin Mode")
#     frame.destroy()
#     adminFrame = Frame(window)
#     adminFrame.columnconfigure(0, weight=1)
#     adminFrame.rowconfigure(0, weight=1)

#     adminLabel = Label(
#         adminFrame,
#         text="Entered Admin Mode")
    
#     adminLabel.grid(row=0, column=0, sticky="news")
#     adminFrame.grid(row=0, column=0, sticky="news")

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
        yAxisLabel.grid(row=0)
        aButton.grid(row=1)
        dfButton.grid(row=2)
        yAxisFrame.grid(row=3, column=0, sticky="news")

    if choice == "A" or choice == "D/F":
        # Once Y-Axis has been selected, add Faculty/Count checkboxes to the window
        optionsLabel.grid(row=0)
        facultyCheckbox.grid(row=1)
        countCheckbox.grid(row=2)
        optionsFrame.grid(row=4, column=0, sticky="news")

        # Also include Generate button since all required variables have been assigned
        generateButton.grid(row=0)
        generateFrame.grid(row=5, column=0, sticky="news")


# All Frames are Created Below. They are not added to the Grid until they are needed
#------------------------------------------------------------------------------
# Mode Selection Frame
# modeFrame = Frame(window, style='new.TFrame')
# modeFrame.columnconfigure(0, weight=1)
# modeFrame.rowconfigure(0, weight=1)

# modeLabel = Label(
#     modeFrame,
#     text="Are You a Student or an Administrator?")
    
# studentButton = Button(
#     modeFrame,
#     text="Student",
#     command=lambda: enter_student_mode(modeFrame))
    
# adminButton = Button(
#     modeFrame,
#     text="Admin",
#     command=lambda: enter_admin_mode(modeFrame))

#------------------------------------------------------------------------------
# Department Selection Dropdown Menu Frame
departmentFrame = Frame(window, style='new.TFrame')
departmentFrame.columnconfigure(0, weight=1)
departmentFrame.rowconfigure(0, weight=1)

departmentLabel = Label(
    departmentFrame,
    text="Select a Department",
)

departmentVar = StringVar()
departments = [""] + list(naturalSci.depts_dict.values())

departmentMenu = OptionMenu(
    departmentFrame,
    departmentVar,
    *departments,
    command=display_level)

#------------------------------------------------------------------------------
# Course Level Dropdown Menu Frame
levelFrame = Frame(window)
levelFrame.columnconfigure(0, weight=1)
levelFrame.rowconfigure(0, weight=1)

levelLabel = Label(
    levelFrame,
    text="Select a Level")

levelVar = StringVar()
levels = ["", "All", "100-Level", "200-Level", "300-Level", "400-Level", "500-Level", "600-Level", "700-Level"]

levelMenu = OptionMenu(
    levelFrame,
    levelVar, 
    *levels,
    command=display_x_axis_choices)

#------------------------------------------------------------------------------
# X-Axis Selection Frame (Instructors or Courses)
xAxisFrame = Frame(window)
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
yAxisFrame = Frame(window)
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
# Options - Regular Faculty and Count Frame
optionsFrame = Frame(window)
optionsFrame.columnconfigure(0, weight=1)
optionsFrame.rowconfigure(0, weight=1)

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
generateFrame.columnconfigure(0, weight=1)
generateFrame.rowconfigure(0, weight=1)

generateButton = Button(
    generateFrame,
    text="Generate Graph",
    command=generate_graph)

#------------------------------------------------------------------------------


enter_student_mode()
# infinite loop 
window.mainloop()