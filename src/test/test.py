import csv
import my_temp_sensor as myt

tmp = myt.getCurrent()

print('temp:',tmp)


def test():
    with open('/home/pi/currentRoomClimate.txt','w') as f:
        f.write('temp:' +str(tmp['temp'])+'\n')
        f.write('humidity:' +str(tmp['humidity'])+'\n')
    return True

print('Humidity:',tmp['humidity'])
