import time
from pynput.keyboard import Key, Controller
def delay():
    time.sleep(0.4)

time.sleep(3)

key = Controller()
key.type('hello')
delay()
key.press(Key.tab)
key.release(Key.tab)
delay()

with key.pressed(Key.cmd):
    key.press('c')
    key.release('c')
delay()
key.press(Key.tab)
key.release(Key.tab)
delay()
with key.pressed(Key.cmd):
    key.press("v")
    key.release("v")

# Key presses could work, but possibly editing the actial csv file would be much better
