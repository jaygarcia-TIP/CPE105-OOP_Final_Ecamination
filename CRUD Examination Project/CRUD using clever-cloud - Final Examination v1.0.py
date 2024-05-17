# Author: Jay Garcia BSCPE - CPE12S1
# Created: 05/09/2024
# CRUD using clever-cloud - Final Examination v1.0

from tkinter import *
from tkinter import messagebox
import mysql.connector

mydb = mysql.connector.connect(
    host = "localhost", # briqxuuhzzlbogumbfob-mysql.services.clever-cloud.com
    user = "root", # uxwwl3gzc1hqxj34
    password = "", # MwpBfsmaeqkm1FwhTnEn
    database = "database_Final-Examination" # briqxuuhzzlbogumbfob
)
mycursor = mydb.cursor()

def Add():
    
    EnableEntries()
    ClearEntries()
    entry_FirstName.focus_set()
    button_Add["state"]= "disable"
    button_Save["state"]= "normal"
    button_Cancel["state"]= "normal"
    button_Search["state"]= "disable"


def Save():
    # User Input Error Handling
        # Check if First Name entry is valid
    if len(entry_FirstName.get()) == 0:
        messagebox.showwarning("Input Error", "Do not leave First Name blank!")
        entry_FirstName.delete(0, END)
        entry_FirstName.focus_set()
        return
    elif len(entry_FirstName.get()) > 50:
        messagebox.showwarning("Input Error", "First Name cannot exceed 50 characters!")
        entry_FirstName.delete(0, END)
        entry_FirstName.focus_set()
        return
    
        # Check if Last Name entry is valid
    if len(entry_LastName.get()) == 0:
        messagebox.showwarning("Input Error", "Do not leave Last Name blank!")
        entry_LastName.delete(0, END)
        entry_LastName.focus_set()
        return
    elif len(entry_LastName.get()) > 50:
        messagebox.showwarning("Input Error", "Last Name cannot exceed 50 characters!")
        entry_LastName.delete(0, END)
        entry_LastName.focus_set()
        return
    
        # Check if Age entry length is valid
    if len(entry_Age.get()) == 0:
        messagebox.showwarning("Input Error", "Do not leave Age blank!")
        entry_Age.delete(0, END)
        entry_Age.focus_set()
        return
    else:
        try:
                # Check whether Age entry is in range 
            if int(entry_Age.get()) < 0 or int(entry_Age.get()) > 999:
                messagebox.showwarning("Invalid Age", "Age must be between 0 and 999!")
                entry_Age.delete(0, END)
                entry_Age.focus_set()
                return
            # Execute when the entry input is a string
        except ValueError:
            messagebox.showwarning("Type Error", "Age must be a valid integer!")
            entry_Age.delete(0, END)
            entry_Age.focus_set()
            return

        # Check if Sex entry is valid
    if len(entry_Sex.get()) == 0:
        messagebox.showwarning("Input Error", "Do not leave Sex blank!")
        entry_Sex.delete(0, END)
        entry_Sex.focus_set()
        return
    elif len(entry_Sex.get()) > 6:
        messagebox.showwarning("Input Error", "Sex cannot exceed 6 characters!")
        entry_Sex.delete(0, END)
        entry_Sex.focus_set()
        return
    elif entry_Sex.get() != "Male" and entry_Sex.get() != "Female":
        messagebox.showwarning("Type Error Warning","Choose between Male and Female only")
        entry_Sex.delete(0, END)
        entry_Sex.focus_set()
        return

        # Save entry to database
    try:
        sql = "INSERT INTO table_students VALUES (NULL, '" + entry_FirstName.get() + "', '" + entry_LastName.get() + "', " + entry_Age.get() + ", '" + entry_Sex.get() + "')"
        mycursor.execute(sql)
        mydb.commit()
        
        mycursor.execute("SELECT studentID FROM table_students ORDER BY studentID DESC LIMIT 1")
        ID_no = mycursor.fetchone()
        messagebox.showinfo("showinfo", f"Record Saved, your ID no. is {ID_no[0]}")
        
        ClearEntries()
        button_Add["state"]= "normal"
        button_Save["state"]= "disable"
        DisableEntries()

    except Exception as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")
        mydb.rollback()
        

