import os 
import sys
import time
import subprocess
import gpxpy
import shutil
import pandas as pd
import getpass
import tarfile
import matplotlib.pyplot as plt
from types import LambdaType
from gpxpy.geo import length_3d
from zipfile import ZipFile
from numpy.core.arrayprint import TimedeltaFormat
from pykalman import KalmanFilter
import AUTOGUI_PYTHON.auto_gui_test

### Folders and launchers exist?:
def try_paths():
    global rtklib_path, rtklib_242_path, rtk_events
    global ppk_bike_conf, gpsbabel_path, GPS_TRACK_EDITOR_path
    global autogui_path, rnx2rtkp, cmd_pos2kml, cmd_babel, cmd_GPS_TRACK_EDITOR
    path_control_list = []

    ###### FOLDERS ########
    rtklib_path = 'Z:\Bike_processing_Ignat\RTKLIB_bin-rtklib_2.4.3\/bin'
    path_control_list.append(rtklib_path)

    rtklib_242_path = 'Z:\Bike_processing_Ignat\/rtklib_2.4.2\/bin'
    path_control_list.append(rtklib_242_path)

    rtk_events = 'Z:\Bike_processing_Ignat\RTKLIB for BIKE'
    path_control_list.append(rtk_events)

    ppk_bike_conf = 'Z:\Bike_processing_Ignat\RTKLIB_bin-rtklib_2.4.3\/nmea.conf'
    path_control_list.append(ppk_bike_conf)

    ###### 3rd party soft paths #######
    gpsbabel_path = 'Z:\Bike_processing_Ignat\GPSBabel'
    path_control_list.append(gpsbabel_path)

    GPS_TRACK_EDITOR_path = "Z:\Bike_processing_Ignat\GPS Track Editor"
    path_control_list.append(GPS_TRACK_EDITOR_path)
    
    autogui_path = "Z:\Bike_processing_Ignat\mode3\AUTOGUI_PYTHON"
    path_control_list.append(autogui_path) 

    ###### 3rd party soft cmds #######
    rnx2rtkp = 'rnx2rtkp'
    cmd_pos2kml = rtklib_path + '\pos2kml.exe'
    cmd_babel = gpsbabel_path + "\gpsbabel.exe"
    cmd_GPS_TRACK_EDITOR = GPS_TRACK_EDITOR_path + "\/GpsTrackEditor.exe"

    for i in path_control_list:
        if os.path.exists(i) == False:
            raise Exception(i + " is not exist")
 
### -----------------------------------------------------------------------

### GPS TRACK EDITOR OPP
def craft_filter(list, iter=3, speed_lim=4.5, accel_lim=0.85, lim_filter=0.65):   # iter=3, speed_lim=5, accel_lim=1.4, lim_filter=0.6
    for raw in list:
        print("------------------------------")
        print("Filtering process for ", list.index(raw) + 1, " track from ", len(list))
        print("Track name: ", raw)
        with open(raw) as fh:
            gpx_file = gpxpy.parse(fh)

        print("File has {} track(s).".format(len(gpx_file.tracks)))
        print("Track has {} segment(s).".format(len(gpx_file.tracks[0].segments)))

        segment = gpx_file.tracks[0].segments[0]

        start_len = segment.points.__len__()
        print('Points on start: ', start_len)

        for i in range(iter):
            tik = time.perf_counter()
            for x in segment.points:
                x.speed = None
            segment.points[0].speed = 0.0
            segment.points[-1].speed = 0.0
            gpx_file.add_missing_speeds()
            gpx_file.add_missing_elevations()
            point_1 = segment.points[0]
            for p in segment.points[1:]:
                try:
                    point_2 = p
                    speed_1 = point_1.speed
                    speed_2 = point_2.speed
                    delta_speed = speed_2 - speed_1
                    time_dif = point_2.time_difference(point_1)
                    accel = abs(delta_speed/time_dif)
                    if speed_2 > speed_lim or accel > accel_lim:
                        segment.points.remove(p)
                        continue
                except TypeError:
                    segment.points.remove(p)
                    continue
                point_1 = point_2
            gpx_file.smooth(vertical=True, horizontal=True, remove_extremes=True)
            tok = time.perf_counter()
            print(i + 1 , ' iteration ', f"made for {tok - tik:0.4f} seconds")

        finish_len = segment.points.__len__()
        print('Points on finish: ', finish_len)

        if finish_len > lim_filter*start_len:
            with open(raw[:-4] + "_filter.gpx", 'w') as fh:
                fh.write(gpx_file.to_xml())
        else:
            print(start_len-finish_len, " from ", start_len," was deleted while filtering!")
            print("Track ", raw, " can't be used!")

        print("------------------------------")

