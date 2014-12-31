import sys
import unittest
import json
import httplib2
from urllib import urlencode

sys.path.append("..")
from appserver.utils import md5encode


class MeditoolCase(unittest.TestCase):
    base_url = 'http://www.meditool.cn'

    def testPhoneRegister(self):
        h = httplib2.Http() 
        data = {'phone': '18901398522'}
        resp, content = h.request(self.base_url + "/Register/getcode",
                                  "POST",
                                  urlencode(data),
                                  headers={'Content-Type': 'application/x-www-form-urlencoded'})
        print content 
        print resp


if __name__ == "__main__":
    unittest.main()
