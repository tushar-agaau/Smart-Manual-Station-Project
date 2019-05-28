#------------------------------------------Arduino Interface---------------------------------------------------#

import sys
import os
import serial
from time import sleep



light = serial.Serial('/dev//ttyACM0', baudrate=9600, timeout=0.5)  #acm0 might change check
sleep(1)

def Arduino(pi_order):                                 ##pi_order from loop
     pi_order1 = str.encode(pi_order + "q")
     print("pi_order" , pi_order1)
     light.write(pi_order1)                          ## write to arduino
     while True:                                   #temporary
         data = light.read(2)                            ## read arduino
         data = data.decode('ascii')
         data = data.split(' ', 1)                                    
         print(data[0])                                  
         break
     return data[0]

                
                
          
                
                    
            
                
            
                
                    
     
        
        

           
    