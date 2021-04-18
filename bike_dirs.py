from exif import Image
from datetime import date, datetime, timedelta
from os import listdir, chdir
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 


### CREATE MEAN VALUES 
def coord_editing(i, count, directions_list, gpx_list):
    num_right = np.searchsorted(gpx_list, i[1], side='right')
    delta_right = gpx_list[num_right] - i[1]
    delta_left = gpx_list[np.searchsorted(gpx_list, i[1], side='left')] - i[1]
    if delta_left <= 0:
        num_left = np.searchsorted(gpx_list, i[1], side='left')
    else:
        num_left = np.searchsorted(gpx_list, i[1], side='left') - 1
        delta_left = gpx_list[num_left] - i[1]

    head_left, head_right = csv['Heading'].iloc[num_left], csv['Heading'].iloc[num_right]
    lat_left, lat_right = csv['Latitude'].iloc[num_left], csv['Latitude'].iloc[num_right]
    long_left, long_right = csv['Longitude'].iloc[num_left], csv['Longitude'].iloc[num_right]
    
    heading = ((1 - abs(delta_left)/(abs(delta_right) + abs(delta_left)))*head_left
                                        + (1 - abs(delta_right)/(abs(delta_right) + abs(delta_left)))*head_right)
    latitude = ((1 - abs(delta_left)/(abs(delta_right) + abs(delta_left)))*lat_left
                                        + (1 - abs(delta_right)/(abs(delta_right) + abs(delta_left)))*lat_right)
    longitude = ((1 - abs(delta_left)/(abs(delta_right) + abs(delta_left)))*long_left
                                        + (1 - abs(delta_right)/(abs(delta_right) + abs(delta_left)))*long_right)

    head_to_dir, lat_to_dir, lon_to_dir= (float('{:.2f}'.format(heading)), 
                                        float('{:.8f}'.format(latitude)), float('{:.8f}'.format(longitude)))
                                      
       
    directions_list.append([count, i[0], head_to_dir, lat_to_dir, lon_to_dir, 155])
    count += 1

    return count, directions_list

### Read GPS
for i in listdir():
    if i.__contains__('.csv'):
        x = i


csv = pd.read_csv(x, sep=',')
gpx_list = []
print('GPS point Date/time changing to total_seconds for ', csv.shape[0], ' points. Please wait!')
for i in range(csv.shape[0]):
    if str(csv['Date/time'].iloc[i]).__contains__('.'):
        gpx_list.append((datetime.strptime(csv['Date/time'].iloc[i], '%Y-%m-%d %H:%M:%S.%f') 
                                                                            - datetime(1970, 1, 1)).total_seconds())
    else:
        gpx_list.append((datetime.strptime(csv['Date/time'].iloc[i], '%Y-%m-%d %H:%M:%S')
                                                                            - datetime(1970, 1, 1)).total_seconds())

######################################################################################

### Read events
for i in listdir():
    if i.__contains__('events'):
        f = open(i)

events_list = []
for line in f.readlines():
    if line.startswith('%') == False:
        events_list.append((datetime.strptime(line.split('   ')[0], '%Y/%m/%d %H:%M:%S.%f') 
                                                                    - datetime(1970, 1, 1) + timedelta(hours=2, minutes=59, seconds=42)).total_seconds())

delta_events = {}
for i in range(len(events_list) - 1):
    # delta_events.append(events_list[i+1] - events_list[i])
    delta_events[events_list[i]] = events_list[i+1] - events_list[i]


### Read exif times
chdir('instaOne')
exif_list = []
for photo in listdir():
    with open(photo, 'rb') as img:
        my_image = Image(img)
        utc_dt_1 = datetime.strptime(my_image.DateTime, '%Y:%m:%d %H:%M:%S')
        print(utc_dt_1)
        exif_timestamp = (utc_dt_1 - datetime(1970, 1, 1)).total_seconds()
        exif_list.append(exif_timestamp)
        print(exif_list)

print(exif_list)

delta_exif = {}
for i in range(len(exif_list) - 1):
    # delta_exif.append(exif_list[i+1] - exif_list[i])
    delta_exif[exif_list[i]] = exif_list[i+1] - exif_list[i]


### sorted tuples by dict values with reverse
list_delta_events = list(delta_events.items())
list_delta_exif = list(delta_exif.items())

######################
# x_1, y_1 = zip(*list_delta_events)
# x_2, y_2 = zip(*list_delta_exif)

# plt.plot(x_1, y_1)
# plt.plot(x_2, y_2)
# plt.grid(True)
# plt.show()
######################

list_delta_exif.sort(key=lambda i: i[1], reverse=True)
list_delta_events.sort(key=lambda i: i[1], reverse=True)


mid_delta = []
for i in list_delta_exif[:8]:
    res = min(list_delta_events[:8], key=lambda x: abs(i[0] - x[0]))
    if len(mid_delta) != 0 and max(mid_delta) - min(mid_delta) > 2:
        del mid_delta[-1]
        break
    if abs(res[0] - i[0]) <= 25: 
        mid_delta.append(i[0] - res[0])



print('Delta time from the data: ', mid_delta)
print('Median delta is: ', np.median(mid_delta))
print('Is it okay? If yes - press Enter. If not - write correct value or write NO (== 0.0) !')
mid = input("Press Enter OR write correct value OR write (NO): ")
if mid == '':
    mid = np.median(mid_delta)  ### Delta of exif and events
if mid == 'NO':
    mid = 0

####################################################################################################

### Read InstaOne        
# chdir('instaOne')
directions_list = []
count = 0
for photo in listdir():
    with open(photo, 'rb') as img:
        my_image = Image(img)
        utc_dt_1 = datetime.strptime(my_image.DateTime, '%Y:%m:%d %H:%M:%S')
        exif_timestamp = (utc_dt_1 - datetime(1970, 1, 1)).total_seconds()
        photo_data = [photo, exif_timestamp - mid]
        count, directions_list = coord_editing(photo_data, count, directions_list, gpx_list)
        print(directions_list[count-1])
        


df = pd.DataFrame(directions_list)
df.to_csv('directions.csv', header=False, sep=';', index=False)






