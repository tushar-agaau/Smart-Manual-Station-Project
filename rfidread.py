import RPi.GPIO as GPIO
import sys
sys.path.append('/home/pi/MFRC522-pytho')
from mfrc522 import SimpleMFRC522

def operator():                                                                                                          #check operator RFID
    GPIO.setwarnings(False)

    reader = SimpleMFRC522()

    print("Hold a tag near the reader")

    try:
        id, text = reader.read()
        if id == 1093900064415:
            N = 'Tushar A.'
        else:
            N = 'New Operator'
    finally:
        GPIO.cleanup()
        
    return N
