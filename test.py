'''i=1
for i in range (10):
    t=int(i%3)
    s='searching'+' '*t+'.'
    print(s)
    '''
import sqlite3
from tkinter import *
from tkinter import PhotoImage

def convertToBinaryData(filename):
    #Convert digital data to binary format
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData

def insertBLOB(empId,photo):
    try:
        sqliteConnection = sqlite3.connect('fingerdb')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")
        sqlite_insert_blob_query = "INSERT INTO rec(id,record) VALUES (?, ?)"

        empPhoto = convertToBinaryData(photo)
        
        # Convert data into tuple format
        data_tuple = (empId,empPhoto)
        cursor.execute(sqlite_insert_blob_query, data_tuple)
        sqliteConnection.commit()
        print("Image and file inserted successfully as a BLOB into a table")
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert blob data into sqlite table", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            print("the sqlite connection is closed")

#insertBLOB(6,"test.png")
# insertBLOB(2, "David", "E:\pynative\Python\photos\david.jpg", "E:\pynative\Python\photos\david_resume.txt")
'''def display():
    db=sqlite3.connect('fingerdb')
    conn=db.cursor()
    conn.execute("SELECT * FROM rec")
    row=conn.fetchall()

    for i in row:

        it=i[1]
        #this= open(str(len(i[1])),'wb')
        #this.write(base64string.decode('base64'))
        #this.close
        imgd=PhotoImage(data=it)
        panel=Label(image=imgd)
        panel.image = imgd
        panel.grid()


    db.close()
    
tk=Tk()
tk.geometry('500x500')
display()'''