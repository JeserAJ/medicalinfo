
from tkinter import *
from tkinter import messagebox
from tkinter import PhotoImage
import sqlite3
from sqlite3 import *
import time
import hashlib
from pyfingerprint.pyfingerprint import PyFingerprint

hash1=''
hash2=''
usr_lvl=1#5 is highest(admin) 1 is not loged in
recid=0

try:
    f = PyFingerprint('/dev/ttyS0', 57600, 0xFFFFFFFF, 0x00000000)
    con = sqlite3.connect('fingerdb')
    cursorObj = con.cursor()

    if ( f.verifyPassword() == False ):
        raise ValueError('The given fingerprint sensor password is wrong!')

except Exception as e:
    print('The fingerprint sensor could not be initialized!')
    print('Exception message: ' + str(e))
except Error:
    print(Error)
    
def dis_text():
    t_name.config(state='disabled')
    t_age.config(state='disabled')
    t_blood.config(state='disabled')
    t_organ.config(state='disabled')
    t_ph.config(state='disabled')
    t_med.config(state='disabled')

def enb_text():
    t_name.config(state='normal')
    t_age.config(state='normal')
    t_blood.config(state='normal')
    t_organ.config(state='normal')
    t_ph.config(state='normal')
    t_med.config(state='normal')    


def enroll():
    enb_text()
    t_name.delete(0,'end')
    t_age.delete(0,'end')
    t_blood.delete(0,'end')
    t_organ.delete(0,'end')
    t_ph.delete(0,'end')
    t_med.delete(0,'end')
    lpg.pack_forget()
    npg.pack_forget()  
    b_ok['state']='normal'
    emr_bt['state']='disabled'
    enrol_bt['state']='disabled'
    t_name.delete(0,'end')
    global hash1
    global hash2
    
    try:
        print('Waiting for finger...')
        op_label['text']='Waiting for finger'
        window.update()

        while ( f.readImage() == False ):
            pass

    ## Converts read image to characteristics and stores it in charbuffer 1
        f.convertImage(0x01)

    ## Checks if finger is already enrolled
        '''result = f.searchTemplate()
        positionNumber = result[0]
    
        if ( positionNumber >= 0 ):
            print('Template already exists at position #' + str(positionNumber))
            return'''
           

        print('Remove finger...')
        op_label['text']='Remove finger...'
        window.update()
        time.sleep(2)

        print('Waiting for same finger again...')
        op_label['text']='Place the finger again...'
        window.update()

    ## Wait that finger is read again
        while ( f.readImage() == False ):
            pass

    ## Converts read image to characteristics and stores it in charbuffer 2
        f.convertImage(0x02)


        hash1 = str(f.downloadCharacteristics(0x01))
        hash2 = str(f.downloadCharacteristics(0x02))
        
    ## Compares the charbuffers
        acur=f.compareCharacteristics()
        print('acuracy ='+str(acur))
        if ( acur == 0 ):
            raise Exception('Fingers do not match')

        op_label['text']='Fill your details'
        lpg.pack()
        b_ok['state']='normal'

        #print('Finger enrolled successfully!')
        #print('New template position #' + str(positionNumber))
    except Exception as e:
        print('Operation failed!')
        print('Exception message: ' + str(e))
        op_label['text']='ERROR :'+str(e)
        lpg.pack_forget()
        emr_bt['state']='normal'
        enrol_bt['state']='normal'
        hash1=''
        hash2=''
        
def btok():
    name=t_name.get()
    age=t_age.get()
    blood=t_blood.get()
    donor=t_organ.get()
    ph=t_ph.get()
    med=t_med.get()
    global hash1
    global hash2
    
    if(name==''or age==''or blood==''or donor=='' or ph==''or med==''):
        messagebox.showerror("Error", "Please fill in all the details")
        return
    
    try:
        cursorObj.execute("Insert into prints(name,hash1,hash2,age,blood,donor,phone,med) values(?,?,?,?,?,?,?,?);",(name,hash1,hash2,age,blood,donor,ph,med))
        con.commit()
        lpg.pack_forget()
        emr_bt['state']='normal'
        enrol_bt['state']='normal'
        hash1=''
        hash2=''
        op_label['text']='Finger enrolled succesfully'
    except Exception as e:
        print('Exception message: ' + str(e))
        op_label['text']='ERROR :'+str(e)
        lpg.pack_forget()
        emr_bt['state']='normal'
        enrol_bt['state']='normal'
        hash1=''
        hash2=''

        
def search():
    try:
        print('Waiting for finger...')
        op_label['text']='Waiting for finger'
        window.update()

    ## Wait that finger is read
        while ( f.readImage() == False ):
            pass

    ## Converts read image to characteristics and stores it in charbuffer 1
        f.convertImage(0x01)
        
        cursorObj.execute("select * from prints;")
        row = cursorObj.fetchall()
        i=1
        for r in row:
            s = eval(r[1])
            s2 = eval(r[2])
            f.uploadCharacteristics(0x02,s)
            if(f.compareCharacteristics()==0):
                #does not match hash1
                f.uploadCharacteristics(0x02,s2)
                if(f.compareCharacteristics() == 0):
                    print('Fingers do not match')
                    i=i+1
                    t=int(i%3)
                    srch='searching'+' '*t+'.'
                    op_label['text']=srch
                    window.update()
                    continue
                
            print('match found')
            op_label['text']='Match Found'
            window.update()
            print(r[0]+'\t'+str(r[3])+'_years_old\tBlood_group_'+r[4]+'\tOrgan_donor_'+r[5])
            return 'found',r
            break
        op_label['text']='No Match'
        return 'not',r

    except Exception as e:
        print('Operation failed!')
        print('Exception message: ' + str(e))
        op_label['text']='ERROR :'+str(e)
        


