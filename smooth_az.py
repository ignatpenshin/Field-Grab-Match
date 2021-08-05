import matplotlib.pyplot as plt
import numpy as np
import math 
import pandas as pd
import os
from pandas.core import indexing
from scipy.signal import savgol_filter


def circ_mean_np(angles,azimuth=True):
    """ numpy version of above"""
    rads = np.deg2rad(angles)
    av_sin = np.mean(np.sin(rads))
    av_cos = np.mean(np.cos(rads))
    ang_rad = np.arctan2(av_sin,av_cos)
    ang_deg = np.rad2deg(ang_rad)
    if azimuth:
        ang_deg = np.mod(ang_deg,360.)
    return ang_deg


def get_bearing(lat1, long1, lat2, long2):
    dLon = (long2 - long1)
    x = math.cos(math.radians(lat2)) * math.sin(math.radians(dLon))
    y = math.cos(math.radians(lat1)) * math.sin(math.radians(lat2)) \
            - math.sin(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.cos(math.radians(dLon))
    brng = np.arctan2(x,y)
    brng = np.degrees(brng)

    if brng < 0:
        brng += 360
    if brng > 360:
        brng -= 360

    return brng

if "panoramas_correction.csv" in os.listdir():

    cor = pd.read_csv("panoramas_correction.csv", header=None, sep=";")
    cor_list = cor[0].tolist()

    df = pd.read_csv("directions.csv", header=None, sep=";")
    azimuth_list = df[2].tolist()

    # Clasterisation and smoothing

    claster = []
    id_claster = []
    change_list = []
    new_azimuth_list = []
    k = 0
    count = -1
    tumb = True
    delta_ang = 22


    for z in azimuth_list:
        count += 1
        if count == 0:
            x = z
            claster.append([x])
            id_claster.append([count])
            continue
        if abs(z - x) < delta_ang:
            for s in claster[k]:
                if abs(z - s) > delta_ang:
                    tumb = False
                    break
            if tumb == True:
                x = z
                claster[k].append(x)
                id_claster[k].append(count)
            else:
                # write info to change_list
                if len(claster[k]) >= 3:
                    mean = float('{:.2f}'.format(circ_mean_np(claster[k])))
                    t = []
                    for i in range(len(claster[k])):
                        t.append(mean)
                    change_list.append(t)
                else:
                    change_list.append(claster[k])
                # end write and continue
                x = z
                claster.append([x])
                id_claster.append([count])
                k += 1
                tumb = True
        else:
            # write info to change_list
            if len(claster[k]) >= 3:
                mean = float('{:.2f}'.format(circ_mean_np(claster[k])))
                t = []
                for i in range(len(claster[k])):
                    t.append(mean)
                change_list.append(t)
            else:
                change_list.append(claster[k])
            # end write and continue
            x = z
            claster.append([x])
            id_claster.append([count])
            k += 1
        if count == len(azimuth_list) - 1:
            if len(claster[k]) >= 3:
                mean = float('{:.2f}'.format(circ_mean_np(claster[k])))
                t = []
                for i in range(len(claster[k])):
                    t.append(mean)
                change_list.append(t)
            else:
                change_list.append(claster[k])

    counter = -1
    for d in change_list:
        for c in d:
            counter += 1
            if counter not in cor_list:
                new_azimuth_list.append(c)
            else:
                new_azimuth_list.append(azimuth_list[counter])
            
    df[2] = new_azimuth_list
    df.to_csv('directions_smoothed.csv', header=False, sep=";", index=False)

    ### write to new directions



    # print(len(id_claster))
    # print(len(claster))
    #print(claster)
    # print(change_list)

    # print(sorted(claster, key=lambda l: (len(l), l)))
    # print("___________")
    # print(sorted(id_claster, key=lambda l: (len(l), l)))


    # for d in claster:
    #     plt.plot(d)

    # for s in change_list:
    #     plt.plot(s)

    # plt.show()







    # ss_list = []

    # for i in azimuth_list:
    #     rads = np.deg2rad(i)
    #     ss_list.append(np.arctan2(np.sin(rads), np.cos(rads)))

    # sav_gol = savgol_filter(ss_list, 9, 3, 0, 0, 0, 'nearest')

    # plt.plot(ss_list)
    # plt.plot(sav_gol)

    # size = len(lat_list)
    # for i in range(size):
    #     if i + 1 < size:
    #         lat_1 = lat_list[i]
    #         lon_1 = lon_list[i]
    #         lat_2 = lat_list[i+1]
    #         lon_2 = lon_list[i+1]
    #         angle = get_bearing(lat_1, lon_1, lat_2, lon_2)
    #         calc_azimuth.append(angle)
    #         mean_value.append(circ_mean_np([angle, azimuth_list[i]]))
    #     else:
    #         calc_azimuth.append(azimuth_list[i])
    #         mean_value.append(azimuth_list[i])




    # plt.plot(azimuth_list)
    # plt.plot(calc_azimuth)
    # plt.plot(mean_value)
    # plt.plot(sav_gol)

    # plt.show()



    # for i in 

    # s = get_bearing(55.755247, 37.639954, 55.755275, 37.639814)
    # print(s)


    # dir_l = [350, 355, 10, 8]

    # # print(np.mean([340, 385, 333, 376]))



    # deg = circ_mean_np(dir_l)

    # print(deg)