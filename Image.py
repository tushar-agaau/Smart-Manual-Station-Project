from PIL import Image, ImageTk
import io
import PySimpleGUI as sg
import sys
import os
from time import sleep

def get_img_data(f, maxsize = (300, 300), first = True):                                                                #convert any format to png
    img = Image.open(f)
    img.thumbnail(maxsize)
    if first:                     # tkinter is inactive the first time
        bio = io.BytesIO()
        img.save(bio, format = "PNG")
        del img
        return bio.getvalue()
    return ImageTk.PhotoImage(img)


