
import PySimpleGUI as sg
import sys
import os
import io
import serial
from PIL import Image, ImageTk
from time import sleep
from opcua import Client
from opcua import ua
from arduino import Arduino
from Image import get_img_data
from weight import bricks, quantity, check_single
from quanim import quan
from rfidread import operator
import socket
import RPi.GPIO as GPIO

#--------------------------------------------------------PLC Interface--------------------------------------------------

url = "opc.tcp://172.20.15.1:4840"

client = Client(url)

client.connect()
print("Client Connected")

def plc_data():
    global Bricks
    global Order_ID
    global Quantities
    global Bricks_trash
    global Bricks_pack
    global flag
    global Status
    
    while True:
        flag = client.get_node("ns=2;s=|var|CECC-LK.Application.g_ctrl_modules.man_1.com")                               #read value from PLC node
        Status = flag.get_value()
        print(Status)
        if Status == 1001:                                                                                               #if tag 1001- store order info.
            flag.set_value(ua.Variant(1010, ua.VariantType.Int16))                                                       #write tag 1010
            Order_IdP = client.get_node("ns=2;s=|var|CECC-LK.Application.packML_status.parameter.carrier_order_id.value")#collect order ID
            Order_ID = Order_IdP.get_value()
            print(Order_ID)

            Brick_PLC = client.get_node("ns=2;s=|var|CECC-LK.Application.packML_status.parameter.operations_doing.value") #collect brick number- 16 digit array
            Bricks = Brick_PLC.get_value()
            Bricks_trash = [x for x in Bricks if x == 2 ]                                                                #extract operation number 2-trash
            print(Bricks_trash)
            Bricks_pack = [x for x in Bricks if x == 1]                                                                  #extract operation number 1-pack
            print(Bricks_pack)
            Bricks= [x for x in Bricks if x != 0 and x != 2 and x != 1]                                                  #extract brick operation
            bricks(Bricks)                                                                                               #send value to library weight
            print(Bricks)

            Quantity_PLC = client.get_node("ns=2;s=|var|CECC-LK.Application.packML_status.parameter.quantities_doing.value")   #extract quantities
            Quantities = Quantity_PLC.get_value()
            quantity(Quantities)                                                                                         #send value to library weight
            print(Quantities)
            window.FindElement('_OUTPUT6_').Update('order received')
            window.Refresh()
            sleep(3)
            break
        
        elif Status == 1002:                                                                                             #flag 1002 - pass by
            window.FindElement('_OUTPUT6_').Update('Sit and Relax')
            window.Refresh()
            sleep(5)

#---------------------------------------Printer-------------------------------------------------------------------------

def Printer():                                                                                                            #print sticker
    window.FindElement('_OUTPUT6_').Update('Check Printer')
    image_elem3.Update(data=get_img_data('/home/pi/practice/order_101/printer.jpg')) #printer image
    window.Refresh()
    for i in range(Quantities[i]):
        os.system("clear")
        os.system("lp -o orientation-requested=3 -o cpi=7 -o media=Custom.10x20mm printNameBadge.txt")
    
  
#------------------------------------------------Brick Information------------------------------------------------------
def yellows():                                                                                                            #update info for 1x2 yellow brick
    window.FindElement('_OUTPUT4_').Update(1)
    image_elem2.Update(data=quan(Quantities[i]))
    window.FindElement('_OUTPUT6_').Update('Take brick from box 1')
    image_elem.Update(data=get_img_data('/home/pi/practice/order_101/yellow_small.jpg')) #printer image
    window.Refresh()

def yellowm():                                                                                                            #update info for 2x2 yellow brick
    window.FindElement('_OUTPUT4_').Update(4)
    image_elem2.Update(data=quan(Quantities[i]))
    window.FindElement('_OUTPUT6_').Update('Take brick from box 2')
    image_elem.Update(data=get_img_data('/home/pi/practice/order_101/yellow.jpg'))  # printer image
    window.Refresh()


def yellowl():                                                                                                           #update info for 2x4 yellow brick
    window.FindElement('_OUTPUT4_').Update(5)
    image_elem2.Update(data=quan(Quantities[i]))
    window.FindElement('_OUTPUT6_').Update('Take brick from box 3')
    image_elem.Update(data=get_img_data('/home/pi/practice/order_101/yellow_large.jpg'))  # printer image
    window.Refresh()


def reds():                                                                                                              #update info for 2x3 red brick
    window.FindElement('_OUTPUT4_').Update(2)
    image_elem2.Update(data=quan(Quantities[i]))
    window.FindElement('_OUTPUT6_').Update('Take brick from box 4')
    image_elem.Update(data=get_img_data('/home/pi/practice/order_101/red_small.jpg'))  # printer image
    window.Refresh()


