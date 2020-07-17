

#from enroll import *
#from search import *
import sqlite3
from sqlite3 import *


import time
import hashlib
from pyfingerprint.pyfingerprint import PyFingerprint


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
   
    
print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))

        
        
def enroll():
    #try:
     #   f = PyFingerprint('/dev/ttyS0', 57600, 0xFFFFFFFF, 0x00000000)

      #  if ( f.verifyPassword() == False ):
       #     raise ValueError('The given fingerprint sensor password is wrong!')

    #except Exception as e:
     #   print('The fingerprint sensor could not be initialized!')
      #  print('Exception message: ' + str(e))
        
    try:
        print('Waiting for finger...')

    ## Wait that finger is read
        while ( f.readImage() == False ):
            pass

    ## Converts read image to characteristics and stores it in charbuffer 1
        f.convertImage(0x01)

    ## Checks if finger is already enrolled
        result = f.searchTemplate()
        positionNumber = result[0]
    
        if ( positionNumber >= 0 ):
            print('Template already exists at position #' + str(positionNumber))
            return
           

        print('Remove finger...')
        time.sleep(2)

        print('Waiting for same finger again...')

    ## Wait that finger is read again
        while ( f.readImage() == False ):
            pass

    ## Converts read image to characteristics and stores it in charbuffer 2
        f.convertImage(0x02)

        
        #hash1 = hashlib.sha256(ch1).hexdigest()
        #hash2 = hashlib.sha256(ch2).hexdigest()
        hash1 = str(f.downloadCharacteristics(0x01))
        hash2 = str(f.downloadCharacteristics(0x02))
        
    ## Compares the charbuffers
        acur=f.compareCharacteristics()
        print(acur)
        if ( acur == 0 ):
            raise Exception('Fingers do not match')

    ## Creates a template
       # f.createTemplate()

    ## Saves template at new position number
        name=input('Enter name of the person')
        age=int(input('Enter your age : '))
        blood=input('Enter your blood group : ')
        donor=input('Are you a organ donor(yes/no) ')
        
        
        #positionNumber = f.storeTemplate()
        print(hash1)
        print(hash2)
        print('Finger enrolled successfully!')
        print('New template position #' + str(positionNumber))
        
        cursorObj.execute("Insert into prints values(?,?,?,?,?,?);",(name,hash1,hash2,age,blood,donor))
        con.commit()

    except Exception as e:
        print('Operation failed!')
        print('Exception message: ' + str(e))
       
def search():
    try:
        print('Waiting for finger...')

    ## Wait that finger is read
        while ( f.readImage() == False ):
            pass

    ## Converts read image to characteristics and stores it in charbuffer 1
        f.convertImage(0x01)
        
        cursorObj.execute("select * from prints;")
        row = cursorObj.fetchall()
        
        
        for r in row:
            s = eval(r[1])
            s2 = eval(r[2])
            f.uploadCharacteristics(0x02,s)
            if(f.compareCharacteristics()==0):
                #does not match hash1
                f.uploadCharacteristics(0x02,s2)
                if(f.compareCharacteristics() == 0):
                    print('Fingers do not match')
                    continue
                
            print('match found')
            print(r[0]+'\t'+str(r[3])+'_years_old\tBlood_group_'+r[4]+'\tOrgan_donor_'+r[5])
            break

    ## Searchs template
        #result = f.searchTemplate()

        #positionNumber = result[0]
        #accuracyScore = result[1]

        #if ( positionNumber == -1 ):
         #   print('No match found!')
          
       # else:
        #    print('Found template at position #' + str(positionNumber))
         #   print('The accuracy score is: ' + str(accuracyScore))

    ## OPTIONAL stuff
    ##

    ## Loads the found template to charbuffer 1
        #f.loadTemplate(positionNumber, 0x01)

    ## Downloads the characteristics of template loaded in charbuffer 1
        #characterics = str(f.downloadCharacteristics(0x01)).encode('utf-8')

    ## Hashes characteristics of template
        #print('SHA-2 hash of template: ' + hashlib.sha256(characterics).hexdigest())
        #print(str(f.downloadCharacteristics(0x01)))

    except Exception as e:
        print('Operation failed!')
        print('Exception message: ' + str(e))
    

while(1):
    
    print('Select your operation')
    x=input(' 1.Enroll\n 2.Search\n 3.Exit\nEnter your choice---->>>')
    
    if x=='1':
        enroll()
    elif x=='2':
        search()
    elif x=='3':
        exit(1)
    else:
        default:print('Select a valid option')