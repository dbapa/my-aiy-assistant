# pylint: disable=C0111
import unittest
import my_locker

class MyLockerTest(unittest.TestCase):

    def test_get_content1(self):
        self.assertEqual(my_locker.getContent("roomsensor", "current"),
                         r"/home/pi/currentRoomClimate.txt")

    def test_get_content2(self):
        self.assertEqual(my_locker.getContent('quandl', 'key'), "mVT2uZx9yVpevoNYzt1n")

if __name__ == '__main__':
    unittest.main()
