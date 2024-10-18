from datetime import date, datetime
import time
from pynput.keyboard import Key, Controller

key = Controller()

import pyperclip


def delay():
    time.sleep(0.09)

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
            timeOut = 100
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

def getLatestYtEntry():
    goHome()
    # go to youtube column
    amtRight = findCell("Youtube", "Right")
    # go to most recent youtube entry
    multiPress(Key.cmd, Key.down)
    # go back to date
    goAmt(amtRight, "Left")
    # check date difference from current
    previousDate = datetime.strptime(getCell(), "%m/%d/%Y")
    currentDate = date.today()
    dateDif = currentDate.toordinal() - previousDate.toordinal()
    # go back to yt column
    goAmt(amtRight, "Right")
    goAmt(dateDif, "Down")
    # ends with cursor on first yt column
    return dateDif


time.sleep(2)
daysToGet = getLatestYtEntry()
