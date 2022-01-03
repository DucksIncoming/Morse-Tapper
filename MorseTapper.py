# Morse Tapper
# v1.0 by DucksIncoming
# 1/3/2021 - Python 3.10.1 64-bit

import speech_recognition as sr

r = sr.Recognizer()

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
    }
    return switch.get(character,"")

def morseCodify(input):
    #Change speed of morse code. All timings are based on this
    speed = 10

    #Standard morse code time spacing. Don't change
    dotTime = speed
    dashTime = speed * 3
    symbolSpacing = speed
    characterSpacing = speed * 3
    wordSpacing = speed * 7
    
    input = input.replace(' ', '')
    input = input.replace('-', '')
    shortBeep = "."
    longBeep = "-"

    inputArray = list(input)

    for inputChar in inputArray:
        print(morseCharacter(inputChar))

#Speech Recognition
with sr.Microphone() as source:
    print('Say something')
    audio = r.listen(source)
    
    try:
        text = r.recognize_google(audio)
        print(text)
        morseCodify(text)
    
    except:
        print("No speech")