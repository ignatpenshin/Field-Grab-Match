'''
Author: Penshin Ignat (HelgiLab Ltd.), 2021

To correctly make post-processing, please, install or update next packeges.

Pip install: exif, numpy, matplotlib, pandas, gpxpy, pykalman, pyautogui, 
scipy, pywin32, keyboard, opencv-python
default: time, zipfile, os, subprocess, shutil, getpass, types

''' 

import os
import time
import sys
import shutil
import subprocess
import logging

scripts_folder = "Z:\Bike_processing_Ignat\mode3"
PanoAngle_folder = "C:\projects\python\PanoAngle"
sys.path.append(scripts_folder)

import track_analyzer
import scripts.script_1
import scripts.script_2
import scripts.script_3

track_analyzer.log()

logging.basicConfig(format = '%(message)s', filemode='w', \
                             filename='track_log.log', level = logging.INFO)

# dirs 
var = os.getcwd()
for i in os.listdir():
    if i.__contains__("GPS"):
        os.chdir(i)
        GPS_dir = os.getcwd()
        GPX_path = GPS_dir + "\GPXs"

cond_1, cond_2 = track_analyzer.work(GPS_dir, GPX_path)

print("------------------")
print("Script_1 avalible (PPK + Merge + Track). input = 1 to RUN")
if cond_1 == True:
    print("Script_2 avalible (Merge + Track). input = 2 to RUN")
if cond_2 == True:
    print("Script_3 avalible (Track). input = 3 to RUN")
print("------------------\n")
x = int(input("Enter your input to run: "))



if x == int(1):
    scripts.script_1.work(GPS_dir, var, GPX_path, PanoAngle_folder)
elif x == int(2):
    scripts.script_2.work(GPS_dir, var, GPX_path, PanoAngle_folder)
elif x == int(3):
    scripts.script_3.work(var, PanoAngle_folder, GPX_path)
else:
    input("Incorrect input. Repeat, please!")
    raise Exception("1 or 2 or 3! NOT ", x)


os.chdir(var)
for i in os.listdir():
    if i.__contains__("track_log.log"):
        log = os.path.abspath(i)
    if i.__contains__("i01_"):
        track_path = os.path.abspath(i)
shutil.copyfile(log, track_path + '/track_log.log')

