import sys
import os
import serial
from time import sleep
from server import runserver_s

def bricks(value):
    global Bricks
    Bricks = value
    
    
def quantity(value):
    global Quantities
    Quantities = value
        
    
def check_single(value):
    
    i=value
    port = serial.Serial("/dev/ttyUSB0", baudrate=9600 , timeout=3.0)
    sleep(1)
    w = port.read(18)[5:12]
    a = w.decode("utf-8")                                                                                                #weight from digital scale
    print(a.strip())
    
    lower_weight = {
        300424 : 0.75,
        300324 : 1.10,
        300124 : 2.10,
        302121 : 0.85,
        302021 : 1.10,
        30032401 : 1.10
        }

    upper_weight = {
        300424 : 0.9,
        300324 : 1.21,
        300124 : 2.20,
        302121 : 0.9,
        302021 : 1.15,
        30032401 : 1.20
        }
   
    
    low = []
    high = []

    for i in range(value+1):                                                                                             #calculate expected weight
        z = lower_weight[Bricks[i]] * Quantities[i]
        low.append(z)
        x = upper_weight[Bricks[i]] * Quantities[i]
        high.append(x)
    
    runserver_s(a.strip(), z, x, Bricks[value], Quantities[value])                                                       #call server code
    if a.strip() >= str(sum(low)) and a.strip() <= str(sum(high)):
        value = 1
        return 1
    else :
        return 0