def redl():                                                                                                              #update info for 2x4 red brick
    window.FindElement('_OUTPUT4_').Update(3)
    image_elem2.Update(data=quan(Quantities[i]))
    window.FindElement('_OUTPUT6_').Update('Take brick from box 5')
    image_elem.Update(data=get_img_data('/home/pi/practice/order_101/red_large.jpg'))  # printer image
    window.Refresh()


def yellowc():                                                                                                           #update info for 2x2 customised brick
    window.FindElement('_OUTPUT4_').Update(4)
    image_elem2.Update(data=quan(Quantities[i]))
    window.FindElement('_OUTPUT6_').Update('Take brick from box 5')
    image_elem.Update(data=get_img_data('/home/pi/practice/order_101/yellow.jpg'))  # printer image
    window.Refresh()
    sleep(2)

#----------------------------------------  repeated function----------------------------------------------------------
def Correct():                                                                                                           #if brick type is correct
    window.FindElement('_OUTPUT6_').Update('Correct Brick type put in box')
    image_elem3.Update(data=get_img_data('/home/pi/practice/order_101/box.jpg'))
    window.Refresh()
    sleep(3)
    button()   
    wait_button()
    
def weigh():
    window.FindElement('_OUTPUT6_').Update('Checking Weight...')
    window.Refresh()
 
def yesCorrect():
    window.FindElement('_OUTPUT6_').Update('Correct Brick quantity, Take        Next')
    window.Refresh()
    
def NotCorrect():
    window.FindElement('_OUTPUT6_').Update('Wrong Brick type, Take Again')
    window.Refresh()

def InCorrect():
    window.FindElement('_OUTPUT6_').Update('Wrong Quantity, check Again')
    window.Refresh()

def trash():                                
    window.FindElement('_OUTPUT6_').Update('Put Order in trash')
    image_elem.Update(data=get_img_data('/home/pi/practice/order_101/trash.jpg'))
    window.Refresh()
def start():
    initiate()
    plc_data()
    window.FindElement('_OUTPUT6_').Update('press Next')
    window.Refresh()
    
def pack():
    window.FindElement('_OUTPUT6_').Update('take all bricks and but in a bag') #add image
    window.Refresh()
   
def button():
    window.FindElement('_OUTPUT6_').Update('Press black button when LED high')
    image_elem3.Update(data=get_img_data('/home/pi/practice/order_101/button.jpg'))
    window.Refresh()

def initiate():                                                                                                          #clear information from screen
    window.FindElement('_OUTPUT2_').Update('')
    window.FindElement('_OUTPUT4_').Update('')
    window.FindElement('_OUTPUT5_').Update('')
    window.FindElement('_OUTPUT6_').Update('')
    image_elem.Update(data=get_img_data('/home/pi/practice/order_101/lego.jpg'))
    image_elem2.Update(data=get_img_data('/home/pi/practice/order_101/grey.jpeg'))
    image_elem3.Update(data=get_img_data('/home/pi/practice/order_101/grey.jpeg'))
    window.Refresh()

def done():
    flag.set_value(ua.Variant(1100, ua.VariantType.Int16))                                                               #write flag 1100 when executed

#---------------------------------button--------------------------------------------------------------------------------


