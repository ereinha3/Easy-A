'''
Project Creation - EAR - 01/16/2024'''

import tkinter as tk
from tkinter import ttk
from archive.gradeData import courseDict
from tkinter import *
from accessData import *

for key in courseDict.keys():
    group = courseDict[key]
    for element in group:
        if element["TERM_DESC"] == "Fall 2015":
            print(key)
    break


class GradeDisplayer(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(UserSelectionPage)
        
    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()
        
class UserSelectionPage(ttk.Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        Label(self, text="Select the program mode you would like to enter:").pack(side="top", fill="x", pady=5)
        Button(self, highlightbackground = "blue", text="Student", borderwidth=.2, 
                  command=lambda: parent.switch_frame(StudentPage)).pack(side = "top", expand = True, fill = "both", pady = 5, padx = 5)
        Button(self, text="Admin", highlightbackground = "red", borderwidth = 0.2,
                  command=lambda: parent.switch_frame(AdminPage)).pack(side = "top", expand = True, fill = "both", pady = 5, padx = 5)
        
        
class AdminPage(ttk.Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        Label(self, text="Entered Admin Mode.\n Please upload your new data file to the package and delete the previous file.\n Once finished, select Next.").pack(side="top", fill="x", pady=10)
        Button(self, text = "Next", command= lambda: parent.switch_frame(AdminFinishedPage)).pack(side = RIGHT, padx = 5)
        Button(self, text = "Back", command = lambda: parent.switch_frame(UserSelectionPage)).pack(side = LEFT, padx = 5)
        
class AdminFinishedPage(ttk.Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        Label(self, text="Entered Admin Mode. Please upload your new data file to the package and delete the previous file. Once finished, select Next.").pack(side="top", fill="x", pady=10)
        Button(self, text = "Next", command= lambda: parent.switch_frame)

        
class StudentPage(ttk.Frame):
    def __init__(self, parent):
        self.buttons = {}
        Frame.__init__(self, parent)
        Label(self, text="Entered Student Mode").pack(side="top", fill="x", pady=10)
        Label(self, text="Please Select a Department").pack(side="top", fill="x", pady=10)
        self.dept_selected = StringVar()
        self.science_depts = getScienceDepts()
        self.dept_selected.set(self.science_depts[0])
        self.deptMenu = OptionMenu(self, self.dept_selected, *self.science_depts).pack()
        Label(self, text="Would you like to view by course instructor or course?").pack(side="top", fill="x", pady=10)
        self.instructorButton = Button(self, pady = 10, foreground= 'black', text = "Instructor", command= lambda: self.pressed("instructor"))
        self.buttons["instructor"] = self.instructorButton
        self.instructorButton.pack(expand=True, fill="x", side= LEFT)
        self.courseButton = Button(self, foreground= 'black', pady = 10, text = "Course", command= lambda: self.pressed("course"))
        self.buttons["course"] = self.courseButton
        self.courseButton.pack(expand= True, fill="x",side= LEFT)
        Label(self, text = "If viewing by instructor, would you like to view faculty only?").pack(side="top", fill="x", pady=10)
        self.facultyButton = Button(self, text = "Faculty", pady = 10, command= lambda: self.pressed("faculty"))
        self.buttons["faculty"] = self.facultyButton
        self.facultyButton.pack(side="top", fill="x")
        Label(self, text = "Please select the department level you would like to consider.").pack(side="top", fill="x", pady=10)
        self.level_selected = StringVar()
        self.dept_selected_code = getCodefromDeptName(self.dept_selected.get())
        self.level_selected.set("None")
        self.lvlMenu = OptionMenu(self, self.level_selected, *getLevelsfromDeptCode(self.dept_selected_code)).pack()
        # self.dept_selected["command"] = self.update_levels_available()
        
    def update_levels_available(self):
        # self.lvlMenu['menu'] = getLevelsfromDeptCode(getCodefromDeptName(self.dept_selected.get()))
        return
        

        
        
        
        

        
    
    def pressed(self, buttonName):
        if buttonName == "faculty":
            if self.buttons[buttonName]['fg'] == "black":
                self.buttons[buttonName]['fg'] = "blue"
            else:
                self.buttons[buttonName]['fg'] = "black"
        elif buttonName == "instructor":
            if self.buttons["course"]['fg'] == self.buttons["instructor"]['fg']:
                self.buttons['instructor'].configure(fg="blue")
            else:
                self.buttons['instructor'].configure(fg="blue")
                self.buttons["course"].configure(fg="black")
        elif buttonName == "course":
            if self.buttons["course"]['fg'] == self.buttons["instructor"]['fg']:
                self.buttons['course'].configure(fg="blue")
            else:
                self.buttons['course'].configure(fg="blue")
                self.buttons["instructor"].configure(fg="black")
        else:
            print("failed!")
        
        
    def change_x_axis(self, new):
        if new == self.courseButton:
            old = self.instructorButton
        else:
            old = self.courseButton
        if new['fg'] == old['fg']:
            new.configure(fg="blue")
        else:
            new.configure(fg="blue")
            old.configure(fg="black")
        
    def disable(self):
        return 0
            
            
        
        
        
        
if __name__ == '__main__':
    app = GradeDisplayer()
    app.mainloop()
    