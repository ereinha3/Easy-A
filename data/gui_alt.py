from tkinter import *
from tkinter.ttk import *
import naturalSci
from dataAccess import *


#------------------------------------------------------------------------------
# Create Window
window = Tk()
window.title('Grade Display')
window.config(bg='grey')

#------------------------------------------------------------------------------
# Setting up Styles (...But FAILING...)
style = Style(window)
style.configure('TFrame', background='blue')
style.configure('TLabel', background="green")

#------------------------------------------------------------------------------
# Helper Functions
def enter_student_mode():
    departmentLabel.pack()
    departmentMenu.pack()
    departmentFrame.pack(fill=BOTH, expand=True)
    
def department_selected(self):
    # After a department is selected, the user selects a level
    levelLabel.pack()
    change_menu(levelMenu["menu"], determine_levels())
    levelMenu.pack()
    levelFrame.pack(fill=BOTH, expand=True)

def level_selected(self):
    # After a level is selected, the user chooses between comparing instructors or courses
    xAxisLabel.pack()
    instructorButton.pack()
    courseButton.pack()
    xAxisFrame.pack(fill=BOTH, expand=True)
    
def get_dept():
    """
    Obtain the department selected
    """
    return departmentVar.get()
    
def determine_levels():
    '''
    Use the selected department to find the levels available'''
    if get_dept():
        dept_code = get_dept_code_from_name(get_dept())        
        return ["All"] + get_levels_from_dept_code(dept_code)

    else:
        return [""]
    
def determine_course():
    if get_dept():
        dept_code = get_dept_code_from_name(get_dept())        
        return ["All"] + get_courses_from_dept_code(dept_code)
    else:
        return [""]
    
def change_menu(menu, queue):
    menu.delete(0, "end")
    for ele in queue:
        menu.add_command(label=ele, 
                             command=lambda value=ele: levelVar.set(value))
    
    
    
def instructor_selected(self):
    # After instructor is selected, the user needs to specify which course to compare
    courseLabel.pack()
    
    courseMenu.pack()
    courseFrame.pack(fill=BOTH, expand=True)

def course_selected(choice):
    # After course is selected (either through instructor or directly), the user chooses the data
    if choice == "Course":
         courseFrame.pack_forget()

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

def generate_graph():
    print("Gathering Data...This is what we need to graph:")
    department = departmentVar.get()
    level = levelVar.get()
    xVariable = xAxisVar.get()
    course = courseVar.get()
    yVariable = yAxisVar.get()
    faculty = facultyVar.get()
    count = countVar.get()
    print(f'Department: {department}\n Level: {level}\n X-Axis: {xVariable}\n \
        Course: {course}\n Y-Axis: {yVariable}\n Include Only Faculty?: {faculty}\n Include Count?: {count}')

# All Frames are Created Below. They are not added to the Grid until they are needed
#------------------------------------------------------------------------------
# Department Selection Dropdown Menu Frame
departmentFrame = Frame(window, style='TFrame')
departmentVar = StringVar()
departments = [""] + list(naturalSci.depts_dict.values()) # <--- This should be changed to a more dynamic approach
departmentLabel = Label(
    departmentFrame,
    text="Select a Department")
departmentMenu = OptionMenu(
    departmentFrame,
    departmentVar,
    *departments,
    command=department_selected)

#------------------------------------------------------------------------------
# Course Level Dropdown Menu Frame
levelFrame = Frame(window)
levelVar = StringVar()
levels = determine_levels() # <--- This should be changed to a more dynamic approach
levelLabel = Label(
    levelFrame,
    text="Select a Level")
levelMenu = OptionMenu(
    levelFrame,
    levelVar, 
    *levels,
    command=level_selected)

#------------------------------------------------------------------------------
# X-Axis Selection Frame (Instructors or Courses)
xAxisFrame = Frame(window)
xAxisVar = IntVar()
xAxisLabel = Label(
    xAxisFrame,
    text="Compare Instructors or Courses")
instructorButton = Radiobutton(
    xAxisFrame,
    text = "Instructor",
    variable=xAxisVar,
    value=0,
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
courses = ["", "All"] # <--- This NEEDS to be changed to a more dynamic approach
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
    command=generate_graph)

#------------------------------------------------------------------------------


enter_student_mode()
window.mainloop()
