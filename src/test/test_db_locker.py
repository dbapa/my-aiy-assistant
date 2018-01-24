import unittest
import my_locker

class DBLockerTest(unittest.TestCase):

    def test_getContent1(self):
        self.assertEqual(my_locker.getContent("roomsensor","current"),r"/home/pi/currentRoomClimate.txt")

    def test_getContent2(self):    
        self.assertEqual(my_locker.getContent('quandl','key'),"mVT2uZx9yVpevoNYzt1n")

if __name__ == '__main__':
    unittest.main()
