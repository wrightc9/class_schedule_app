#  Title:		Program driver
#  Purpose:     The driver of the overall program, including the UI. It takes in the user input, and 
#                   uses the other classes to execute their request.
# 
#  TC:          O(n^3), obtained from the highest time complexity of the classes it invokes.

import tkinter as tk
from tkinter import messagebox
from graph import Graph as g
from reader import Reader as r
from course_ui import GraphUI

def check_valid(credits, start_quarter):
    # Checks to see if the csv format is good
    if not read_major.valid_format[0]:
        messagebox.showerror("Error", read_major.valid_format[1])
        return False
    
    # Checks that the input for credits is a number
    if not credits.isnumeric() and credits != '':
        message = "Invalid input. Please enter a number."
        messagebox.showerror("Error", message)
        return False

    # Checks to make sure that the input for start_quarter is a number
    if not start_quarter.isnumeric() and start_quarter != '':
        message = "Invalid input. Please enter a number from 1 - 3"
        messagebox.showerror("Error", message)
        return False
    
    return True

# writes the schedule to a file
def create_schedule_file(schedule):
    file = open("major_schedule.txt", 'w')
    file.write(str(schedule))
    file.close()

# Create button press function
def button_press(file_name, credits, start_quarter):
    # Adding a clear to reader to ensure old data is wiped (TESTING)
    read_major.clear()
    read_major.read(file_name)
    
    # Message about how to toggle full screen mode
    messagebox.showwarning("INFO", "When the program runs, the graph will be set to fullscreen.\nTo close this window please use CTL-F, (or CMD-W for Mac)")

    if check_valid(credits, start_quarter):
        # Creates the graph and topological sorted graph by calling those methods in graph.py
        graph_make.create_graph(read_major.courseDict) 
        graph_make.create_top_sort()
        
        # Gets the course schedule by calling the method in graph.py
        schedule = graph_make.create_schedule(credits, start_quarter)

        # Output schedule to text file
        create_schedule_file(schedule)

        # Display graph
        class_display = GraphUI(schedule, read_major)
        class_display.create_graph()

# Create the UI
root = tk.Tk()
root.geometry("500x300")
root.title("Course Schedule")
root.eval('tk::PlaceWindow . center')

# Create a label for Input File
label = tk.Label(root, text="Input File:")
label.pack()

# Create an entry field for Input File
entry = tk.Entry(root)
entry.pack()

# Create a label for Credits per quarter
label = tk.Label(root, text="Credits per quarter:")
label.pack()

# Create an entry field for Credits per quarter
entry_credit = tk.Entry(root)
entry_credit.pack()

# Create a label for starting quarter
label = tk.Label(root, text="Starting quarter:")
label.pack()

# Create an entry for starting quarter
entry_start = tk.Entry(root)
entry_start.pack()

read_major = r()
graph_make = g()

# Creates a button that calls the button_press button
button = tk.Button(root, text="Generate Graph", command=lambda:[button_press(entry.get(), entry_credit.get(), entry_start.get())])
button.pack()

root.mainloop()