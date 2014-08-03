import sys
import unittest
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

sys.path.append("..")
from appserver.model import User
from appserver.utils import JsonEncoder


class JsonTestCase(unittest.TestCase):
    def _create_session(self):
        engine = create_engine('mysql://%s:%s@%s/%s?charset=%s' %
                               ('root', '', 'localhost', 'cloudapi', 'utf8'),
                               echo=False)
        Session = sessionmaker(bind=engine)
        session = Session()
        return session
        

    def test_encode(self):
        session = self._create_session()
        users = session.query(User)
        #for user in users:
        #    print JsonEncoder().encode(user)
        #user = User(name='admin', password='admin')
        #print JsonEncoder().encode(user)
        

if __name__ == "__main__":
    unittest.main()
