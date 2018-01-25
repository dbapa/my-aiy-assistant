import configparser

locker_file = "/home/pi/locker.cfg"
#locker_file = "../../locker.cfg"

def getContent(section, key):
    locker = configparser.ConfigParser()
    locker.read(locker_file)    
    value = locker.get(section, key,raw=True)
    return value

if __name__ =='__main__':
    getContent("quandl","key")
