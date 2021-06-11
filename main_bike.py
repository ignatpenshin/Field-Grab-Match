import os
import subprocess
import time

'''
Author: Penshin Ignat (HelgiLab Ltd.), 2021

To correctly make post-processing, please, install or update next packeges.

Pip install: exif, numpy, matplotlib, pandas, gpxpy, pykalman, pyautogui, 
scipy, pywin32, keyboard, opencv-python
default: time, zipfile, os, subprocess, shutil, getpass, types
''' 

stitcher_folder = "C:\Program Files\Insta360 Studio 2021\Insta360 Studio 2021.exe"
scripts_folder = "Z:\Bike_processing_Ignat"


print("-------------")
# print("Run Stitcher")
# subprocess.Popen(stitcher_folder)
# input("Press Enter to continue processing :")

Track = os.getcwd()

for i in os.listdir():
    if i.__contains__("GPS"):
        os.chdir(i)
        GPS = os.getcwd()

os.chdir(scripts_folder)

subprocess.Popen('auto_GNSS_v2.py ' + GPS, shell=True).wait()

time.sleep(10)

# input("Press Enter if Navigation processing complete and all panoramas are stitched :")

subprocess.Popen('bike_dirs.py ' + Track, shell=True).wait()

print("Track processing complete!")
input("Press ENTER to close Bike_processing script!")


    
