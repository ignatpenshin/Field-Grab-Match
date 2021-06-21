import os
import time
import sys
import logging
import auto_GNSS_v3

def log():
    log_exist = os.path.isfile("track_log.log")
    print('log exist: ', log_exist, '\n')
    if log_exist == True:
        print("---- LOG_START ----\n")
        with open("track_log.log", "r") as file:
            for line in file:
                if line.__contains__("FAIL"):
                    print(line)
                if line.__contains__("6 - DONE"):
                    print("6 - GNSS post-processing - DONE\n")
                if line.__contains__("10 - DONE"):
                    print("10 - Final.csv - DONE\n")
                if line.__contains__("16 - DONE"):
                    print("16 - Track processing and building - DONE")
        print("---- LOG_END ----\n")


def work(GPS_dir, GPX_path):

    condition_1 = False
    condition_2 = False

    print("Run Track Analyzer...\n")

    #1 try_paths - обязательно выполнить проверку на исключения
    try:
        auto_GNSS_v3.try_paths()
        logging.info("1 - DONE")
    except Exception as Argument:
        logging.exception("1 - FAIL")  
        sys.exit(1)

    #2 unzip_bases - обязательно выполнить
    try:
        bases = auto_GNSS_v3.unzip_bases()
        logging.info("2 - DONE")
        time.sleep(2)
        base_num = len(bases)
    except Exception as Argument:
        logging.exception("2 - FAIL")
        sys.exit(1)

    #3 unzip_rover - обязательно выполнить
    try:    
        auto_GNSS_v3.unzip_rover(GPS_dir)
        logging.info("3 - DONE")
    except Exception as Argument:
        logging.exception("3 - FAIL")
        sys.exit(1)
    
    #4 rtkpost_run - не запускается, если есть events
    try:  
        is_event_list = auto_GNSS_v3.rtkpost_run()  
        logging.info("4 - DONE")
        time.sleep(2)
        event_num = len(is_event_list)
    except Exception as Argument:
        logging.exception("4 - FAIL")
        sys.exit(1)
    
    #5 create_nmea_dir - не запускается, если уже есть папка
    try:
        nmea_num = auto_GNSS_v3.create_nmea_dir() 
        logging.info("5 - DONE")
        time.sleep(2)
    except Exception as Argument:
        logging.exception("5 - FAIL")   
        sys.exit(1)
    
    # raw_filter.gpx - how many?
    list = []
    for i in os.listdir(GPX_path):
        if i.__contains__("raw") and i.__contains__("_filter") == True:
            list.append(i)
    filter_num = len(list)

    # FINAL.CSV EXISTS?
    os.chdir(GPX_path)
    if os.path.isfile("final.csv") == True:
        final_num = 1
    else:
        final_num = 0

    # ОТЧЕТ ПО ТРЕКУ
    print("\n_____Analysis result_____")
    print("\n", "Event: ", event_num, "\n", \
                               "NMEA: ", nmea_num, "\n", "Filtered: ", filter_num, "\n", "Final.csv: ", final_num, "\n")

    # CONDITION CREATE
    if nmea_num >= base_num and event_num == 1:
        condition_1 = True
    if final_num == 1:
        condition_2 = True
    
    return condition_1, condition_2
