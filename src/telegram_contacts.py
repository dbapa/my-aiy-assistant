# pylint: disable=C0111
import json
import my_locker as locker

class TelegramContacts:
    _data = {}

    _fname = ''

    def __init__(self):
        try:
            _fname = locker.get_content("telegram", "contacts")
            with open(_fname, 'r') as fopen:
                self._data = json.load(fopen)
        except IOError:
            self._data = {'contacts':[]}
    

    def get_all_data(self):
        return self._data

    def save(self):
        try:
            with open(self._fname,'w') as fopen:
                json.dump(self._data, fopen)
        except IOError:
            return False
        finally:
            return True
    
    def add_contact(self,name,userid,name_tag=""):
        self._data['contacts'].append({
                            'name':name,
                            'id':userid,
                            'name_tag':name_tag})

    def get_contact(self,name):
        id = None
        for contact in self._data['contacts']:
            if name == contact['name']:
                id = contact 
        
        return id
