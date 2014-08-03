import sys
import unittest
import json
import httplib2
from urllib import urlencode


BASE_URL='http://localhost:8080/'
SERVER_PORT=80
TIMEOUT=30
TEST_TOKEN="ece83cbdac1b43bb9dac367e25b3aa16"

class UserTestCase(unittest.TestCase):
    def test_list_user(self):
        h = httplib2.Http() 
        resp, content = h.request(BASE_URL + "user",
                                  "GET",
                                  headers={'Content-Type': 'application/x-www-form-urlencoded',
                                           'X-Auth-Token': TEST_TOKEN}
                                 )  
        #print resp  
        print json.loads(content)


if __name__ == "__main__":
    unittest.main()
