import os
import subprocess

def rnx2rtkp_run(rover, base, rover_path, base_path, p):
    os.chdir(rtklib_path)
    if (len(rover) > 0 and len(base) > 0) and \
    (os.path.exists(rover_path) and os.path.exists(base_path)):
        for i in base:
            cmd = rnx2rtkp + " -k " + ppk_bike_conf + " " + \
                " " + (str(rover_path) + "\*.22O") + " " + str(i) + \
                " " + (str(rover_path) + "\*.22P") + " " + (str(rover_path) + "\*.22B") + \
                " > " + p + "\\raw_" + str(base.index(i)) + ".pos"
            print(cmd)
            print("raw.pos in process...")
            subprocess.Popen(cmd, shell=True)
        print('raw.pos creating is complete!')
    else:
        print('No bases. Check GNSS-data!')
    
source = os.getcwd()
rtklib_path = 'Z:\Bike_processing_Ignat\RTKLIB_bin-rtklib_2.4.3\/bin'
ppk_bike_conf = 'Z:\Bike_processing_Ignat\RTKLIB_bin-rtklib_2.4.3\/ppk_bike.conf'
rnx2rtkp = 'rnx2rtkp'

if __name__ == "__main__":
    for p in [os.path.abspath(i) for i in os.listdir() if os.path.isdir(i)]:
        rover_path = p + "\GPS\\rover"
        base_path = p + "\GPS\\base"
        rover = [os.path.abspath(i) for i in os.listdir(rover_path) if i.endswith(".22O")]
        base = [os.path.abspath(i) for i in os.listdir(base_path) if i.endswith(".22o")]
        rnx2rtkp_run(rover, base, rover_path, base_path, p)


