# pylint: disable=C0111
import unittest as ut
import telegram_contacts as tc


class TelegramTest(ut.TestCase):
    """ Test the TelegramContacts functionality """

    obj = None
    '''
    def __init__(self):
        ut.TestCase.__init__(self)
        print ("constructor called")
    '''    
    def test_init(self):
        """ object instantiation test """
        self.obj = tc.TelegramContacts()
        assert self.obj != None
        print (type(self.obj))

    def test_load_contacts(self):
        """ read the contacts from the json and print them out """
        self.test_init()
        data = self.obj.get_all_data()
        print (data['contacts'])
        assert len(data['contacts']) >= 1

    def test_add_contacts(self):
        """ this should be called before save_contacts. Will save a new contact to the tree """
        self.test_load_contacts()
        l = len(self.obj.get_all_data()['contacts'])
        self.obj.add_contact("three",21232131213345522,"bap")
        data = self.obj.get_all_data()
        print (data['contacts'])
        assert len(data['contacts']) == l+1

    def test_save_contacts(self):
        """ save the newly created/added contacts back to json """
        self.test_add_contacts()
        assert self.obj.save()

        


def main():
    test_obj = TelegramTest()
    test_obj.test_init()
    test_obj.test_load_contacts()


if __name__ == '__main__':
    main()
