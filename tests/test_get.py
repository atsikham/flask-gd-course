import urllib.request
import os

from flask_testing import LiveServerTestCase
from app import create_test_app, db


class GetTest(LiveServerTestCase):

    def create_app(self):
        os.chdir('../')
        return create_test_app()

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_animals(self):
        response = urllib.request.urlopen(self.get_server_url() + '/animals')
        self.assertEqual(response.code, 200)

    def test_species(self):
        response = urllib.request.urlopen(self.get_server_url() + '/species')
        self.assertEqual(response.code, 200)

    def test_centers(self):
        response = urllib.request.urlopen(self.get_server_url() + '/centers')
        self.assertEqual(response.code, 200)
