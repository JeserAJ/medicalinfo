import time
import hashlib
from pyfingerprint.pyfingerprint import PyFingerprint

def enroll():
    try:
        f = PyFingerprint('/dev/ttyS0', 57600, 0xFFFFFFFF, 0x00000000)

        if ( f.verifyPassword() == False ):
            raise ValueError('The given fingerprint sensor password is wrong!')

    except Exception as e:
        print('The fingerprint sensor could not be initialized!')
        print('Exception message: ' + str(e))
        
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

        ch1 = str(f.downloadCharacteristics(0x01)).encode('utf-8')
        ch2 = str(f.downloadCharacteristics(0x02)).encode('utf-8')
        hash1 = hashlib.sha256(ch1).hexdigest()
        hash2 = hashlib.sha256(ch2).hexdigest()
        print(hash1)
        print(hash2)
    ## Compares the charbuffers
        acur=f.compareCharacteristics()
        print(acur)
        if ( acur == 0 ):
            raise Exception('Fingers do not match')

    ## Creates a template
        f.createTemplate()

    ## Saves template at new position number
        name=input('Enter name of the person')
        
        
        
        positionNumber = f.storeTemplate()
        print(hash1)
        print(hash2)
        print('Finger enrolled successfully!')
        print('New template position #' + str(positionNumber))

    except Exception as e:
        print('Operation failed!')
        print('Exception message: ' + str(e))
       
