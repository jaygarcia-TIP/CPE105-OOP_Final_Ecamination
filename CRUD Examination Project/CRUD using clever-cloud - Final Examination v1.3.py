# Author: Jay Garcia BSCPE - CPE12S1
# Created: 05/17/2024
# CRUD using clever-cloud - Final Examination v1.3

from tkinter import *
from tkinter import messagebox
import mysql.connector

mydb = mysql.connector.connect(
    host = "briqxuuhzzlbogumbfob-mysql.services.clever-cloud.com",
    user = "uxwwl3gzc1hqxj34",
    password = "MwpBfsmaeqkm1FwhTnEn",
    database = "briqxuuhzzlbogumbfob"
)
mycursor = mydb.cursor()

def EnableEntries():
    entry_FirstName["state"]= "normal"
    entry_LastName["state"]= "normal"
    entry_Age["state"]= "normal"
    entry_Sex["state"]= "normal"
    
def DisableEntries():
    entry_FirstName["state"]= "disable"
    entry_LastName["state"]= "disable"
    entry_Age["state"]= "disable"
    entry_Sex["state"]= "disable"

def ClearEntries():
    entry_FirstName.delete(0, END)
    entry_LastName.delete(0, END)
    entry_Age.delete(0, END)
    entry_Sex.delete(0, END)
    entry_Search.delete(0, END)


def Add():
    
    EnableEntries()
    ClearEntries()
    entry_FirstName.focus_set()
    button_Add["state"]= "disable"
    button_Save["state"]= "normal"
    button_Cancel["state"]= "normal"
    button_Search["state"]= "disable"
    button_Delete["state"]= "disable"
    entry_Search["state"]= "disable"
    entry_Delete["state"]= "disable"


def Cancel():
    
    ClearEntries()
    DisableEntries()
    button_Add["state"]= "normal"
    button_Save["state"]= "disable"
    button_Cancel["state"]= "disable"
    button_Search["state"]= "normal"
    button_Delete["state"]= "normal"
    entry_Search["state"]= "normal"
    entry_Delete["state"]= "normal"
    

    # User Input Error Handling
def validate_input(entry_name, field_name, max_length=None, is_integer=False, integer_range=None):
    
    valid_data = entry_name.get().strip()
    if not valid_data:
        messagebox.showwarning("Input Error", f"Do not leave {field_name} blank!")
        entry_name.delete(0, END)
        entry_name.focus_set()
        return False
    
    if max_length is not None and len(valid_data) > max_length:
        messagebox.showwarning("Input Error", f"{field_name} cannot exceed {max_length} characters!")
        entry_name.delete(0, END)
        entry_name.focus_set()
        return False
    
    if is_integer:
        try:
            int_value = int(valid_data)
            if integer_range and (int_value < integer_range[0] or int_value > integer_range[1]):
                raise ValueError()
        except ValueError:
            messagebox.showwarning("Type Error", f"{field_name} must be a valid integer!")
            entry_name.delete(0, END)
            entry_name.focus_set()
            return False
    return True


def Save():
        # User Input Validation
    if not validate_input(entry_FirstName, "First Name", max_length=50):
        return
    if not validate_input(entry_LastName, "Last Name", max_length=50):
        return
    if not validate_input(entry_Age, "Age", is_integer=True, integer_range=(1, 999)):
        return
    if not validate_input(entry_Sex, "Sex", max_length=6):
        return
    if entry_Sex.get() not in {"Male", "Female"}:
        messagebox.showwarning("Type Error Warning", "Choose between Male and Female only")
        entry_Sex.delete(0, END)
        entry_Sex.focus_set()
        return

        # Save entry to database
    try:
            # Parameterized SQL query to prevent SQL injection attacks
        sql = "INSERT INTO table_students (FirstName, LastName, Age, Sex) VALUES (%s, %s, %s, %s);"
        
        values = (
            entry_FirstName.get(),
            entry_LastName.get(),
            int(entry_Age.get()),
            entry_Sex.get()
        )
        mycursor.execute(sql, values)
        mydb.commit()
        
        mycursor.execute("SELECT studentID FROM table_students ORDER BY studentID DESC LIMIT 1")
        ID_no = mycursor.fetchone()
        messagebox.showinfo("showinfo", f"Record Saved, your ID no. is {ID_no[0]}")
        
        ClearEntries()
        DisableEntries()
        button_Add["state"]= "normal"
        button_Save["state"]= "disable"
        button_Cancel["state"]= "disable"
        button_Search["state"]= "normal"
        button_Delete["state"]= "normal"
        entry_Search["state"]= "normal"
        entry_Delete["state"]= "normal"

    except Exception as error:
            # Error Handling
        messagebox.showerror("Database Error", f"An error occurred: {error}")
        mydb.rollback()


def Search():
    
    if validate_input(entry_Search, "Student ID", is_integer=True, integer_range=(1, 9999999)):
        try:
            sql = "SELECT * FROM table_students WHERE studentID = %s"
            mycursor.execute(sql, (entry_Search.get(),))
            results = mycursor.fetchone()

            if results is not None:
                EnableEntries()
                ClearEntries()
                entry_FirstName.insert(0, results[1])
                entry_LastName.insert(0, results[2])
                entry_Age.insert(0, results[3])
                entry_Sex.insert(0, results[4])
                DisableEntries()

            else:
                ClearEntries()
                messagebox.showwarning("showwarning", "Record not found.")
        
        except Exception as error:
            messagebox.showerror("Database Error", f"An error occurred: {error}")


