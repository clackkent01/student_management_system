import unittest
from .. import create_app
from ..config.config import config_dict
from ..utils import db
from werkzeug.security import generate_password_hash
from ..models.users import User
from http import HTTPStatus


class UserTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config=config_dict['testing'])

        self.appctx = self.app.app_context()
        self.appctx.push()
        self.client = self.app.test_client()

        db.create_all()

    def tearDown(self):
        db.drop_all()

        self.appctx.pop()
        self.app = None
        self.client = None

    def test_signup(self):
        data = {
            'username': "teacher",
            'email': "teacher@gmail.com",
            'password': "password"
        }

        response = self.client.post('/signup', json=data)

        user = User.query.filter_by(email="teacher@gmail.com").first()

        self.assertEqual(user.username, "teacher")
        self.assertEqual(response.status_code, HTTPStatus.CREATED)

    def test_login(self):
        data = {
            "email": "teacher@gmail.com",
            "password": "password"
        }
        response = self.client.post('/login', json=data)

        assert response.status_code == 200
