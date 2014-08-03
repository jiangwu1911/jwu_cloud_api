import sys
import unittest
import json
import httplib2
from urllib import urlencode


class BaseTestCase(unittest.TestCase):
    base_url = 'http://localhost:8080/'

    def get_token(self):
        h = httplib2.Http() 
        data = {'username':'admin', 'password':'admin'}
        resp, content = h.request(self.base_url + "login",
                                  "POST",
                                  urlencode(data), 
                                  headers={'Content-Type': 'application/x-www-form-urlencoded'})  
        result = json.loads(content)
        return result['success']['token']
