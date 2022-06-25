import unittest

from app import app
from api import db


class BaseCase(unittest.TestCase):

    def setUp(self):
        self.app = app#.test_client()
        self.db = db
        self.db.init_app(self.app)
        with self.app.app_context():
            self.db.create_all()
            # self.populate_db() 


    def tearDown(self):
        # Delete Database collections after the test is complete
        with self.app.app_context():
            self.db.session.remove()
            self.db.drop_all()

