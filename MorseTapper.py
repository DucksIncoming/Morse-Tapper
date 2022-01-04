# Morse Tapper
# v1.0 by DucksIncoming
# 1/3/2021 - Python 3.10.1 64-bit

# This video was very helpful I'm glad I don't have to deal with any cloud APIs
# https://www.youtube.com/watch?v=K_WbsFrPUCk

import speech_recognition as sr
import time
from pyfirmata import Arduino, SERVO

# Arduino config
port = "COM5" # Set to the USB port of your arduino device
servoPin = 9 # Set to your servo pin
servoPinType = "digital" # Set to analog if using analog

try:
	board = Arduino(port)
except:
	print("Arduino board not plugged in! (Or not accessible on specified port)")
	time.sleep(5000)
	quit()
if (servoPinType == "digital"):
    board.digital[servoPin].mode = SERVO
else:
    board.analog[servoPin].mode = SERVO

# Speech recognition stuff, don't mess with unless u know how it works
r = sr.Recognizer()
r.pause_threshold = 0.3
r.non_speaking_duration = r.pause_threshold
r.WaitTimeoutError = 2
r.energy_threshold = 3000

#Convert characters to morse code
def morseCharacter(character):
    switch = {
        "a":
            ".-",
        "b":
            "-...",
        "c":
            "-.-.",
        "d":
            "-..",
        "e":
            ".",
        "f":
            "..-.",
        "g":
            "--.",
        "h":
            "....",
        "i":
            "..",
        "j":
            ".---",
        "k":
            "-.-",
        "l":
            ".-..",
        "m":
            "--",
        "n":
            "-.",
        "o":
            "---",
        "p":
            ".--.",
        "q":
            "--.-",
        "r":
            ".-.",
        "s":
            "...",
        "t":
            "-",
        "u":
            "..-",
        "v":
            "...-",
        "w":
            ".--",
        "x":
            "-..-",
        "y":
            "-.--",
        "z":
            "--..",
        "0":
            "-----",
        "1":
            ".----",
        "2":
            "..---",
        "3":
            "...--",
        "4":
            "....-",
        "5":
            ".....",
        "6":
            "-....",
        "7":
            "--...",
        "8":
            "---..",
        "9":
            "----.",
        "|":
            "X",
        "=":
            ">"
    }
    return switch.get(character,"")

def morseCodify(input):
    input = input.replace(' ', '|')
    input = input.replace('-', '')

    inputArray = list(input)

    for inputChar in inputArray:
        for morseChar in morseCharacter(inputChar):
            tap(morseChar)
        tap(morseCharacter("="))

#Speech Recognition
def searchForSpeech():
    with sr.Microphone() as source:
        audio = r.listen(source)
        
    try:
        text = str(r.recognize_google(audio))
        
        #You can pry swearing from my cold dead hands
        text = text.replace('f***', 'fuck')
        text = text.replace('s***', 'shit')
        text = text.replace('b****', 'bitch')

        text = text.lower()
        
        print(text)
        morseCodify(text)
        
    except:
        print("...")


# Functions to make stuff more readable
def tapDown(pin):
    if (servoPinType == "digital"):
        board.digital[pin].write(45) # Angle is mostly arbitrary, just found 45 works well
    else:
        board.analog[pin].write(45)

def tapUp(pin):
    if (servoPinType == "digital"):
        board.digital[pin].write(0)
    else:
        board.analog[pin].write(0)

def tap(tapType):
    # Change speed of morse code (in s). All timings are based on this
    # 0.15 is about the fastest you should go, since the servo doesn't have enough speed to make the full rotation in any time less than that. Even 0.15 is a bit rough for this, I stick with 0.2
    # If you're using a different/stronger servo feel free to make this lower
    speed = 0.1

    #Don't change these unless you want to change the entire morseCharacter() function
    dot = "."
    dash = "-"
    wordBreak = "X"
    charBreak = ">"

    #Standard morse code time spacing. Don't change
    dotTime = speed
    dashTime = speed * 3
    symbolSpacing = speed # Unused but here for completeness
    intraCharacterSpacing = speed
    characterSpacing = speed * 3
    wordSpacing = speed * 7

    #This should be a switch statement but with python its so much effort so here's some inefficiency for u as a gift
    if (tapType == dot):
        tapDown(9)
        print(".")
        time.sleep(dotTime)
        
        tapUp(9)
        print(" ")
        time.sleep(intraCharacterSpacing)
    elif (tapType == dash):
        tapDown(9)
        print("-")
        time.sleep(dashTime)
        
        tapUp(9)
        print(" ")
        time.sleep(intraCharacterSpacing)
    elif (tapType == wordBreak):
        print("X")
        #This feels sloppy but its easier than checking if its the end of a sentence in the first place
        time.sleep(wordSpacing - characterSpacing)
    elif (tapType == charBreak):
        print(">")
        time.sleep(characterSpacing - intraCharacterSpacing)

while True:
    searchForSpeech()