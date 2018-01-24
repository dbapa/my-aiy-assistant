import csv
import my_temp_sensor as myt
import time
import datetime

# get the current reading from the DHT11
tmp = myt.getCurrent()

print('temp:',tmp['temp'])

f =  open('/home/pi/currentRoomClimate.txt','w') 
f.write('temp:' +str(tmp['temp'])+'\n')
f.write('humidity:' +str(tmp['humidity'])+'\n')
f.close()

fLog =  open('/home/pi/RoomClimate.log','a') 
fLog.write(str(datetime.datetime.now())+';'+str(tmp['temp'])+';'+str(tmp['humidity'])+'\n')
fLog.close()

print('Humidity:',tmp['humidity'])