def trylogin(uname,pwd):
    global usr_lvl
    cursorObj.execute("select pwd from users where name=?;",(uname,))
    row = cursorObj.fetchall()
    if row == [(pwd,)]:
        if uname=='admin':
            usr_lvl=5
            text_login.insert(0,'Admin')
        return 1
    else:
        return 0

def login():
    lpg.pack_forget()
    uname=text_login.get()
    pwd=pwd_login.get()
    if uname =='' or pwd == '':
        messagebox.showinfo("Error", "please enter a valid user name or pasword")
    else:
        text_login.delete(0,'end')
        pwd_login.delete(0,'end')
        i=trylogin(uname,pwd)
        if i == 0:
            messagebox.showerror("Error", "invalid credentials")
        else:
            text_login['state']='disabled'
            pwd_login['state']='disabled'
            login_bt['state']='disabled'
            login_bt['text']='LOGGED IN'
            op_label['text']='Logged in sucesfully'
            enrol_bt['state']='normal'

def searchbt():
    global usr_lvl,recid
    recid=0
    emr_bt['state']='disabled'
    enrol_bt['state']='disabled'
    if usr_lvl==1:
        login_bt['state']='disabled'
    lpg.pack_forget()
    npg.pack_forget()  
    status,r=search()
    if status=='found':
        lpg.pack()
        enb_text()
        if usr_lvl>1:
            npg.pack()
            recid=r[8]
        t_name.delete(0,'end')
        t_age.delete(0,'end')
        t_blood.delete(0,'end')
        t_organ.delete(0,'end')
        t_ph.delete(0,'end')
        t_med.delete(0,'end')
        b_ok['state']='disabled'
        t_name.insert(0,r[0])
        t_age.insert(0,r[3])
        t_blood.insert(0,r[4])
        t_organ.insert(0,r[5])
        t_ph.insert(0,r[6])
        t_med.insert(0,r[7])
        dis_text()
    emr_bt['state']='normal'
    enrol_bt['state']='normal'
    emr_bt['text']='Search Again'
    if usr_lvl==1:
        login_bt['state']='normal'
        enrol_bt['state']='disabled'
def addp():
    pass

def viewp():
    global recid
    try:
        cursorObj.execute("SELECT record FROM rec where id= ?;",str(recid))
        row=cursorObj.fetchall()

        for i in row:
            it=i[0]
            imgd=PhotoImage(data=it)
            panel=Label(lpg,image=imgd)
            panel.image = imgd
            panel.grid(column=0,row=0)
            panel.after(5000, panel.destroy)
    except Exception as e:
        print('Operation failed!')
        print('Exception message: ' + str(e))
        op_label['text']='No Record'
    

window = Tk()
loginpg = Frame(window)
loginpg.pack()
searchpg = Frame(window)
searchpg.pack()
lpg = Frame(window)
lpg.pack_forget()
npg = Frame(window)
npg.pack_forget()

window.title("NETWORKED HEALTHCARE") 
window.geometry('500x500')

l_uname = Label(loginpg, text='User')
l_pwd = Label(loginpg, text='Password')
login_bt = Button(loginpg, text="Login", command=login, width=20)
emr_bt = Button(searchpg, text="Search", command=searchbt,width=25)
space1 = Label(loginpg,height=2)
space2 = Label(searchpg,height=2)
text_login = Entry(loginpg)
pwd_login = Entry(loginpg,show='*')
enrol_bt = Button(searchpg, text='Enroll', command=enroll, state=DISABLED,width=25)
#enrol_bt['state']='normal'
op_label = Label(searchpg, font=('Arial,13'))


fnt=("Verdana",12)
l_name = Label(lpg,font=fnt,text='Name')
l_age =  Label(lpg,font=fnt,text='Age')
l_blood= Label(lpg,font=fnt,text='Blood Group')
l_organ =Label(lpg,font=fnt,text='Organ donor')
l_ph =   Label(lpg,font=fnt,text='Phone Num')
l_med =  Label(lpg,font=fnt,text='Medical con')
t_name = Entry(lpg,font=fnt)
t_age = Entry(lpg,font=fnt)
t_blood = Entry(lpg,font=fnt)
t_organ = Entry(lpg,font=fnt)
t_ph = Entry(lpg,font=fnt)
t_med = Entry(lpg,font=fnt)
b_ok = Button(lpg, text='OK', command=btok)
b_add = Button(npg, text='Add', command=addp)
b_view = Button(npg, text='View', command=viewp)

space1.grid(column=1,row=0) 
text_login.grid(column=2, row=1)
pwd_login.grid(column=2,row=2,pady=5)
l_uname.grid(column=1,row=1)
l_pwd.grid(column=1,row=2)
login_bt.grid(column=3, row=1,padx=30,rowspan=3)
space2.grid(column=1,row=4)
emr_bt.grid(column=1,row=5)
enrol_bt.grid(column=1,row=7,pady=10)
op_label.grid(column=1,row=8,pady=10)
l_name.grid(column=1,row=9)
l_age.grid(column=1,row=10)
l_blood.grid(column=1,row=11)
l_organ.grid(column=1,row=12)
l_ph.grid(column=1,row=13)
l_med.grid(column=1,row=14)
t_name.grid(column=2,row=9)
t_age.grid(column=2,row=10)
t_blood.grid(column=2,row=11)
t_organ.grid(column=2,row=12)
t_ph.grid(column=2,row=13)
t_med.grid(column=2,row=14)
b_ok.grid(column=1,row=15,pady=4)
b_add.grid(column=2,row=15)
b_view.grid(column=3,row=15)

window.mainloop()