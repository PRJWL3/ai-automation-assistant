import pygame
import os
import time

pygame.mixer.init()

sound_path = os.path.join(os.getcwd(), "alarm.mp3")

pygame.mixer.music.load(sound_path)
pygame.mixer.music.play(-1)  # infinite loop

# Keep running forever
while True:
    time.sleep(1)