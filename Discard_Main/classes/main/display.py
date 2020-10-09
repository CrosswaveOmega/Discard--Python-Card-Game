#This is a class to help make images.


import math

from tkinter import *
from PIL import Image, ImageTk, ImageGrab, ImageDraw, ImageFont
import time
import textwrap

class Imaging_Class:
    #This class helps with making images.
    def scale_image_and_open(self, scale):
        image = Image.open("source.png")
        image.thumbnail(size, Image.ANTIALIAS)
        image.save("newfile.png", "png")

    def makeNumber(self, number):
        #turns a integer into a image.
        sizeX=32 #size of number
        sizeY=32
        path="C:\\Users\\xtrea\\OneDrive\\classes\\"
        path="classes/"
        img = Image.open("mario_numbers.png")

        stringNumber=str(number)
        background = Image.new('RGBA', (len(stringNumber)*sizeX, sizeY), (0, 0, 0, 0))
    #    background.paste(img)
        d=ImageDraw.Draw(background)
        cursor=0
        for char in stringNumber:
            x=int(char)
            startX=x*sizeX
            crop=img.crop((startX,0,startX+sizeY,sizeY))
            background.paste(crop,(cursor*sizeX,0))
            cursor=cursor+1
        return (background)
    def makeCardWithHP(self, number):
        #For making a character card with HP.
        sizeX=32 #size of number
        sizeY=32
        path="C:\\Users\\xtrea\\OneDrive\\classes\\"
        path="classes/"
        img = Image.open("cardlayout-big.png")

        stringNumber=str(number)
        width, height = img.size
        background = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        background.paste(img)
        d=ImageDraw.Draw(background)

        hpStart=Image.open("HP_Meter_Start.png")
        hpMid=Image.open("HP_Meter_Middle.png")
        hpEnd=Image.open("HP_Meter_End.png")
        to_paste=self.makeNumber(number)
        background.paste(hpStart, (18,63), hpStart)
        widthofnumbers, heightofnumbers=to_paste.size
        for i in range (0,widthofnumbers):
            background.paste(hpMid, (24+i, 63), hpMid)
        background.paste(hpEnd, (21+widthofnumbers, 63), hpEnd)
        background.paste(to_paste,(24,69),to_paste)
        return background


#Driver Code.
if __name__ == "__main__":
    imake=Imaging_Class()
    img=imake.makeCardWithHP(555)
    img.save("Card.PNG")
