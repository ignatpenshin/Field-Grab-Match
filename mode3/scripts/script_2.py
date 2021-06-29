import sys
import logging

scripts_folder = "Z:\Bike_processing_Ignat\mode3"
sys.path.append(scripts_folder)

import auto_GNSS_v3
import bike_dirs_v3

def work(GPS_dir, var, GPX_path):
    #7
    try:
        auto_GNSS_v3.babel_nmea2gpx(GPS_dir, GPX_path)
        logging.info("7 - DONE")
    except Exception as Argument:
        logging.exception("7 - FAIL")
        sys.exit(1)
    #8
    try:
        auto_GNSS_v3.filtering(GPX_path)
        logging.info("8 - DONE")
    except Exception as Argument:
        logging.exception("8 - FAIL")
        sys.exit(1)
    #9
    try:
        auto_GNSS_v3.GPS_TE()
        logging.info("9 - DONE")
    except Exception as Argument:
        logging.exception("9 - FAIL")
        sys.exit(1)
    #10
    try:
        auto_GNSS_v3.final_merge(GPX_path)
        logging.info("10 - DONE")
    except Exception as Argument:
        logging.exception("10 - FAIL")
        sys.exit(1)


    ### Bike_dirs_v3

    #11
    try:
        bike_dirs_v3.get_dirs(var)
        logging.info("11 - DONE")
    except Exception as Argument:
        logging.exception("11 - FAIL")
        sys.exit(1)
    #12
    try:
        bike_dirs_v3.get_GPS()
        logging.info("12 - DONE")
    except Exception as Argument:
        logging.exception("12 - FAIL")
        sys.exit(1)
    #13
    try:
        bike_dirs_v3.read_events()
        logging.info("13 - DONE")
    except Exception as Argument:
        logging.exception("13 - FAIL")
        sys.exit(1)
    #14
    try:
        bike_dirs_v3.read_exif()
        logging.info("14 - DONE")
    except Exception as Argument:
        logging.exception("14 - FAIL")
        sys.exit(1)
    #15
    try:
        x, y = bike_dirs_v3.create_delta()
        ls_x = ", ".join([str(item) for item in x])
        logging.info("15 - DONE\n" + "mid_list: " + ls_x + " \n" + "mid: " + str(y))
    except Exception as Argument:
        logging.exception("15 - FAIL")
        sys.exit(1)
    #16
    try:
        bike_dirs_v3.build_track()
        logging.info("16 - DONE")
    except Exception as Argument:
        logging.exception("16 - FAIL")
        sys.exit(1)    