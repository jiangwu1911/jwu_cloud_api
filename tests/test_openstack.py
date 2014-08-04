# -*- coding: UTF-8 -*-

import sys
import unittest
import novaclient.openstack.common.jsonutils as jsonutils

sys.path.append("..")
sys.path.append("../appserver")
from appserver.actions.openstack import nova_list_flavor
from appserver.utils import sql_result_to_json

reload(sys)
sys.setdefaultencoding( "utf-8" )


class UtilsTestCase(unittest.TestCase):
    def test_list_flavor(self):
        flavor_objs = nova_list_flavor()
        flavors = [f.to_dict() for f in flavor_objs if f]
        self.assertTrue(len(flavors)>2, 'test_list_flavor failed')


if __name__ == "__main__":
    unittest.main()
