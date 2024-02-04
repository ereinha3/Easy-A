from tkinter import *
from tkinter.ttk import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import dataAccess
                                               
from matplotlib.figure import Figure

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
        The course level to filter from as an integer (400). If you don't want to select a 
    courseNumber:
        The specific course number to select. If you don't want to select a 
    groupBy:
        'instructor' or 'course' based on which to group by
    """
    fig = Figure(figsize = (5, 5), dpi = 100)
    # TODO
    # Change the logic for course level selection
    if not courseNumber:
        level = courseLevel
    else:
        level = courseNumber
    dept_data = dataAccess.query_graphing_data(department, level, groupBy, filterFaculty=facultyOnly)
    print(dept_data)
    y_bar = []
    x_bar = []
    counts = []
    for key, value in dept_data.items():
        if value["course_count"] > 0:
            if easyA == True:
                y_bar.append(dept_data[key]["aprec"])
            else:
                y_bar.append(dept_data[key]["dprec"] + dept_data[key]["fprec"])
            x_bar.append(key)
            counts.append(value["course_count"])
    
    plot = fig.add_subplot(111)
    plot.bar(x_bar, y_bar, align='center')
    if count:
        for x, y, c in zip(x_bar, y_bar, counts):
            plot.annotate(f'{c}', xy=(x, y), ha='center', va='center')
            #plot.text(x,y,c)
        
    canvas = FigureCanvasTkAgg(fig, master = frame)
    canvas.draw()
    canvas.get_tk_widget().pack()
    toolbar = NavigationToolbar2Tk(canvas, frame)
    toolbar.update()
    canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        
if __name__ == "__main__":
    my_obj = GraphObj()
    window = Tk()
    f1 = Frame(window)
    # window.mainloop()
    # my_obj.courseByInstructor(window)
    window.wm_title("Embedding in Tk")

    # fig = Figure(figsize=(5, 4), dpi=100)
    # t = [0, 1]
    # fig.add_subplot(111).plot(t, [0, 1])

    
    my_obj.courseByInstructor(f1)
    # canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
    # canvas.draw()
    # canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

    # toolbar = NavigationToolbar2Tk(canvas, root)
    # toolbar.update()
    # canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)


    def _quit():
        window.quit()     # stops mainloop
        window.destroy()  # this is necessary on Windows to prevent
                        # Fatal Python Error: PyEval_RestoreThread: NULL tstate


    button = Button(master=window, text="Quit", command=_quit)
    button.pack(side=BOTTOM)

    mainloop()
    # If you put root.destroy() here, it will cause an error if the window is
    # closed with the window manager.
    