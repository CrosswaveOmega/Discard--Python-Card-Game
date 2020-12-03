import math

from tkinter import *
from PIL import Image, ImageTk, ImageGrab, ImageDraw, ImageFont
import time
import textwrap
import urllib.request

from ..main.generic.notationhelp import to_notation


def url_to_PIL_image(image_url):
    #full_path = file_path + file_name + '.png'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.76 Safari/537.36', }
    request = urllib.request.Request(image_url, None, headers)
    response = urllib.request.urlopen(request)
    image = Image.open(response)
    return image



def make_card_grid_icon(pil_image, team=1, hp_float=1, name=""):
    squaresize = 188
    background = Image.open(
        """Discard_Main\classes\imagemakingfunctions\imageres\CardEX.png""")
    fontname = """Discard_Main\classes\imagemakingfunctions\imageres\{}""".format(
        'bahnschrift.ttf')


    newfont = ImageFont.truetype(fontname, 32)
    other_font = ImageFont.truetype(fontname, 32)
    d = ImageDraw.Draw(background)
    to_replace = (0,0,0)
    if team==1:
        to_replace=(255,0,0)
    if team==2:
        to_replace=(0,0,255)
    #background = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    new_image_data = []
    datas = background.getdata()
    for item in datas:
        # change all white (also shades of whites) pixels to yellow
        if item[0] in list(range(210, 256)):
            new_image_data.append(to_replace)
        else:
            new_image_data.append(item)

    # update image data
    background.putdata(new_image_data)
    background.paste(pil_image.resize((squaresize, squaresize)), (28, 28))
    d.text((64, 218), text=str(hp_float),
           anchor='ma', font=newfont, fill="black")
    d.text((48, 0), text=str(name), font=iconfont, fill="black")

    return background


def make_image_from_grid(grid, col, row):
    squaresize = 256
    width, height = col * squaresize, row * squaresize
    pasteme = Image.open(
        """Discard_Main\classes\imagemakingfunctions\imageres\GridSquare.png""")
    fontname = """Discard_Main\classes\imagemakingfunctions\imageres\{}""".format(
        'bahnschrift.ttf')
    newfont = ImageFont.truetype(fontname, 72)

    background = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    d = ImageDraw.Draw(background)
    for j in range(col):
        for i in range(row):
            if(isinstance(grid[i][j], str)):
                background.paste(pasteme, (j * squaresize, i * squaresize))
                if(grid[i][j] != "_"):
                    name = grid[i][j]
                    x, y = j * squaresize, i * squaresize
                    x = x + squaresize // 2
                    y = y + squaresize // 2
                    d.text((x, y), text=name, anchor='mb',
                           font=newfont, fill="White")
                else:
                    name = to_notation(j + 1, i + 1)
                    x, y = j * squaresize, i * squaresize
                    x = x + squaresize // 2
                    y = y + squaresize // 2
                    d.text((x, y), text=name, anchor='mb',
                           font=newfont, fill="Black")

            else:
                background.paste(pasteme, (j * squaresize, i * squaresize))
                cardsqu = grid[i][j]
                background.paste(cardsqu, (j * squaresize + 6,
                                           i * squaresize + 6), cardsqu)

    return background


def make_summon_cost(r, b, g):
    img = Image.open(
        "Discard_Main\classes\imagemakingfunctions\imageres\scost.png")
    width, height = img.size
    background = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    background.paste(img)
    return background


def make_card_image(cardimg=None):
    if(cardimg != None):
        img = Image.open(cardimg)
        width, height = img.size
        background = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        background.paste(img)
        return background


def makeNumber(number):
    """makes the param :number: into a image"""
    # turns a integer into a image.
    sizeX = 32  # size of number
    sizeY = 32
    path = "C:\\Users\\xtrea\\OneDrive\\classes\\"
    path = "classes/"
    img = Image.open(
        """Discard_Main\classes\imagemakingfunctions\imageres\mario_numbers.png""")

    stringNumber = str(number)
    background = Image.new(
        'RGBA', (len(stringNumber) * sizeX, sizeY), (0, 0, 0, 0))
#    background.paste(img)
    d = ImageDraw.Draw(background)
    cursor = 0
    for char in stringNumber:
        x = int(char)
        startX = x * sizeX
        crop = img.crop((startX, 0, startX + sizeY, sizeY))
        background.paste(crop, (cursor * sizeX, 0))
        cursor = cursor + 1
    return (background)


def dc(expressionA, expressionB, success_msg="ok", casea_msg="none", caseb_msg="none"):
    passA, passB = False, False
    if(expressionA):
        passA = True
    else:
        print(casea_msg)
    if(expressionB):
        passB = True
    else:
        print(caseb_msg)
    if(passA and passB):
        s = 1 + 2
        # Ok.
    return passA and passB
# We really need to re-organize everything.


# Funciton is for the math behind scaling a uploaded image
def custom_image_scaling(scaled_width, scaled_height, offset_x, offset_y):
    display_width, display_height = 402,  224

    display_x, display_y = 21, 63

    res = dc(scaled_width >= display_width, scaled_height >= display_height,
             "Test A passed.", "scaled_width is too low.", "scaled_height is too low.")
    if(res):
        print("Test A Passed.")
    res2 = dc(offset_x <= display_x, offset_y <= display_y,
              "Test B passed.", "offset_x is too high.", "offset_y is too high.")

    if(res2):
        print("Test B Passed")

    diff_x = display_x - offset_x
    diff_y = display_y - offset_y

    rem_x = scaled_width - diff_x
    rem_y = scaled_height - diff_y

    max_diff_x = scaled_width - display_width
    max_diff_y = scaled_height - display_height
    res3 = dc(rem_x >= display_width, rem_y >= display_height,
              "Test C passed.", "remainder_x is too low.", "remainder_y is too low.")

    if(res3):
        print("Test C Passed")

    print("scaled_size", scaled_width, scaled_height)
    print("scaled_offset", offset_x, offset_y)
    print("display_size", display_width, display_height)
    print("display_offset", display_x, display_y)

    print("diff", diff_x, diff_y)
    print("rem", rem_x, rem_y)
    print("max_diff", max_diff_x, max_diff_y)

    range_x = display_x - max_diff_x
    range_y = display_y - max_diff_y
    print("range", range_x, range_y)
    print("")


# Driver Code.
if __name__ == "__main__":
    custom_image_scaling(521, 288, 0, 0)

    print("CLUSTER_TEST.")
    custom_image_scaling(521, 288, 200, 0)

    custom_image_scaling(521, 288, -98, 0)
    custom_image_scaling(521, 288, 21, 0)
    custom_image_scaling(521, 288, -150, 0)
    custom_image_scaling(521, 288, 50, 0)
    custom_image_scaling(521, 288, 521, 0)
    custom_image_scaling(521, 288, 521 - 21, 0)

    custom_image_scaling(521, 288, -521 + 22, 0)
    custom_image_scaling(521, 288, -521, 0)