def Delete():
    
    if entry_Search.get() == "admin" and entry_Delete.get() == "sudo showall table_students":
        try:
            mycursor = mydb.cursor()
            mycursor.execute("SELECT * FROM table_students")
            table_students = mycursor.fetchall()
            messagebox.showinfo("admin", "Check terminal output")
            ClearEntries()
            entry_Delete.delete(0, END)
        
            for results in table_students:
                print(results)
        
        except Exception as error:
            messagebox.showerror("Database Error", f"An error occurred: {error}")
    
    elif validate_input(entry_Delete, "Student ID", is_integer=True, integer_range=(0, 9999999)):
        try:
            mycursor = mydb.cursor()
            sql = "SELECT * FROM table_students WHERE studentID = %s"
            mycursor.execute(sql, (entry_Delete.get(),))
            results = mycursor.fetchone()
        
            if results is not None:
                EnableEntries()
                ClearEntries()
                entry_FirstName.insert(0, results[1])
                entry_LastName.insert(0, results[2])
                entry_Age.insert(0, results[3])
                entry_Sex.insert(0, results[4])
                DisableEntries()
            
                if messagebox.askquestion("Delete Data", "Are you sure to delete this data?") == "yes":
                    mycursor = mydb.cursor()
                    delete_sql = "DELETE FROM table_students WHERE studentID = %s"
                    mycursor.execute(delete_sql, (entry_Delete.get(),))
                    mydb.commit()
                    messagebox.showinfo("Info", "Record deleted successfully.")
                    EnableEntries()
                    ClearEntries()
                    DisableEntries()
                    entry_Delete.delete(0, END)
            
                else:
                    messagebox.showinfo("Info", "Deletion cancelled.")
                    EnableEntries()
                    ClearEntries()
                    DisableEntries()
                    entry_Delete.delete(0, END)
        
            else:
                ClearEntries()
                messagebox.showwarning("showwarning", "Record not found.")
        except Exception as error:
            messagebox.showerror("Database Error", f"An error occurred: {error}")
            mydb.rollback()


    # main color for GUI
color_global = "gainsboro"

root = Tk()
root.title("Student Database v1.3")
root.geometry("500x600")
root.resizable(width= False, height= False)
root.configure(background= color_global)

label_title = Label(root, bg= color_global, text= "Student Database", font= "Arial 20 bold")
label_1 = Label(root, bg= color_global, text= "First Name:", font= "Arial 20 bold")
label_2 = Label(root, bg= color_global, text= "Last Name:", font= "Arial 20 bold")
label_3 = Label(root, bg= color_global, text= "Age:", font= "Arial 20 bold")
label_4 = Label(root, bg= color_global, text= "Sex:", font= "Arial 20 bold")
label_5 = Label(root, bg= color_global, text= "Search by Student ID no.", font= "Arial 12 bold")
label_6 = Label(root, bg= color_global, text= "Delete by Student ID no.", font= "Arial 12 bold")
label_Creator = Label(root, bg= color_global, text= "Created by: Jay Garcia - BSCpE", font= "Arial 8 bold")
  # place value coordinates
label_title.place(x= 250, y= 20, anchor= "center")
label_1.place(x= 20, y= 40)
label_2.place(x= 20, y= 80)
label_3.place(x= 20, y= 120)
label_4.place(x= 20, y= 160)
label_5.place(x= 20, y= 440)
label_6.place(x= 20, y= 510)
label_Creator.place(x= 325, y= 580)

entry_FirstName = Entry(root, font= "Arial 20 bold")
entry_FirstName["state"]= "disable"
entry_LastName = Entry(root, font= "Arial 20 bold")
entry_LastName["state"]= "disable"
entry_Age = Entry(root, font= "Arial 20 bold")
entry_Age["state"]= "disable"
entry_Sex = Entry(root, font= "Arial 20 bold")
entry_Sex["state"]= "disable"
entry_Search = Entry(root, font= "Arial 20 bold")
entry_Delete = Entry(root, font= "Arial 20 bold")

  # place value coordinates
entry_FirstName.place(x= 180, y= 40, width= 300)
entry_LastName.place(x= 180, y= 80, width= 300)
entry_Age.place(x= 180, y= 120, width= 300)
entry_Sex.place(x= 180, y= 160, width= 300)
entry_Search.place(x= 20, y= 465, width= 250)
entry_Delete.place(x= 20, y= 535, width= 250)

button_Add = Button(root, bg= color_global, text= "Add", font= "Arial 20 bold", command= Add)
button_Save = Button(root, bg= color_global, text= "Save", font= "Arial 20 bold", command= Save)
button_Save["state"]= "disable"
button_Cancel = Button(root, bg= color_global, text= "Cancel", font= "Arial 20 bold", command= Cancel)
button_Cancel["state"]= "disable"
button_Search = Button(root, bg= color_global, text= "Search", font= "Arial 20 bold", command= Search)
button_Delete = Button(root, bg= "firebrick1", text= "Delete", font= "Arial 20 bold", command= Delete)
  # place value coordinates
button_Add.place(x= 25, y= 220, width= 450)
button_Save.place(x= 25, y= 285, width= 450)
button_Cancel.place(x= 25, y= 350, width= 450)
button_Search.place(x= 280, y= 450, width= 195)
button_Delete.place(x= 280, y= 520, width= 195)

showvalue= StringVar()

root.mainloop()