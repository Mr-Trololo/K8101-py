from enum import Enum
import serial



'''
       a command is: AA, lsb(size), msb(size), cmd, [data,] chk, 55
       thus Size it is 6 bytes + data (if any)
       and checksum is SUM( size + command + params bytes, not including start & stop) modulo 256
'''

VID = 0x10cf
PID = 0x8101

# define thangs
class Command(Enum):
    bitmap = 1
    clearall = 2
    clearfg = 3
    bigtext = 4
    smalltext = 5
    beep = 6
    drawrect = 7
    eraserect = 8
    drawpixel = 9
    erasepixel = 16
    backlight = 20
    contrast = 17
    drawline = 18
    eraseline = 19
    invert = 21
    
class TextSize(Enum):
    small = 4
    big = 6


# the main command building/sending code

def checkSum(cmd):
    return sum(cmd) % 256  

def makeCommand(cmd, params):
    length = 0
    
    if cmd == Command.bitmap:
        length = 6 + 1024 + 1
    elif cmd in [Command.bigtext, Command.smalltext]:
        length = 6 + len(params) + 1
    elif cmd in [Command.drawline, Command.drawrect, Command.eraseline, Command.eraserect]:
        length = 6 + 4
    elif cmd in [Command.drawpixel, Command.erasepixel]:
        length = 6 + 2
    elif cmd in [Command.beep, Command.backlight, Command.contrast, Command.invert]:
        length = 6 + 1
    elif cmd in [Command.clearall, Command.clearfg]:
        length = 6
    
    payload = bytearray(length)
    size = len(params) + 6
    payload[1] = size & 0xFF
    if cmd in [Command.drawline, Command.eraseline, Command.drawrect, Command.eraserect]:
        payload[1] += 6
    
    payload[2] = (size >> 8) & 0xFF
    payload[3] = cmd.value
    
    for i in range(len(params)):
        payload[4 + i] = params[i]
    
    payload[-2] = checkSum(payload)
    payload[0] = 0xAA
    payload[-1] = 0x55
    
    return payload

def send(cmd): # to do: Make this not suck ass :)
    ser = serial.Serial('COM9', 9600)
    ser.write(cmd)


# here's some miscelanious code we'll need later ;)

def convertBMP(image):
    if image.mode != 'L': # Convert the image to grayscale if it's not already
        image = image.convert('L')
    pixel_data = list(image.getdata()) # Get the image data as a list of pixel values (0-255)
    binary_data = [1 if pixel < 128 else 0 for pixel in pixel_data] # Convert pixel values to 1s (black) and 0s (white)
    width, height = image.size # Determine the width and height of the image
    pixel_array = [binary_data[i:i+width] for i in range(0, len(binary_data), width)] # Reshape the 1D list into a 2D array
    # Now, pixel_array contains the binary data for each pixel in the image
    # 1 represents black, and 0 represents white

    # this headache shuffles the 1s and 0s to the stupid layout the hellish LCD wants, then converts it to decimals 0-255 and a lot more shit...
    allbands = []
    for start_row in range(0, 64, 8): # repeat from row 0 to 64 in 8 px increments
        for band in range(128): #repeat 128 times, one for each pixel (horizontally) on the screen 
            column = []
            for row in range(7, -1, -1): 
                column.append(str(pixel_array[start_row + row][band]))
            binary_string = ''.join(column) # Convert the binary array to a binary string
            decimal_value = int(binary_string, 2) # Convert the binary string to an integer
            decimal_value = min(max(decimal_value, 0), 255) # Make sure the decimal value is within the range of 0 to 255
            allbands.append(decimal_value)
    return bytearray(allbands)

# here goes all user instructions/commands

def drawBitmap(bmp):
    params = convertBMP(bmp)
    cmd = makeCommand(Command.bitmap, params)
    send(cmd)


def clearAll():
    params = [] 
    cmd = makeCommand(Command.clearall, params)
    send(cmd)

