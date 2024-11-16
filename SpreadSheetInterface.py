from datetime import date, datetime, timedelta
import os
import time
from pynput.keyboard import Key, Controller

key = Controller()

import pyperclip

if os.name == "posix":
    copyKey = Key.cmd
elif os.name == "nt":
    copyKey = Key.ctrl


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
    with key.pressed(copyKey):
        key.press("c")
        key.release("c")
    delay()
    return pyperclip.paste()

def goHome():
    with key.pressed(copyKey):
        for i in range(10):
            press(Key.up)
            press(Key.left)

def goAmt(Amt=0, strDirection="Down"):
    # set direction
    if Amt < 0:
        Amt = Amt * -1
        match strDirection:
            case "Down":
                Direction = Key.up
            case "Up":
                Direction = Key.down
            case "Left":
                Direction = Key.right
            case "Right":
                Direction = Key.left
            case _:
                raise ValueError("Invalid direction")
    else:
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
    multiPress(copyKey, Key.down)
    # go back to date
    goAmt(amtRight, "Left")
    # check date difference from current
    previousDate = datetime.strptime(getCell(), "%d/%m/%Y")
    currentDate = date.today()
    dateDif = currentDate.toordinal() - previousDate.toordinal()
    
    # print dates to current day
    neg = 1
    if dateDif < 0:
        neg = -1
        dateDif = dateDif * -1
    for i in range(dateDif):
        goAmt(neg, "Down")
        # type in previous date + 1
        key.type((previousDate + timedelta(days=(i + 1) * neg)).strftime("%d/%m/%Y"))

    
    
    
    # go back to yt column
    goAmt(amtRight, "Right")
    # ends with cursor on first yt column
    return dateDif
class WatchTime:
    def __init__(self, amtShorts, amtVideos, timeShorts, timeVideos, totalTime):
        self.amtShorts = amtShorts
        self.amtVideos = amtVideos
        self.timeShorts = timeShorts
        self.timeVideos = timeVideos
        self.totalTime = totalTime
        
a = WatchTime(1, 1, "0h", "0h", "0h")

def setWatchTime(totalTime, amtShorts, timeShorts, amtVideos, timeVideos):
    """
    convert time values from seconds to hours:minutes:seconds
    """
    
    totalTime = time.strftime("%Hh%Mm%Ss", time.gmtime(totalTime))
    timeShorts = time.strftime("%Hh%Mm%Ss", time.gmtime(timeShorts))
    timeVideos = time.strftime("%Hh%Mm%Ss", time.gmtime(timeVideos))
    key.type(totalTime)
    press(Key.tab)
    key.type(str(amtShorts))
    press(Key.tab)
    key.type(timeShorts)
    press(Key.tab)
    key.type(str(amtVideos))
    press(Key.tab)
    key.type(timeVideos)
    multiPress(copyKey, 's')
    goAmt(4, "Left")
    goAmt(1, "Up")
    

# time.sleep(2)
# # setWatchTime(a)
# daysToGet = getLatestYtEntry()
# setWatchTime(a)