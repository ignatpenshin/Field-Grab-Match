import os

GPS = "_GPS_"

if os.path.exists(GPS) == False:
    os.mkdir(GPS)
if os.path.exists("original") == False:
    os.mkdir("original")
if os.path.exists("instaOne") == False:
    os.mkdir("instaOne")

os.chdir(GPS)
if os.path.exists("BASE") == False:
    os.mkdir("BASE")
if os.path.exists("GPXs") == False:
    os.mkdir("GPXs")
if os.path.exists("ROVER") == False:
    os.mkdir("ROVER")
if os.path.exists("_extend") == False:
    os.mkdir("_extend")
