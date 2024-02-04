from tkinter import *
from tkinter.ttk import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import dataAccess
                                               
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

def graph_in_frame(frame: Frame, 
                   department: str, 
                   courseLevel: int, 
                   courseNumber: int, 
                   facultyOnly: bool, 
                   groupBy: str,
                   easyA: bool,
                   count: bool):
    """Given a tkinter frame, draws a bar graph based on the parameters
    
    frame:
        A tkinter frame into which to draw the bar graph
    department:
        The sciences department from which to take the data
    courseLevel:
        The course level to filter from as an integer (400). If you don't want to select a course level, set it to -1
    courseNumber:
        The specific course number to select. If you don't want to select a course number, set it to -1
    groupBy:
        'instructor' or 'course' based on which to group by
    easyA:
        True if you want to show EasyA data, False if you want to show "just pass" data
    count:
        True if you want to show the count of each class, False if not
    """

    # Create a matplotlib figure to draw into
    fig = Figure(figsize = (5, 5), dpi = 100)

    # Select the appropriate level based on courseLevel and courseNumber
    level = -1
    if courseLevel != -1 and type(courseLevel) is int:
        level = courseLevel
    if courseNumber != -1 and type(courseNumber) is int:
        level = courseNumber

    # Get data from dataAccess module
    dept_data = dataAccess.query_graphing_data(department, level, groupBy, filterFaculty=facultyOnly)

    y_bar = []
    x_bar = []
    counts = []
    # Build up labels, values, and counts for bar plot
    for key, value in dept_data.items():
        if value["course_count"] > 0:
            if easyA == True:
                y_bar.append(dept_data[key]["aprec"])
            else:
                y_bar.append(dept_data[key]["dprec"] + dept_data[key]["fprec"])
            x_bar.append(key)
            counts.append(value["course_count"])

    # Cut out middle name for display purposes (makes names too long)
    for ind, name in enumerate(x_bar):
        print(name, len(name.split(" ")))
        if len(name.split(" ")) == 3:
            x_bar[ind] = " ".join(name.split(" ")[0:2])

    # Sort graph based on decreasing %A's or increasing %D's/F's
    if easyA == True:
        y_bar, x_bar = zip(*sorted(zip(y_bar, x_bar)))
    else:
        y_bar, x_bar = zip(*sorted(zip(y_bar, x_bar), reverse=True))

    # Add the plot to the figure and create the bar plot
    plot = fig.add_subplot(111)
    plot.bar(x_bar, y_bar, align='center')

    # Add count labels to top of the bars
    if count:
        for x, y, c in zip(x_bar, y_bar, counts):
            plot.annotate(f'{c}', xy=(x, y), ha='center', va='bottom')
    
    # Draw to the canvas (tkinter frame)
    canvas = FigureCanvasTkAgg(fig, master = frame)
    canvas.draw()

    # Set labels for axes
    ax = fig.axes[0]
    if(level != -1):
        ax.set_title(f"{department.capitalize()} {level}")
    else:
        ax.set_title(f"{department.capitalize()} Department")
    
    if groupBy == "course_name":
        ax.set_xlabel("Course")
    elif groupBy == "instructor":
        ax.set_xlabel("Instructor")
    
    if easyA == True:
        ax.set_ylabel("Percentage of A's")
    else:
        ax.set_ylabel("Percentage of D's or F's")

    # Set the bottom spacing to vary based on the length of the bar labels
    bottom_spacing = 0.1 + 0.01*(max([len(name) for name in x_bar]))

    # Set the rotation to vary based on number of bar labels
    rotation = 45 * min(len(x_bar) / 10, 1)

    # If we have more than 4 bar labels, set them to tilt and adjust the bottom spacing
    if len(x_bar) > 4:
        ax.set_xticks(ax.get_xticks(), ax.get_xticklabels(), rotation=rotation, ha='right')
        fig.subplots_adjust(bottom=bottom_spacing)
    
    # Pack the plot and the toolbar
    canvas.get_tk_widget().pack()
    toolbar = NavigationToolbar2Tk(canvas, frame)
    toolbar.update()
    canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
