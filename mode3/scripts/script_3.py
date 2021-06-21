import sys
import logging

scripts_folder = "Z:\Bike_processing_Ignat\mode3"
sys.path.append(scripts_folder)

import bike_dirs_v3

def work(var):

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
        bike_dirs_v3.create_delta()
        logging.info("15 - DONE")
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