def wait_button():                                                                                                       #activate button
    LED = 17
    buttonp = 27

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(LED, GPIO.OUT)
    GPIO.setup(buttonp, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.output(LED, GPIO.LOW)

    try:
        while True:
            if GPIO.input(buttonp) == False:
                GPIO.output(LED,GPIO.HIGH)
                
                
                
            else:
                GPIO.output(LED,GPIO.LOW)
                break
                
            
    finally:
        GPIO.cleanup()
    
#-----------------------------------------GUI Interface-----------------------------------------------------------------

window = sg.Window('Process Order', return_keyboard_events=True,
                           location=(200, 200), size=(900,900), use_default_focus=False, auto_size_text=True, font=("Helvetica", 20))
image_elem = sg.Image(data = get_img_data('/home/pi/practice/order_101/lego.jpg'), size=(300,300))
image_elem2 = sg.Image(data = get_img_data('/home/pi/practice/order_101/grey.jpeg'), size=(200,200))
image_elem3 = sg.Image(data = get_img_data('/home/pi/practice/order_101/grey.jpeg'), size=(300,300))
col_1 = [
            [sg.T(' ' * 15)],
            [sg.Text('Press Initiate setup', size=(24,2), font=("Helvetica", 20), text_color=('blue'), key= '_OUTPUT6_')],
            [sg.T(' ' * 15)],
            [sg.T(' ' * 15)],
            [sg.T(' ' * 15)],
            [sg.T(' ' * 15)],
            [sg.T(' ' * 15)],
            [sg.RButton('Start', button_color=('white','green')), sg.RButton('Exit', button_color=('white','red')), sg.RButton('Next', button_color=('white','blue'))],
            [sg.RButton('Initiate setup', button_color=('white','Black'))],
            [sg.T(' ' * 15)],
            [sg.Text('Quantity:')],
            [sg.T(' ' * 15)],
            [sg.Text('', size=(5,1), key= '_OUTPUT5_')],
            [image_elem2]
            ]

col_2 = [
            [sg.Text('Operator Name'), sg.Text('', size=(10,1), key= '_OUTPUT7_')],
            [sg.Text('Order Number:'), sg.Text('', size=(12,1), key= '_OUTPUT2_')],
            [sg.Text('Box No.'), sg.Text('', size=(5,1), key= '_OUTPUT4_')],
            [sg.T(' ' * 10)],
            [image_elem],
            [image_elem3]
            
        ]

layout = [[sg.Column(col_1), sg.Column(col_2)]]

window.Layout(layout)
#-------------------------------------------------loop-----------------------------------------------------------------
while True:
    event, values = window.Read(timeout=0)
    if event is None or event == 'Exit':
        window.Close()
    elif event == 'Initiate setup':                                                                                      #checks operator RFID
        while True:
                window.FindElement('_OUTPUT6_').Update('place operator card on RFID')
                window.Refresh()
                sleep(2)
                initiate()
                window.FindElement('_OUTPUT7_').Update(operator())
                window.FindElement('_OUTPUT6_').Update('press Start')
                break
    elif event == 'Start':                                                                                               #fetch data from PLC
        while True:
                initiate()
                plc_data()
                window.FindElement('_OUTPUT6_').Update('press Next')
                break
    elif event == 'Next':                                                                                                #if order received
        while True:
            if len(Bricks_trash) == 1:                                                                                   #if order - trash
                trash()
                sleep(5)
                button()   
                wait_button()                                                                                            #wait for the operator to press button
                done()
                window.FindElement('_OUTPUT6_').Update('Trash Complete, fetching new order')
                window.Refresh()
                sleep(2)
                start()
                break
            elif len(Bricks_pack) == 1:                                                                                  #if order - pack
                pack()
                sleep(5)
                button()
                wait_button()
                done()
                window.FindElement('_OUTPUT6_').Update('order Complete, fetching new order')
                window.Refresh()
                start()
                sleep(2)
                break
            else:
                for i in range(len(Bricks)):                                                                             #to create an order
                    window.FindElement('_OUTPUT2_').Update(Order_ID)
                    if Bricks[i] == 300424:                                                                              #read array
                        pi_order = str(300424)
                    elif Bricks[i] == 300324:
                        pi_order = str(300324)
                    elif Bricks[i] == 300124:
                        pi_order = str(300124)
                    elif Bricks[i] == 302021:
                        pi_order = str(302021)
                    elif Bricks[i] == 302121:
                        pi_order = str(302121)
                    elif Bricks[i] == 30032401:
                        pi_order = str(30032401)
                    while True:
                        if pi_order == str(300424):
                            yellows()
                            sleep(2)
                        elif pi_order == str(300324):
                            yellowm()
                            sleep(2)
                        elif pi_order == str(300124):
                            yellowl()
                            sleep(2)
                        elif pi_order == str(302121):
                            reds()
                            sleep(2)
                        elif pi_order == str(302021):
                            redl()
                            sleep(2)
                        elif pi_order == str(30032401):
                            yellowc()
                            Printer()
                        status = Arduino(pi_order)                                                                       #send info to pick-by-light
                        if status == '11':                                                                               #if correct type
                            Correct()
                            weigh()
                            if check_single(i) == 1:                                                                     #check weight if correct
                                yesCorrect()
                                sleep(2)
                                break
                            elif check_single(i) == 0:
                                InCorrect()
                                sleep(2) 
                        elif status == '22':                                                                             # if incorrect type
                            NotCorrect()
                            sleep(2)
                    sleep(2)
                sleep(5)
                window.FindElement('_OUTPUT6_').Update('Correct number of  total bricks, But bricks in carrier')
                image_elem.Update(data=get_img_data('/home/pi/practice/order_101/carrier.jpg'))
                window.Refresh()
                sleep(2)
                button()
                wait_button()
                done()                                                                                                   #order executed
                sleep(5)
                plc_data()                                                                                               #check PLC if pack
                if Bricks_pack[0] == 1:                                                                                  #pack order
                    pack()
                    sleep(5)
                    button()
                    wait_button()
                    done()
                    window.FindElement('_OUTPUT6_').Update('order Complete, fetching new order')
                    window.Refresh() 
                    start()
                    break
                elif not Bricks_pack:                                                                                    #don't pack
                    window.FindElement('_OUTPUT6_').Update('Sit and Relax')
                    window.Refresh()
                    sleep(5)
                    break
            window.Refresh()
            sleep(2)
               
            
            
            
            
      
       
 
   
        
        
               
    




