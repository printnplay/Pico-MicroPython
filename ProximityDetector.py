from machine import Pin, PWM
import utime

pulse = Pin(18, Pin.OUT)
receiver = Pin(26, Pin.IN, Pin.PULL_DOWN)

speaker = PWM(Pin(19))

def CheckDistance():
    SpeedOfSoundInMM = 0.343
    pulse.low()
    utime.sleep_us(20)
    pulse.high()
    utime.sleep_us(10)
    pulse.low()
    exitLoop = False
    loopcount = 0 #used as a failsafe if the signal doesn't return
    while receiver.value() == 0 and exitLoop == False:
        loopcount = loopcount + 1
        delaytime = utime.ticks_us()
        
        if loopcount > 3000 : exitLoop == True
    
    while receiver.value() == 1 and exitLoop == False:
        loopcount = loopcount + 1
        receivetime = utime.ticks_us()
        if loopcount > 3000 : exitLoop == True
    
    if exitLoop == True: #We failed somewhere
        return 0
    else:
        distance = ((receivetime - delaytime) * SpeedOfSoundInMM) / 2
        return distance

while True:
    distance = CheckDistance()
    print(distance)
    if CheckDistance() < 2500:
        speaker.duty_u16(3000)
        speaker.freq(1700)
        utime.sleep(0.05)
        speaker.duty_u16(0)
        utime.sleep(CheckDistance() / 1000)
  