### ----------------------------------------------------------------------------------


### UNZIP AND LIST ALL BASE STATIONS

def unzip_bases():
    global bases_dir, bases
    os.chdir('BASE')
    def tree():
        os.chdir("rinex")
        while True:
            s = os.listdir()
            if len(s) == 1:
                os.chdir(s[0])
            else:
                return os.listdir()

    trigger = False
    this_d = os.getcwd()
    tar_list = os.listdir(this_d)

    for n in tar_list:
        if n.endswith(".tar"):
            trigger = True
            mytar = tarfile.open(n)
            mytar.extractall()
            mytar.close()
    os.chdir(this_d)

    if trigger == True:
        Bases = tree()
        hall = os.getcwd()
        for s in Bases:
            os.chdir(s)
            rars = os.listdir()
            for rar in rars:
                if rar.endswith(".zip"):
                    with ZipFile(rar, "r") as zipObj:
                        zipObj.extractall()
                        zipObj.close()
                os.remove(rar)
            os.chdir(hall)
            shutil.move(s, this_d)
        os.chdir(this_d)
        shutil.rmtree("rinex/")
        for n in tar_list:
            if n.endswith(".tar"):
                os.remove(n)

    list_base = os.listdir()
    bases_dir = os.getcwd()
    bases = []

    for d in list_base:
        os.chdir(d)
        cwd = os.getcwd()
        s = os.listdir()
        ong_base = []
        if len(s) != 0:
            for base in s:
                if (base.endswith('.21O') or base.endswith('.21o') or base.endswith('.obs')) \
                                            and ong_base.__contains__(str(os.path.abspath(cwd) + "\*.21o")) != True:
                    ong_base.append(os.path.abspath(cwd) + "\*.21o")
                # if (base.endswith('.21N') or base.endswith('.21n')) \
                                            # and ong_base.__contains__(str(os.path.abspath(cwd) + "\*.21n")) != True:
                    # ong_base.append(os.path.abspath(cwd) + "\*.21n")
                # if (base.endswith('.21G') or base.endswith('.21g')) \
                                            # and ong_base.__contains__(str(os.path.abspath(cwd) + "\*.21g")) != True:
                    # ong_base.append(os.path.abspath(cwd) + "\*.21g")
        if len(ong_base) == 1:
            bases.append(ong_base)
        os.chdir(bases_dir)
    return bases

### UNZIP AND LIST ALL ROVER FILES
### in bases, nav, sbs, obs we have all GNSS-data. Then run rnx2rtkp and iter by base

