from tkinter import *
import dataAccess as data
import naturalSci

#------------------------------------------------------------------------------
# Create Window
window = Tk()
window.title('Grade Display')
window.config(bg='grey')
window.minsize(width=250, height=250)

window.columnconfigure(0, weight=1)
window.rowconfigure(0, weight=1)
window.rowconfigure(1, weight=1)
window.rowconfigure(2, weight=1)
window.rowconfigure(3, weight=1)
window.rowconfigure(4, weight=1)


#------------------------------------------------------------------------------
# Helper Functions
def display_level(choice):
    dept_choice = dept_selected.get()
    print(dept_choice)
    # Aragement of widgets within Frame
    levelLabel.grid(row=0)
    levelMenu.grid(row=1)
    # Arangement of Frame Itself
    levelFrame.grid(row=1, column=0,sticky="news")

def display_choices(choice):
    level_choice = level_selected.get()
    print(level_choice)
    # Aragement of widgets within Frame
    compareByLabel.grid(row=1, column=0, columnspan=1)
    instructorButton.grid(row=2, column=0)
    courseButton.grid(row=3, column=0)
    # Arangement of Frame Itself
    compareByFrame.grid(row=2, column=0, sticky="news")

def pressed(choice):
    if choice == "instructor" or choice == "course":
        print(choice)
            # Aragement of widgets within Frame
        dataTypeLabel.grid(row=1, column=0, columnspan=1)
        aButton.grid(row=2, column=0)
        dfButton.grid(row=3, column=0)
        # Arangement of Frame Itself
        dataTypeFrame.grid(row=3, column=0, sticky="news")

    if choice == "A" or choice == "D/F":
        print(choice)
        # Aragement of widgets within Frame
        facultyCheckbox.grid(row=1, column=0)
        countCheckbox.grid(row=2, column=0)
        # Arangement of Frame Itself
        checkboxFrame.grid(row=4, column=0, sticky="news")

    if choice == "Faculty Selected":
        print(choice)
    if choice == "Count Selected":
        print(choice)

#------------------------------------------------------------------------------
# Department Selection Dropdown Menu
deptFrame = Frame(window)
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
    command=display_level) # 

deptFrame.columnconfigure(0, weight=1)
deptFrame.rowconfigure(0, weight=1)

# Arangement of Widgets within Frame
deptLabel.grid(row=0, column=0)
deptMenu.grid(row=1, column=0)
# Arangement of Frame Itself
deptFrame.grid(row=0, column=0, sticky="news")

#------------------------------------------------------------------------------
# Course Level Dropdown Menu
levelFrame = Frame(window)
levelLabel = Label(
    levelFrame,
    text="Select a Level")
level_selected = StringVar()
# dept_selected_code = data.get_courses_by_department(dept_selected.get())
# levels = sorted(data.getLevelsfromDeptCode(dept_selected_code))
# levels.append("All")
levels = ["100-Level", "200-Level", "300-Level", "400-Level", "500-Level", "600-Level", "700-Level", "All"]
level_selected.set("All")
levelMenu = OptionMenu(
    levelFrame,
    level_selected, 
    *levels,
    command=display_choices)

levelFrame.columnconfigure(0, weight=1)
levelFrame.rowconfigure(0, weight=1)

#------------------------------------------------------------------------------
# X-Axis Selection Frame
compareByFrame = Frame(window)
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
    command=lambda: pressed("instructor"))

courseButton = Radiobutton(
    compareByFrame,
    text = "Course",
    variable=compareByVar,
    value=2,
    command= lambda: pressed("course"))

compareByFrame.columnconfigure(0, weight=1)
compareByFrame.rowconfigure(0, weight=1)

#------------------------------------------------------------------------------
# Y-Axis Selection Frame
dataTypeFrame = Frame(window)
dataTypeVar = IntVar()
dataTypeLabel = Label(
    dataTypeFrame,
    text="Compare Percentage of A's or D's/F's"
)
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

dataTypeFrame.columnconfigure(0, weight=1)
dataTypeFrame.rowconfigure(0, weight=1)

#------------------------------------------------------------------------------
# Check for Regular Faculty vs All and Choice to Display Count
checkboxFrame = Frame(window)
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

checkboxFrame.columnconfigure(0, weight=1)
checkboxFrame.rowconfigure(0, weight=1)


# infinite loop 
window.mainloop()