def Cancel():
    
    button_Add["state"]= "normal"
    button_Save["state"]= "disable"
    button_Cancel["state"]= "disable"
    button_Search["state"]= "normal"
    ClearEntries()
    DisableEntries()
    

def Search():
   
    if (entry_Search.get() == ""):
        messagebox.showwarning("showwarning", "Search textbox is blank")
   
    else:
        button_Add["state"]= "normal"
        button_Save["state"]= "disable"
        button_Cancel["state"]= "disable"
       
        mycursor.execute("SELECT * FROM table_students WHERE studentID=" + entry_Search.get())
        rows = mycursor.fetchone()
       
        if (not(rows==None)):
            EnableEntries()
            ClearEntries()
            entry_FirstName.insert(0, rows[1])
            entry_LastName.insert(0, rows[2])
            entry_Age.insert(0, rows[3])
            entry_Sex.insert(0, rows[4])
            DisableEntries()

        else:
            EnableEntries()
            ClearEntries()
            messagebox.showwarning("showwarning", "Record not found")


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

root = Tk()
root.title("Database Example")
root.geometry("500x500")
root.resizable(width= False, height= False)

label_title = Label(root, text= "Database Input", font= "Arial 20 bold")
label_1 = Label(root, text= "First Name:", font= "Arial 20 bold")
label_2 = Label(root, text= "Last Name:", font= "Arial 20 bold")
label_3 = Label(root, text= "Age:", font= "Arial 20 bold")
label_4 = Label(root, text= "Sex:", font= "Arial 20 bold")
label_5 = Label(root, text= "ID no.:", font= "Arial 20 bold")
label_Creator = Label(root, text= "Created by: Jay Garcia - BSCpE", font= "Arial 8 bold")
  # place value coordinates
label_title.place(x= 250, y= 20, anchor= "center")
label_1.place(x= 20, y= 40)
label_2.place(x= 20, y= 80)
label_3.place(x= 20, y= 120)
label_4.place(x= 20, y= 160)
label_5.place(x= 20, y= 420)
label_Creator.place(x= 325, y= 480)

entry_FirstName = Entry(root, font= "Arial 20 bold")
entry_FirstName["state"]= "disable"
entry_LastName = Entry(root, font= "Arial 20 bold")
entry_LastName["state"]= "disable"
entry_Age = Entry(root, font= "Arial 20 bold")
entry_Age["state"]= "disable"
entry_Sex = Entry(root, font= "Arial 20 bold")
entry_Sex["state"]= "disable"
entry_Search = Entry(root, font= "Arial 20 bold")
  # place value coordinates
entry_FirstName.place(x= 180, y= 40, width= 300)
entry_LastName.place(x= 180, y= 80, width= 300)
entry_Age.place(x= 180, y= 120, width= 300)
entry_Sex.place(x= 180, y= 160, width= 300)
entry_Search.place(x= 120, y= 420, width= 150)

button_Add = Button(root, text= "Add", font= "Arial 20 bold", command= Add)
button_Save = Button(root, text= "Save", font= "Arial 20 bold", command= Save)
button_Save["state"]= "disable"
button_Cancel = Button(root, text= "Cancel", font= "Arial 20 bold", command= Cancel)
button_Cancel["state"]= "disable"
button_Search = Button(root, text= "Search", font= "Arial 20 bold", command= Search)
  # place value coordinates
button_Add.place(x= 25, y= 220, width= 450)
button_Save.place(x= 25, y= 280, width= 450)
button_Cancel.place(x= 25, y= 340, width= 450)
button_Search.place(x= 280, y= 410, width= 195)

showvalue= StringVar()

root.mainloop()