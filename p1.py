

import hashlib
from pyfingerprint.pyfingerprint import PyFingerprint


print('Welcome to prototype1 of medical database')
print('------------------------------------------')



try:
    f = PyFingerprint('/dev/ttyS0', 57600, 0xFFFFFFFF, 0x00000000)

    if ( f.verifyPassword() == False ):
        raise ValueError('The given fingerprint sensor password is wrong!')

except Exception as e:
    print('The fingerprint sensor could not be initialized!')
    print('Exception message: ' + str(e))
    exit(1)


print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))

print('Place your finger for identification')

## Tries to search the finger and calculate hash
try:
    print('Waiting for finger...')

    ## Wait that finger is read
    while ( f.readImage() == False ):
        pass

    ## Converts read image to characteristics and stores it in charbuffer 1
    f.convertImage(0x01)

    ## Searchs template
    result = f.searchTemplate()

    positionNumber = result[0]
    accuracyScore = result[1]

    if ( positionNumber == -1 ):
        print('No match found!')
        x=input('do you want to enroll this fingerprint. 1.yes 2.no')
        if(x==1):
            print('Waiting for same finger again...')

    ## Wait that finger is read again
            while ( f.readImage() == False ):
                pass

    ## Converts read image to characteristics and stores it in charbuffer 2
            f.convertImage(0x02)

    ## Compares the charbuffers
            acur=f.compareCharacteristics()
            print(acur)
            if ( acur == 0 ):
                raise Exception('Fingers do not match')

    ## Creates a template
                f.createTemplate()

    ## Saves template at new position number
                positionNumber = f.storeTemplate()
                print('Finger enrolled successfully!')
                print('New template position #' + str(positionNumber))
                exit(0)
            else:
                print('Found template at position #' + str(positionNumber))
                print('The accuracy score is: ' + str(accuracyScore))

    ## OPTIONAL stuff
    ##

    ## Loads the found template to charbuffer 1
    f.loadTemplate(positionNumber, 0x01)

    ## Downloads the characteristics of template loaded in charbuffer 1
    characterics = str(f.downloadCharacteristics(0x01)).encode('utf-8')

    ## Hashes characteristics of template
    print('SHA-2 hash of template: ' + hashlib.sha256(characterics).hexdigest())

except Exception as e:
    print('Operation failed!')
    print('Exception message: ' + str(e))
    exit(1)
