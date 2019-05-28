import sys
import os
import serial
from time import sleep
from PIL import Image, ImageTk
from Image import get_img_data




def quan(value):                                                                                                         #show quantity as an image file
    Quantities = value
    if Quantities == 1:
        im = get_img_data('/home/pi/practice/order_101/1.jpg')
    elif Quantities == 2:
        im = get_img_data('/home/pi/practice/order_101/2.jpg')
    elif Quantities == 3:
        im = get_img_data('/home/pi/practice/order_101/3.jpg')
    elif Quantities == 4:
        im = get_img_data('/home/pi/practice/order_101/3.jpg')
    elif Quantities == 5:
        im = get_img_data('/home/pi/practice/order_101/5.jpg')
    return im