def clearForeground():
    params = [] 
    cmd = makeCommand(Command.clearfg, params)
    send(cmd)

def drawText(txt, x, y, width, size):
    params = bytearray(len(txt)+3)
    params[0] = x
    params[1] = y
    params[2] = width

    # this neat piece of code gets the text and writes it to the bytearray in ASCII numbers
    for i, char in enumerate(txt): 
        params[3+i] = ord(char) 

    if size == TextSize.big.value:
        cmd = makeCommand(Command.bigtext, params)
    elif size == TextSize.small.value:
        cmd = makeCommand(Command.smalltext, params)
    else:
        raise Exception("Hey dummy that text size doesen't exist (4s, 6b)")
    send(cmd)

def beep(num):
    params = [num] 
    cmd = makeCommand(Command.beep, params)
    send(cmd)

def drawFilledRectangle(x, y, width, height):
    params = [x, y, width, height] 
    cmd = makeCommand(Command.drawrect, params)
    send(cmd)

def drawHollowRectangle(x, y, width, height):
    drawLine(x, y, x + width, y)
    drawLine(x + width, y, x + width, y + height)
    drawLine(x + width, y + height, x, y + height)
    drawLine(x, y + height, x, y)

def eraseFilledRectangle(x, y, width, height):
    params = [x, y, width, height] 
    cmd = makeCommand(Command.eraserect, params)
    send(cmd)

def eraseHollowRectangle(x, y, width, height):
    eraseLine(x, y, x + width, y)
    eraseLine(x + width, y, x + width, y + height)
    eraseLine(x + width, y + height, x, y + height)
    eraseLine(x, y + height, x, y)

def drawPixel(x, y):
    params = [x, y] 
    cmd = makeCommand(Command.drawpixel, params)
    send(cmd)

def erasePixel(x, y):
    params = [x, y] 
    cmd = makeCommand(Command.erasepixel, params)
    send(cmd)

def backlight(sec):
    params = [sec] 
    cmd = makeCommand(Command.backlight, params)
    send(cmd)

def setContrast(c):
    params = [c] 
    cmd = makeCommand(Command.contrast, params)
    send(cmd)

def drawLine(x, y, x2, y2):
    params = [x, y, x2, y2] 
    cmd = makeCommand(Command.drawline, params)
    send(cmd)

def eraseLine(x, y, x2, y2):
    params = [x, y, x2, y2] 
    cmd = makeCommand(Command.eraseline, params)
    send(cmd)

def setInverted(inv):
    if inv:
        params = [1]
    else:
        params = [0]
    cmd = makeCommand(Command.invert, params)
    send(cmd)


# custom commands :)

def waitForKey():
    ser = serial.Serial('COM9', 9600)
    data = ser.read(size=5) # waits for serial data and saves result in variable

    if data == bytes.fromhex('ff05ff0400'):
        return("short")
    else:
        return("long")

def drawHollowCircle(x,y,rad,thick):
# Define the center and radius of the "O"
    center_x_O = x
    center_y_O = y
    radius_O = rad
    outline_thickness_O = thick  # Adjust the thickness as needed

    # Calculate the bounding box for the "O"
    x_min_O = center_x_O - radius_O
    x_max_O = center_x_O + radius_O
    y_min_O = center_y_O - radius_O
    y_max_O = center_y_O + radius_O

    # Iterate through the bounding box and draw the thicker "O" outline
    for x in range(x_min_O, x_max_O + 1):
        for y in range(y_min_O, y_max_O + 1):
            # Check if the current pixel is inside the thicker "O" outline
            distance_to_center_O = (x - center_x_O) ** 2 + (y - center_y_O) ** 2
            if (radius_O - outline_thickness_O) ** 2 <= distance_to_center_O <= (radius_O + outline_thickness_O) ** 2:
                drawPixel(x, y)



    