def unzip_rover(GPS_dir):
    global rover_dir
    global nav, obs, sbs
    global o21, p21, b21
    os.chdir(GPS_dir)
    os.chdir('ROVER')
    rover_dir= os.getcwd()
    list_rover = os.listdir()
    nav, obs, sbs = [], [], []
    o21, p21, b21 = [], [], []
    for d in list_rover:
        if d.endswith('.nav') and nav.__contains__(str(os.path.abspath(d))) != True:
                    nav.append(os.path.abspath(d))
        if d.endswith('.obs') and obs.__contains__(str(os.path.abspath(d))) != True:
                    obs.append(os.path.abspath(d))
        if d.endswith('.sbs') and sbs.__contains__(str(os.path.abspath(d))) != True:
                    sbs.append(os.path.abspath(d))     

        if d.endswith('.21P') and p21.__contains__(str(os.path.abspath(d))) != True:
                    p21.append(os.path.abspath(d))
        if d.endswith('.21O') and o21.__contains__(str(os.path.abspath(d))) != True:
                    o21.append(os.path.abspath(d))
        if d.endswith('.21B') and b21.__contains__(str(os.path.abspath(d))) != True:
                    b21.append(os.path.abspath(d)) 

        elif d.endswith('.zip'):      
            with ZipFile(d, 'r') as zipObj:
                zipObj.extractall()
            for x in os.listdir():
                if x.endswith('.nav') and nav.__contains__(str(os.path.abspath(x))) != True:
                    nav.append(os.path.abspath(x))
                if x.endswith('.obs') and obs.__contains__(str(os.path.abspath(x))) != True:
                    obs.append(os.path.abspath(x))
                if x.endswith('.sbs') and sbs.__contains__(str(os.path.abspath(x))) != True:
                    sbs.append(os.path.abspath(x))

                if d.endswith('.21P') and p21.__contains__(str(os.path.abspath(d))) != True:
                    p21.append(os.path.abspath(d))
                if d.endswith('.21O') and o21.__contains__(str(os.path.abspath(d))) != True:
                            o21.append(os.path.abspath(d))
                if d.endswith('.21B') and b21.__contains__(str(os.path.abspath(d))) != True:
                            b21.append(os.path.abspath(d)) 

    print('BASE found: ', len(bases), '\n', 'NAV found: ', len(nav), '\n',  \
                            'OBS found: ', len(obs), '\n', 'SBS found: ', len(sbs), '\n', \
                                '21P found: ', len(p21), '\n', '21O found: ', len(o21), '\n', '21B found: ', len(b21))
    time.sleep(2)

### Manually run RTKpost to create EVENTS.pos
def rtkpost_run():
    is_event_list = []
    for path, dirs, files in os.walk(rover_dir):
        for i in files:
            if i.__contains__('events') == True:
                is_event_list.append(i)
    if len(is_event_list) == 0:
        print("Manually run RTKpost to create EVENTS.pos")
        print("COPY text below to RTKpost OBS rover and base path:\n")
        if len(o21) > 0:
            print(rover_dir + "\*.21O\n")
        if len(obs) > 0:
            print(rover_dir + "\*.obs\n")
        time.sleep(2)
        os.chdir(rtk_events)
        cmd = "rtkpost"
        subprocess.Popen(cmd, shell=True)
        x = input("Press ENTER if you manually start RTKpost")
    return is_event_list

### Create dir for raw.nmea in BASE/!nmea-files
def create_nmea_dir():
    global raw_pos_dir
    raw_pos_dir = str(bases_dir) + "\!nmea-files"
    if os.path.isdir(raw_pos_dir) == False:
        os.mkdir(raw_pos_dir)
        return len(os.listdir(raw_pos_dir))
    else:
        return len(os.listdir(raw_pos_dir))


### Run rnx2rtkp for all bases
def rnx2rtkp_run(GPS_dir):
    os.chdir(rtklib_path)
    #if len(obs) == len(nav) == len(sbs) and len(bases) > 0:
    if len(bases) > 0 and len(obs) > 0:
        for i in bases:
            cmd = rnx2rtkp + " -k " + ppk_bike_conf + " " + (str(rover_dir) + "\*.obs") + " " + str(i[0]) + \
                " " + (str(rover_dir) + "\*.nav") + " " + (str(rover_dir) + "\*.sbs") + \
                    " > " + raw_pos_dir + "\/raw_" + str(bases.index(i)) + ".nmea"
            print("raw_" + str(bases.index(i)) + ".nmea" " in process...")
            if bases.index(i) < len(bases) - 1:
                subprocess.Popen(cmd, shell=True)
                time.sleep(15)
            else:
                print("All raws in process. Please, check rnx2rtkp activitiess in Task Manager.")
                subprocess.Popen(cmd, shell=True).wait()
                subprocess.call("echo .nmea creation complete", shell=True)
    elif len(bases) > 0 and len(o21) > 0:
        for i in bases:
            cmd = rnx2rtkp + " -k " + ppk_bike_conf + " " + (str(rover_dir) + "\*.21O") + " " + str(i[0]) + \
                " " + (str(rover_dir) + "\*.21P") + " " + (str(rover_dir) + "\*.21B") + \
                    " > " + raw_pos_dir + "\/raw_" + str(bases.index(i)) + ".nmea"
            print("raw_" + str(bases.index(i)) + ".nmea" " in process...")
            if bases.index(i) < len(bases) - 1:
                subprocess.Popen(cmd, shell=True)
                time.sleep(15)
            else:
                print("All raws in process. Please, check rnx2rtkp activitiess in Task Manager.")
                subprocess.Popen(cmd, shell=True).wait()
                subprocess.call("echo .nmea creation complete", shell=True)
    else:
        print('No bases. Check GNSS-data!')
    print('NMEA creating is complete!')
    


