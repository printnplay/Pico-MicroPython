#Pico Invaders!
#
# TODO : Implement alien shots, Shields, Sound
from machine import Pin, I2C, ADC, PWM
from ssd1306 import SSD1306_I2C
from time import sleep
import framebuf
import random

WIDTH  = 128                                            # oled display width
HEIGHT = 64                                             # oled display height

#up = Pin(2, Pin.IN, Pin.PULL_DOWN)                     # for future games
#down = Pin(3, Pin.IN, Pin.PULL_DOWN)                   # for future games
left = Pin(4, Pin.IN, Pin.PULL_UP)
right = Pin(5, Pin.IN, Pin.PULL_UP)
button1 = Pin(14, Pin.IN, Pin.PULL_UP)

#removed for conversion to buttons

#Pot = ADC(26)
#conversion_factor = 3.3 / (65535) # Conversion from Pin read to proper voltage

speaker = PWM(Pin(18))

i2c = I2C(0)                                            # Init I2C using I2C0 defaults, SCL=Pin(GP9), SDA=Pin(GP8), freq=400000

oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)                  # Init oled display

lowres = True

if lowres == True:
    #smaller alien sprites. set spritex to 5 and spritey to 5
    inv1a = bytearray(b"\xd0xPx\xf0")
    inv1b = bytearray(b"\xf0xPx\xd0")
    inv2a = bytearray(b"\xe0P\xf8P\xe0")
    inv2b = bytearray(b"`\xd0x\xd0`")
    spritex = 5 #how big are your alien sprites?
    spritey = 5
    aliencountx = 4 #How many rows and columns of aliens
    aliencounty = 5
    alienspacingx = 5
    alienspacingy = 3
else:
     #sprite definitions for Aliens. set spritex and spritey to 7
    inv1a = bytearray(b"~\xd8\x88\xf8\x88\xd8~")
    inv1b = bytearray(b"|\xda\xc8\xf8\xc8\xda|")
    inv2a = bytearray(b"\x88\\:\x1e:\\\x88")
    inv2b = bytearray(b"\x08\\\xba\x1e\xba\\\x08")
    spritex = 7 #how big are your alien sprites?
    spritey = 7
    aliencountx = 4 #How many rows and columns of aliens
    aliencounty = 4
    alienspacingx = 3
    alienspacingy = 3
