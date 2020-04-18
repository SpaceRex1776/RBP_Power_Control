# this code is used to create a wake on lan RaspberryPi
# requires etherwake
import os
from gpiozero import LED, Button
from time import time, sleep
# variables
serverIP = "192.168.1.111" # IP address of the server
serverMac = "00:11:22:33:44:55" # Mac adress of the card for WOL
serverUser = "will" # user you are going to be logging in with
onTime = 10 # how many seconds to turn a status light on for
blinkTime = .2 # how long to blink for
blinkNum = 8 # how many times to blink the LED
#pin assigment
onLED = LED(22) # states if the server is on
errorLED = LED(17) # error LED if something goes wrong
workingLED = LED(27) # LED for when something has been sent
onButton = Button(23) # turn the server on
offButton = Button(24) # turn the server off

#time assigment for info LEDs
workingTime = time()-5 #assign a time in the past
errorTime = time()-5

# check if server conected
def serverPing():
   # print("ping Start")
    pingStatus = os.system("ping -c 1 " + serverIP) # 0 means on
   # print("ping Stop")
   # print(pingStatus)
    if pingStatus == 0:
        onLED.on()
        print("server on")
    else:
        onLED.off()
        print("server off")
# code to wake server up
def wakeUp():
    print("wake up pressed")
    # make sure nothing should be happening
    if time() - workingTime + onTime > 1 and time() - errorTime + onTime > 1:
        wakeStatus = os.system("sudo etherwake -i wlan0 "+serverMac) # send the etherwake
        if wakeStatus == 0:
            workingStatus()
            print("WOL sent")
        else:
            errorStatus()
            print("WOL had error")
    else:
        print("too many clicks")

def shutDown():
    print("shutdown pressed")
    # make sure nothing should be happening
    if time() - workingTime + onTime > 1 and time() - errorTime + onTime > 1:
        # send over ssh to shutDown
        sleepStatus = os.system("ssh "+serverUser+"@"+serverIP+" \'sudo shutdown -P now\'")
        print(sleepStatus)
        if sleepStatus == 0:
            workingStatus()
            print("Shutdown sent")
        else:
            errorStatus()
            print("shutDown Failed")
    else:
        print("too many clicks")

# update working time
def workingStatus():
    global workingTime
    workingTime = time() + onTime # time to turn off light
    workingLED.on()
    for _ in range(0,blinkNum): #how many times to blink the light
        workingLED.off()
        sleep(blinkTime)
        workingLED.on()
        sleep(blinkTime)

#update the error time
def errorStatus():
    global errorTime
    errorTime = time() + onTime # time to turn off light
    errorLED.on()
    for _ in range(0,blinkNum): #how many times to blink the light
        errorLED.off()
        sleep(blinkTime)
        errorLED.on()
        sleep(blinkTime)
# setup the buttons to to do the things
onButton.when_pressed = wakeUp
offButton.when_pressed = shutDown
# main while loop just keeps running and checking if the server is on
while True:
    sleep(1)
    serverPing() # check if the server is on
    # check what the lights should be
    if time() - workingTime < 0: # if the light should be on
        workingLED.on()
    else:
        workingLED.off()
    if time() - errorTime < 0: # if the light should be on
        errorLED.on()
    else:
        errorLED.off()
