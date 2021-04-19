from zipfile import ZipFile
import os 
import time
import subprocess


### Folders:
rtklib_path = '\\/store\global-data\Curinsta2\Bike_processing_Ignat\RTKLIB_bin-rtklib_2.4.3\/bin'
rtklib_242_path = '\\/store\global-data\Curinsta2\Bike_processing_Ignat\/rtklib_2.4.2\/bin'
rtk_events = '\\/store\global-data\Curinsta2\Bike_processing_Ignat\RTKLIB for BIKE'
ppk_bike_conf = '\\/store\/global-data\/Curinsta2\/Bike_processing_Ignat\/RTKLIB_bin-rtklib_2.4.3' + '\/ppk_bike.conf'

###### 3rd party soft paths #######
gpsbabel_path = '\\/store\global-data\Curinsta2\Bike_processing_Ignat\GPSBabel'
GPS_TRACK_EDITOR_path = "\\/store\global-data\Curinsta2\Bike_processing_Ignat\GPS Track Editor"

###### 3rd party soft cmds #######
rnx2rtkp = 'rnx2rtkp'

cmd_pos2kml = rtklib_path + '\pos2kml.exe'
cmd_babel = gpsbabel_path + "\gpsbabel.exe"
cmd_GPS_TRACK_EDITOR = GPS_TRACK_EDITOR_path + "\/GpsTrackEditor.exe"

GPS_dir = os.getcwd()
# os.chdir(GPS_dir)

### UNZIP AND LIST ALL BASE STATIONS
os.chdir('BASE')
list_base = os.listdir()
bases_dir = os.getcwd()
bases = []
for d in list_base:
    os.chdir(d)
    s = os.listdir()
    if len(s) != 0:
        for base in s:
            if (base.endswith('.21O') or base.endswith('.21o') or base.endswith('.obs')) \
                                        and bases.__contains__(str(os.path.abspath(base))) != True:
                bases.append(os.path.abspath(base))
            elif base.endswith('.zip'):      
                with ZipFile(base, 'r') as zipObj:
                    zipObj.extractall()
                for x in os.listdir():
                    if (x.endswith('.21O') or x.endswith('.21o') or x.endswith('.obs')) \
                                        and bases.__contains__(str(os.path.abspath(x))) != True:
                        bases.append(os.path.abspath(x))
    os.chdir(bases_dir)

### UNZIP AND LIST ALL ROVER FILES
os.chdir(GPS_dir)
os.chdir('ROVER')
rover_dir= os.getcwd()
list_rover = os.listdir()
nav, obs, sbs = [], [], []

for d in list_rover:
    if d.endswith('.nav') and nav.__contains__(str(os.path.abspath(d))) != True:
                nav.append(os.path.abspath(d))
    if d.endswith('.obs') and obs.__contains__(str(os.path.abspath(d))) != True:
                obs.append(os.path.abspath(d))
    if d.endswith('.sbs') and sbs.__contains__(str(os.path.abspath(d))) != True:
                sbs.append(os.path.abspath(d))     
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

### in bases, nav, sbs, obs we have all GNSS-data. Then run rnx2rtkp and iter by base

print('BASE found: ', len(bases), '\n', 'NAV found: ', len(nav), '\n',  \
                                'OBS found: ', len(obs), '\n', 'SBS found: ', len(sbs))

time.sleep(2)
### Manually run RTKpost to create EVENTS.pos
print("Manually run RTKpost to create EVENTS.pos")
print("COPY text below to RTKpost OBS rover and base path:")
print("")
print(rover_dir + "\*.obs")
print("")
time.sleep(2)
os.chdir(rtk_events)
cmd = "rtkpost"
subprocess.Popen(cmd, shell=True)
x = input("Press ENTER if you manually start RTKpost")

### Create dir for raw.pos in BASE/!pos-files
raw_pos_dir = str(bases_dir) + "\!pos-files"
if os.path.isdir(raw_pos_dir) == False:
    os.mkdir(raw_pos_dir)