### gpsbabel nmea-gpx file convertation
def babel_nmea2gpx(GPS_dir, GPX_path):
    os.chdir(GPS_dir + "\BASE\!nmea-files")
    nmea_list = []
    for d in os.listdir():
        if d.__contains__('.nmea') == True:
            nmea_list.append(os.path.abspath(d))
    os.chdir(gpsbabel_path)
    if len(nmea_list) > 0:
        print(len(nmea_list), " .nmea files found.")
        for nmea in nmea_list:
            print(nmea)
            if nmea_list.index(nmea) < len(nmea_list) - 1:
                cmd = "gpsbabel -w -i nmea -f " + nmea + \
                        " -o gpx,gpxver=1.1 -F " + GPX_path + "\/raw_" + str(nmea_list.index(nmea)) + ".gpx"
                subprocess.Popen(cmd, shell=True).wait()
                # os.remove(nmea)
                print("NMEA to GPX for ", int(nmea_list.index(nmea)) + 1, " file")
            else:
                cmd = "gpsbabel -w -i nmea -f " + nmea + \
                        " -o gpx,gpxver=1.1 -F " + GPX_path + "\/raw_" + str(nmea_list.index(nmea)) + ".gpx"  
                subprocess.Popen(cmd, shell=True).wait()
                # os.remove(kml)
                print("NMEA to GPX for ", int(nmea_list.index(nmea)) + 1, " file") 
    else:
        print("No .nmea in directory. Please, check!")
    print("NMEA to GPX complete!")
    # " -x nuketypes,tracks -x transform,trk=wpt -x nuketypes,waypoints"


# Filter all tracks
def filtering(GPX_path):
    print("Run filtering process...")
    os.chdir(GPX_path)
    list = []
    for i in os.listdir():
        if i.__contains__("raw") and i.__contains__("_filter") == False:
            list.append(i)
    craft_filter(list)

# Merge all tracks
def GPS_TE():
    global merged_track_path
    print("Running GPS Track Editor for merge and filter GPX data with GUI...")
    user_name = getpass.getuser()
    print("user_name: ", user_name)
    merged_track_path = "C:\\Users\\" + user_name + "\\Documents\\_TRACKS"
    print("merged track dir: ", merged_track_path)
    list = []
    for i in os.listdir():
        if (i.__contains__("raw") == False and i.__contains__('.gpx')) or \
                                                             i.__contains__("_filter.gpx"):
            list.append(os.path.abspath(i))

    os.chdir(GPS_TRACK_EDITOR_path)
    cmd = "GpsTrackEditor " + ' '.join(list)
    p1 = subprocess.Popen(cmd, shell=True)
    s = int(input("Press 1 to RUN AutoGUI / 0 to CLOSE: "))
    if s == 1:
        time.sleep(10)
        os.chdir(autogui_path)
        # p2 = subprocess.Popen('auto_gui_test.py', shell=True).wait()
        AUTOGUI_PYTHON.auto_gui_test.work()
        time.sleep(15)
    else:
        raise Exception("BREAK ON MERGE")

# move final track and rename to final.csv for next using 
def final_merge(GPX_path):
    merged_file_name = "final_merged.csv"
    os.chdir(merged_track_path)
    for i in os.listdir():
        if i.__contains__(merged_file_name):
            shutil.move(os.path.abspath(i), GPX_path)
            os.chdir(GPX_path)
            if os.path.exists("final.csv") == True:
                os.remove("final.csv")
            os.rename("final_merged.csv", "final.csv")
    print("CSV created")


