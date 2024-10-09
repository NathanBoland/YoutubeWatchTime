from datetime import date
import time
from pynput.keyboard import Key, Controller

key = Controller()

import pyperclip


def delay():
    time.sleep(0.07)


def press(keyToPress):
    "Press and unpress the specifed Key obj or Char"
    key.press(keyToPress)
    key.release(keyToPress)
    delay()


def multiPress(key1, key2):
    "Press and unpress key2 while key1 is held down"
    with key.pressed(key1):
        press(key2)
    delay()


def getCell():
    with key.pressed(Key.cmd):
        key.press("c")
        key.release("c")
    delay()
    return pyperclip.paste()


def goHome():
    with key.pressed(Key.cmd):
        for i in range(10):
            press(Key.up)
            press(Key.left)


def goAmt(Amt=0, strDirection="Down"):
    # set direction
    match strDirection:
        case "Down":
            Direction = Key.down
        case "Up":
            Direction = Key.up
        case "Left":
            Direction = Key.left
        case "Right":
            Direction = Key.right
        case _:
            raise ValueError("Invalid direction")

    for i in range(Amt):
        press(Direction)


def findCell(strToFind="", strDirection="Down"):
    "Goes to a string in the direction specified"
    # set direction
    match strDirection:
        case "Down":
            Direction = Key.down
            timeOut = 100
        case "Up":
            Direction = Key.up
            timeOut = 300
        case "Left":
            Direction = Key.left
            timeOut = 25
        case "Right":
            Direction = Key.right
            timeOut = 25
        case _:
            raise ValueError("Invalid direction")

    for i in range(timeOut):
        if getCell() == strToFind:
            return i
        key.press(Direction)


time.sleep(2)

# finds current date
currentCell = findCell(date.today().strftime("%m/%d/%Y").replace("/0", "/"), "Down")

goHome()

findCell("Youtube Time", "Right")

goAmt(currentCell, "Down")

if getCell().strip() == "":
    key.type("Hello")
else:
    print("Nah")


# Key presses would work, but possibly editing the actial csv file would be much better
# - Can't really get it to have a locally stored csv that syncs with drive
