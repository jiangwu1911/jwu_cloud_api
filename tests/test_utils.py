import sys
import unittest
import json
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

sys.path.append("..")
from appserver.model import User
from appserver.utils import sql_results_to_json
from appserver.utils import md5encode


class UtilsTestCase(unittest.TestCase):
    def _create_session(self):
        engine = create_engine('mysql://%s:%s@%s/%s?charset=%s' %
                               ('root', '', 'localhost', 'cloudapi', 'utf8'),
                               echo=True)
        Session = sessionmaker(bind=engine)
        session = Session()
        return session
        

    def atest_json_user_encode(self):
        session = self._create_session()
        results = session.query(User)
        str = sql_results_to_json(results, 'users')
        print json.loads(str) 


    def test_md5encode(self):
        print md5encode('admin')
        

if __name__ == "__main__":
    unittest.main()
