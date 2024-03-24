import os
import sys
import time
import random
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
    config_data[item.strip()] = float(value.strip())

peace_time = int(config_data['peace_time'])
invasion_chance = config_data['invasion_chance']
invasion_attempt_interval = int(config_data['invasion_attempt_interval'])
peace_chance = config_data['peace_chance']
peace_attempt_interval = int(config_data['peace_attempt_interval'])

timer = 0

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
            break

print(f"Please ensure that the {activation_voice} and {deactivation_voice} files of your choice are within the same folder as this .exe file, and that they are correctly named")
print(f"Time before invasions could start: {peace_time} seconds\nActivation chance: {int(invasion_chance*100)}% every {invasion_attempt_interval} seconds\nDeactivation chance: {int(peace_chance*100)}% every {peace_attempt_interval} seconds\n\nIt is more fun if you don't know when the invader is coming, make sure you're not looking at the timer all the time.\n")
input("Press Enter to start the timer...")

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