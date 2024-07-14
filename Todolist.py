from tkinter import *
from tkinter import messagebox
import sqlite3 as sql

def add_task():  
    task_string = task_field.get()  
    if len(task_string) == 0:  
        messagebox.showinfo('Error', 'Field is Empty.')  
    else:    
        tasks.append(task_string)   
        the_cursor.execute('insert into tasks values (?)', (task_string ,))    
        list_update()    
        task_field.delete(0, 'end')  
    
def list_update():    
    clear_list()    
    for task in tasks:    
        task_listbox.insert('end', task)  
  
def delete_task():  
    try:  
        the_value = task_listbox.get(task_listbox.curselection())    
        if the_value in tasks:  
            tasks.remove(the_value)    
            list_update()   
            the_cursor.execute('delete from tasks where title = ?', (the_value,))  
    except:   
        messagebox.showinfo('Error', 'No Task Selected. Cannot Delete.')        
  
def delete_all_tasks():  
    message_box = messagebox.askyesno('Delete All', 'Are you sure?')  
    if message_box == True:    
        while(len(tasks) != 0):    
            tasks.pop()    
        the_cursor.execute('delete from tasks')   
        list_update()  
   
def clear_list():   
    task_listbox.delete(0, 'end')  
  
def close():    
    print(tasks)   
    guiWindow.destroy()  
    
def retrieve_database():    
    while(len(tasks) != 0):    
        tasks.pop()    
    for row in the_cursor.execute('select title from tasks'):    
        tasks.append(row[0])  
   
if __name__ == "__main__":   
    guiWindow = Tk()   
    guiWindow.title("To-Do List")  
    guiWindow.geometry("665x400+550+250")   
    guiWindow.resizable(0, 0)  
    guiWindow.configure(bg="#A7C7E7")  # Changed background color
   
    the_connection = sql.connect('listOfTasks.db')   
    the_cursor = the_connection.cursor()   
    the_cursor.execute('create table if not exists tasks (title text)')  
    
    tasks = []  
        
    functions_frame = Frame(guiWindow, bg="#E6E6FA")  # Changed frame background color
    functions_frame.pack(side="top", expand=True, fill="both")  
  
    task_label = Label(functions_frame, text="TO-DO LIST\nEnter the Task Title:",  
        font=("Helvetica", 16, "bold"),  
        background="#E6E6FA",  # Updated background color
        foreground="#4B0082"   # Updated text color
    )    
    task_label.place(x=20, y=30)  
        
    task_field = Entry(functions_frame,  
        font=("Helvetica", 14),  
        width=42,  
        foreground="black",
        background="white",  
    )    
    task_field.place(x=230, y=35)  
    
    add_button = Button(functions_frame,  
        text="Add Task",  
        width=15,
        bg='#32CD32',  # Updated button background color
        fg='white',    # Updated button text color
        font=("Helvetica", 14, "bold"),
        command=add_task,
    )  
    del_button = Button(functions_frame,  
        text="Remove Task",  
        width=15,
        bg='#FF6347',  # Updated button background color
        fg='white',    # Updated button text color
        font=("Helvetica", 14, "bold"),
        command=delete_task,  
    )  
    del_all_button = Button(functions_frame,  
        text="Delete All",  
        width=15,
        bg='#FF4500',  # Updated button background color
        fg='white',    # Updated button text color
        font=("Helvetica", 14, "bold"),
        command=delete_all_tasks  
    )
    
    exit_button = Button(functions_frame,  
        text="Exit / Close",  
        width=52,
        bg='#1E90FF',  # Updated button background color
        fg='white',    # Updated button text color
        font=("Helvetica", 14, "bold"),
        command=close  
    )    
    add_button.place(x=20, y=80)  
    del_button.place(x=240, y=80)  
    del_all_button.place(x=460, y=80)  
    exit_button.place(x=20, y=330)  
    
    task_listbox = Listbox(functions_frame,  
        width=70,  
        height=9,  
        font=("Helvetica", 12, "bold"),
        selectmode='SINGLE',  
        background="white",
        foreground="black",    
        selectbackground="#FFD700",  # Updated selected background color
        selectforeground="black"
    )    
    task_listbox.place(x=20, y=140)  
    
    retrieve_database()  
    list_update()    
    guiWindow.mainloop()    
    the_connection.commit()  
    the_cursor.close()  