logo = bytearray(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x1f\xff\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x1f\xff\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x1f\xff\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x07\xbd\xe0\x00\x00\x00\x00\xff\xfc\x00\x00\x00\x00\x00\x00\x00\x07\xbd\xe0\x00\x00\x00\x00\xff\xfc\x00\x00\x00\x00\x00\x00\x00\x07\xbd\xe0\x00\x00\x00\x00\xff\xfc\x00\x00\x00\x01\xff\x80\x00\x07\xbd\xe0\x00\x00\x00\x00\x03\xe0\x00\x00\x00\x01\xff\x80\x00\x00\x00\x00\x00\x00\x00\x00\x1f\x00\x00\x00\x00\x01\x08\x80\x00\x00\x01\xef\x00\x00\x00\x00\xff\xfc\x00\x00\x00\x01\x08\x80\x00\x00\x01\xef\x00\x00\x00\x00\xff\xfc\x07\xff\xe0\x01\x08\x80\x00\x00\x01\xef\x00\x00\x00\x00\xff\xfc\x07\xff\xe0\x01\x08\x80\x00\x00\x01\xef\x00\x00\x00\x00\x00\x00\x07\xff\xe0\x01\xff\x80\x00\x00\x00\x00\x00\x00\x00\x00\x05\x00\x008\xe0\x00\xf7\x00\x00\x07\xbd\xefx\x1e\x00\x02\xff\x00\x00\x18\xe0\x00\x00\x00\x00\x07\xbd\xefx\x1e\x00?\xff\x00\x00?\xe0\x00\x0c\x00\x00\x07\xbd\xefx\x1e\x00?\xd0\x00\x00\x1f\xc0\x08<\x00\x00\x07\xbd\xefx\x1e\x00<\x00\x00\x00\x0f\x80\x0c\xf0\x00\x00\x00\x00\x00\x00\x00\x00?\xff\x00\x00\x00\x00\x07\xc0\x00\x00\xf0=\xe0{\xc0\x00?\xff\x00\x00\x00\x00\x03\xc0\x00\x00\xf0=\xe0{\xc0\x00\x00\xbf\x00\x00\x00\x00\x00\xf0\x00\x00\xf0=\xe0{\xc0\x00\x00\x00\x00\x00\x00\x00\x00<\x00\x00\xf0=\xe0{\xc0\x00\x00`\x00\x00\x00\x00\x00\x0c\x00\x00\x00\x00\x00\x00\x00\x00\x00\x7f\xc0\x07\xff\xe0\x00\x00\x00\x00\xf0=\xefx\x00\x00\x00\x7f\xfe\x07\xff\xe0\x00\x00\x00\x00\xf0=\xefx\x00\x00\x00\x1e\xfe\x07\xff\xe0\x00\x00\x00\x00\xf0=\xefx\x00\x00\x00\x18\x1e\x00\x00\x00\x00\x00\x00\x00\xf0=\xefx\x00\x00\x00?\xfe\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x7f\xfe\x00\x00\x00\x01\xff\x80\x00\x00=\xefx\x00\x00\x00\x7f\x80\x00\x00\x00\x01\xff\x80\x00\x00=\xefx\x00\x00\x00@\x00\x00\x00\x00\x00\x10\x80\x00\x00=\xefx\x00\x00\x00\x00\x00\x00\x00\x00\x00\x10\x80\x00\x00=\xefx\x00\x00?\xff\x00\x01\xff\x80\x00\x10\x80\x00\x00\x00\x00\x00\x00\x00?\xff\x00\x03\xff\xc0\x00\x10\x80\x00\xf0=\xefx\x00\x00?\xff\x00\x07\xff\xe0\x00\x1f\x80\x00\xf0=\xefx\x00\x008\x07\x00\x07\x00\xe0\x00\x0f\x00\x00\xf0=\xefx\x00\x000'\x00\x06\x00\xe0\x00\x00\x00\x00\xf0=\xefx\x00\x00?\xff\x00\x07\xe7\xe0\x01\xfc\x00\x00\x00\x00\x00\x00\x00\x00\x1f\xfe\x00\x03\xe3\xc0\x01\xfc\x00\x00\xf0=\xe0{\xc0\x00\x0f\xfc\x00\x01\xe3\x80\x00\x04\x00\x00\xf0=\xe0{\xc0\x00\x00\x00\x00\x00\x00\x00\x00\x04\x00\x00\xf0=\xe0{\xc0\x00\x00\x7f\xfe\x00\x00\x00\x01\xfc\x00\x00\xf0=\xe0{\xc0\x00\x00\x7f\xfe\x00\x00\x00\x01\xf8\x00\x00\x00\x00\x00\x00\x00\x00\x00\x7f\xfe\x00\x00\x00\x00\x00\x00\x00\x07\xbd\xefx\x1e\x00\x00q\xce\x01\xff\x80\x00\x00\x00\x00\x07\xbd\xefx\x1e\x00\x00`\xc6\x03\xff\xc0\x01\xff\x80\x00\x07\xbd\xefx\x1e\x00\x00p\x8e\x07\xff\xe0\x01\xff\x80\x00\x07\xbd\xefx\x1e\x00\x00\x00\x00\x07\x00\xe0\x00\x10\x80\x00\x00\x00\x00\x00\x00\x00\xff\xfc\x00\x06\x04\xe0\x00\x10\x80\x00\x00\x01\xef\x00\x00\x00\xff\xfc\x00\x07\xff\xe0\x00\x10\x80\x00\x00\x01\xef\x00\x00\x00\xff\xfc\x00\x03\xff\xc0\x00\x10\x80\x00\x00\x01\xef\x00\x00\x00\x03\x9c\x00\x01\xff\x80\x00\x1f\x80\x00\x00\x01\xef\x00\x00\x00\t\x9c\x00\x00\x00\x00\x00\x0f\x00\x00\x00\x00\x00\x00\x00\x00\xff\xfc\x00\x00\x00\x00\x00\x00\x00\x00\x07\xbd\xe0\x00\x00\x00\xfe\xf8\x00\x00\x00\x00\x00\x00\x00\x00\x07\xbd\xe0\x00\x00\x00\xfep\x00\x00\x00\x00\x00\x00\x00\x00\x07\xbd\xe0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x07\xbd\xe0\x00\x00\x00\x00\x1cx\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00<\xfc\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00|\xfe\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00q\xce\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x7f\xde\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00?\x9c\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x1f\x18\x00\x00\x00")

ship = bytearray(b" p\xf8l>//>l\xf8p ")
ufo = bytearray(b"\x0c\x00>\x80\x1d\x80\r\xe0\x1d\xc0\x15\x80>\x80\x0c\x00")

num0 = bytearray(b"\x7f\x80\xff\xc0\x80@\x80@\xff\xc0\x7f\x80")
num1 = bytearray(b"\x00\x00\x00\x80\x00\x80\xff\xc0\xff\xc0\x00\x00")
num2 = bytearray(b"\xe1\x80\xf1\xc0\x98@\x8c@\x87\xc0\x83\x80")
num3 = bytearray(b"@\x80\xc0\xc0\x84@\x84@\xff\xc0{\x80")
num4 = bytearray(b"0\x00<\x00/\x00#\x80\xff\xc0\xff\xc0")
num5 = bytearray(b"O\xc0\xcf\xc0\x84@\x84@\xfc@x@")
num6 = bytearray(b"\x7f\x80\xff\xc0\x84@\x84@\xfc\xc0x\x80")
num7 = bytearray(b"\x00@\xe0@\xfc@\x1f@\x03\xc0\x00\xc0")
num8 = bytearray(b"{\x80\xff\xc0\x84@\x84@\xff\xc0{\x80")
num9 = bytearray(b"G\x80\xcf\xc0\x88@\x88@\xff\xc0\x7f\x80")

aliens = []
class Alien(object):
    
    def __init__(self, type, x, y):
        self.visible = True
        self.type = type
        self.x = x
        self.y = y
        self.origx = x
        self.origy = y
    
def create_alien(type, x, y):
    alien = Alien(type, x, y)
    return alien

def define_aliens():
    type = "inv1a" #First row is type 1. 
    for x in range (1, aliencountx + 1):
        for y in range (1, aliencounty + 1):
            aliens.append(create_alien(type, (120 - ((x * (spritex + alienspacingx)) - spritex)), (y * (spritey + alienspacingy)) - spritey))
        if type == "inv1a":
            type = "inv2a" #Second row is type 2
        else:
            type = "inv1a"

def reset_aliens(visibility): # Used to reset aliens to starting position and, optionally, visibility
    x = 1
    y = 1
    for c in aliens:
        if visibility:
            c.visible = True
            
        c.x = c.origx
        c.y = c.origy
            
# Load images into framebuffer
inv1aBuff = framebuf.FrameBuffer(inv1a, 7, 7, framebuf.MONO_HLSB)
inv1bBuff = framebuf.FrameBuffer(inv1b, 7, 7, framebuf.MONO_HLSB)
inv2aBuff = framebuf.FrameBuffer(inv2a, 7, 7, framebuf.MONO_HLSB)
inv2bBuff = framebuf.FrameBuffer(inv2b, 7, 7, framebuf.MONO_HLSB)

ufoBuff = framebuf.FrameBuffer(ufo, 12, 8, framebuf.MONO_HLSB)

logoBuff = framebuf.FrameBuffer(logo, 128, 64, framebuf.MONO_HLSB)

#Dictionary for lookup of digits for score, level, possibly lives
numbers = {
    '0': framebuf.FrameBuffer(num0, 10, 6, framebuf.MONO_HLSB),
    '1': framebuf.FrameBuffer(num1, 10, 6, framebuf.MONO_HLSB),
    '2': framebuf.FrameBuffer(num2, 10, 6, framebuf.MONO_HLSB),
    '3': framebuf.FrameBuffer(num3, 10, 6, framebuf.MONO_HLSB),
    '4': framebuf.FrameBuffer(num4, 10, 6, framebuf.MONO_HLSB),
    '5': framebuf.FrameBuffer(num5, 10, 6, framebuf.MONO_HLSB),
    '6': framebuf.FrameBuffer(num6, 10, 6, framebuf.MONO_HLSB),
    '7': framebuf.FrameBuffer(num7, 10, 6, framebuf.MONO_HLSB),
    '8': framebuf.FrameBuffer(num8, 10, 6, framebuf.MONO_HLSB),
    '9': framebuf.FrameBuffer(num9, 10, 6, framebuf.MONO_HLSB)}

shipBuff = framebuf.FrameBuffer(ship, 8, 12, framebuf.MONO_HLSB)
# Clear the oled display in case it has junk on it.
oled.fill(0)
oled.blit(logoBuff, 0, 0)
# Finally update the oled display so the image & text is displayed
oled.show()

sleep(2)

addy = 3 #pixels of movement per turn on aliens

shotx = 1 
shoty = 140
loopCount = 0
define_aliens()
score = 0
difficulty = 1
showufo = False
ufoy = 0
ufoCount = 0
soundfreq = 160
shippos = 30
while True:
    if showufo:
        if soundfreq == 1100: soundfreq = 2000
        else: soundfreq = 1100
        speaker.freq(soundfreq)
        speaker.duty_u16(2000)
    if shotx > 36 and showufo == False: speaker.duty_u16(0)
    ufoChance = random.randrange(1, 350, 1) # 1 in 1000 chance of running this loop that UFO will appear
    if ufoChance == 123 and showufo == False:
        showufo = True
        ufoy = 0
    if showufo:
        ufoy = ufoy + 1
        if ufoy > 64:
            showufo = False
    loopCount = loopCount + 1
    oled.fill(0)
    if loopCount > 16 - difficulty:
        if showufo == False:
            if soundfreq == 180: soundfreq = 160
            elif soundfreq == 160: soundfreq = 140
            elif soundfreq == 140: soundfreq = 120
            else: soundfreq = 180
            speaker.freq(soundfreq)
            speaker.duty_u16(2000)
         
        dropdown = False
        loopCount = 0
        for c in aliens:
            if c.visible == True: #switch between sprites to animate aliens
                if c.type == "inv1a": c.type = "inv1b"
                elif c.type == "inv1b": c.type = "inv1a"
                elif c.type == "inv2a": c.type = "inv2b"
                elif c.type =="inv2b": c.type = "inv2a"
                if c.y + addy > 56 or c.y + addy < 0: #are any of the visible invaders at the edge of the screen?
                    if c.x - 3 < 20: #If they're at the bottom, reset their position
                        reset_aliens(False)
                        dropdown = False
                    dropdown = True
        if dropdown == True: #move the aliens down if any of the visible ones hit the screen edge
            addy = addy * -1
            for c in aliens:
                c.x = c.x - 3 
        else:
            for c in aliens:
                c.y = c.y + addy
                
    if left.value() == 0:
        if shippos > 1:
            shippos = shippos - 1
    
    if right.value() == 0:
        if shippos < 60:
            shippos = shippos + 1

    shotx = shotx + 2
    foundVisible = False #By default, assume all the aliens are dead
    if showufo:
        if shotx > 120 and shotx < 140:
            if shoty >= ufoy:
                if shoty < ufoy + 12:
                    score = score + 50
                    showufo = False
                    ufoy = 0
                    shotx = 140
                    shoty = int(shippos) + 6
                    
    for c in aliens:
        if shotx >= c.x and c.visible == True: #Collision detection for aliens with the shots
            if shotx - 4 <= c.x + 8:
                if shoty > c.y:
                    if shoty <= c.y + 7: #You hit an alien!
                        c.visible = False 
                        score = score + 10
                        shotx = 140
                        shoty = int(shippos) + 6
        if c.visible == True:
            foundVisible = True
            if c.type == "inv1a": #Display aliens
                oled.blit(inv1aBuff, c.x, c.y) #display animation frame 1, set to frame 2 for next time
            elif c.type == "inv1b":
                oled.blit(inv1bBuff, c.x, c.y) #display animation frame 2, set to frame 1 for next time
            elif c.type == "inv2a":
                oled.blit(inv2aBuff, c.x, c.y) #display animation frame 1, set to frame 2 for next time
            elif c.type == "inv2b":
                oled.blit(inv2bBuff, c.x, c.y) #display animation frame 2, set to frame 1 for next time
        if showufo:
            oled.blit(ufoBuff, 120, ufoy)
    if shotx > 130:
        if button1.value() == 0:
            shotx = 32
            shoty = int(shippos) + 6
        else:
            shotx = 140
  
    if foundVisible == False: # You finish the level! Increase the difficulty and reset the aliens
            if difficulty < 10:
                difficulty = difficulty + 1
            reset_aliens(True)
    
    oled.blit(shipBuff, 18, int(shippos)) # draw the ship
    oled.line(shotx, shoty, shotx - 4, shoty, 1) #draw the laser
    
    numcount = 0 #keeps track of the number of times through the loop!
    
    for c in str(score):
        oled.blit(numbers[c], 1, ((numcount * 7) + 2)) #Display the score, 1 digit at a time
        numcount = numcount + 1
    
    numcount = 0
    
    for c in str(difficulty):
        oled.blit(numbers[c], 1, 48 + ((numcount * 7) + 2)) #Display the level, 1 digit at a time
        numcount = numcount + 1
                  
    oled.show()
    if shotx == 32 and showufo == False:
        speaker.duty_u16(0)
        speaker.freq(1000)
        speaker.duty_u16(2000)
    
    sleep(0.001)
        
