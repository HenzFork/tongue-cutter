import os
import sys
import time
import random
import ctypes
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

path = os.path.dirname(sys.argv[0])

activation_voice = "activate.mp3"
deactivation_voice = "deactivate.mp3"
with open(os.path.join(path, "config.txt"), "r") as file:
    config_lines = file.readlines()

config_data = {}
for line in config_lines:
    item, value = line.strip().split('=')
    config_data[item.strip()] = value.strip()

peace_time = int(config_data['peace_time'])
invasion_chance = float(config_data['invasion_chance'])
invasion_attempt_interval = int(config_data['invasion_attempt_interval'])
peace_chance = float(config_data['peace_chance'])
peace_attempt_interval = int(config_data['peace_attempt_interval'])
shortcut_key = str(config_data['taunters_tongue_shortcut'].upper())

buttons = {"E":0x12, "LEFT":0xCB, "UP":0xC8, "RIGHT":0xCD, "DOWN":0xD0}


SendInput = ctypes.windll.user32.SendInput
PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]
                
class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                 ("mi", MouseInput),
                 ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]


def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))



def play_sound(file):
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(file)
    pygame.mixer.music.play()

def toggle_tongue(toggle_chance, attempt_interval, voice):
    while True:
        time.sleep(attempt_interval)
        if random.random() < toggle_chance:
            play_sound(os.path.join(path, voice))
            PressKey(buttons["E"])
            time.sleep(0.3)
            PressKey(buttons[shortcut_key])
            time.sleep(0.3)
            ReleaseKey(buttons["E"])
            ReleaseKey(buttons[shortcut_key])
            time.sleep(0.3)
            PressKey(buttons["E"])
            time.sleep(0.3)
            ReleaseKey(buttons["E"])
    
            break

print(f"Please ensure that the {activation_voice} and {deactivation_voice} files of your choice are within the same folder as this .exe file, and that they are correctly named")
print(f"Time before invasions could start: {peace_time} seconds\nActivation chance: {int(invasion_chance*100)}% every {invasion_attempt_interval} seconds\nDeactivation chance: {int(peace_chance*100)}% every {peace_attempt_interval} seconds\nYour taunter's tongue should be set on the {shortcut_key} button\n\nIt is more fun if you don't know when the invader is coming, make sure you're not looking at the timer all the time.\n")
input("Press Enter to start the timer...")

timer = 0

while True:
    time.sleep(1)
    timer +=1
    print(f"Time left in peace: {str(timer)}/{str(peace_time)} seconds..")
    if timer >= peace_time:
        print("Rolling the dice..")
        toggle_tongue(invasion_chance, invasion_attempt_interval, activation_voice)
        print("Invasions Active!")
        toggle_tongue(peace_chance, peace_attempt_interval, deactivation_voice)
        print("Invasions Disabled!")
        timer = 0