os.chdir(rtklib_242_path)

### Run rnx2rtkp for all bases
if len(obs) == len(nav) == len(sbs) and len(bases) > 0:
    for i in bases:
        cmd = rnx2rtkp + " -k " + ppk_bike_conf + " " + (str(rover_dir) + "\*.obs") + " " + str(i) + \
            " " + (str(rover_dir) + "\*.nav") + " " + (str(rover_dir) + "\*.sbs") + \
                " > " + raw_pos_dir + "\/raw_" + str(bases.index(i)) + ".pos"
        if bases.index(i) < len(bases) - 1:
            subprocess.Popen(cmd, shell=True)
            time.sleep(30)
        else:
            subprocess.Popen(cmd, shell=True).wait()
            subprocess.call("echo .pos creation complete", shell=True)
else:
    print('Something goes wrong. Check GNSS-data!')

print('POS creating is complete!')

GPX_path = GPS_dir + "\GPXs"

### pos2kml file convertation
os.chdir(GPS_dir + "\BASE\!pos-files")
pos_list = []
for d in os.listdir():
    if d.__contains__('.pos') == True:
        pos_list.append(os.path.abspath(d))

os.chdir(rtklib_path)

if len(pos_list) > 0:
    print(len(pos_list), " .pos files found.")
    for pos in pos_list:
        print(pos)
        if pos_list.index(pos) < len(pos_list) - 1:
            cmd = "pos2kml" + " -tu " + pos
            subprocess.Popen(cmd, shell=True)
            print("POS to KML for ", int(pos_list.index(pos)) + 1, " file")
            time.sleep(2)
        else:
            cmd = "pos2kml" + " -tu " + pos
            subprocess.Popen(cmd, shell=True).wait()
            print("POS to KML for ", int(pos_list.index(pos)) + 1, " file") 
else:
    print("No .pos in directory. Please, check!")


print('POS to KML complete.')
time.sleep(2)

### KML to GPX convertation. Pay attention with option flags - it's sensitive to output.

os.chdir(GPS_dir + "\BASE\!pos-files")

kml_list = []
for d in os.listdir():
    if d.__contains__('.kml') == True:
        kml_list.append(os.path.abspath(d))

os.chdir(gpsbabel_path)

if len(kml_list) > 0:
    print(len(kml_list), " .kml files found.")
    for kml in kml_list:
        print(kml)
        if kml_list.index(kml) < len(kml_list) - 1:
            cmd = "gpsbabel -w -i kml -f " + kml + \
                " -x nuketypes,tracks -x transform,trk=wpt -x nuketypes,waypoints" + \
                    " -o gpx,gpxver=1.1 -F " + GPX_path + "\/raw_" + str(kml_list.index(kml)) + ".gpx"
            subprocess.Popen(cmd, shell=True).wait()
            os.remove(kml)
            print("KML to GPX for ", int(kml_list.index(kml)) + 1, " file")
        else:
            cmd = "gpsbabel -w -i kml -f " + kml + \
                " -x nuketypes,tracks -x transform,trk=wpt -x nuketypes,waypoints" + \
                    " -o gpx,gpxver=1.1 -F " + GPX_path + "\/raw_" + str(kml_list.index(kml)) + ".gpx"  
            subprocess.Popen(cmd, shell=True).wait()
            os.remove(kml)
            print("KML to GPX for ", int(kml_list.index(kml)) + 1, " file") 
else:
    print("No .kml in directory. Please, check!")

print("KML to GPX complete!")

time.sleep(2)
print("Running GPS Track Editor for merge and filter GPX data with GUI...")
time.sleep(2)

os.chdir(GPX_path)
GPXs = []
for s in os.listdir():
    GPXs.append(os.path.abspath(s))

os.chdir(GPS_TRACK_EDITOR_path)
cmd = "GpsTrackEditor " + ' '.join(GPXs)
p1 = subprocess.Popen(cmd, shell=True).wait()

print("CSV created")


