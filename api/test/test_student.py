import json
import unittest
from .. import create_app
from ..config.config import config_dict
from ..models.management import Student
from ..utils import db


class StudentTestCase(unittest.TestCase):
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

    def test_create_student(self):
        student_data = {
            'id': 1,
            'name': 'John Doe',
            'email': 'johndoe@example.com'
        }

        response = self.client.post('/student/student', data=json.dumps(student_data),
                                    content_type='application/json')
        print(response.json)
        self.assertEqual(response.status_code, 200)

        student = Student.query.filter_by(id=1).first()
        self.assertEqual(student.name, 'John Doe')
        self.assertEqual(student.email, 'johndoe@example.com')

    def test_get_all_students(self):
        student_data = {
            'id': 1,
            'name': 'John Doe',
            'email': 'johndoe@example.com'
        }

        self.client.post('student/student', data=json.dumps(student_data),
                         content_type='application/json')

        response = self.client.get('student/student')
        self.assertEqual(response.status_code, 200)

        response_data = json.loads(response.data)
        self.assertEqual(len(response_data), 1)
        self.assertEqual(response_data[0]['name'], 'John Doe')
        self.assertEqual(response_data[0]['email'], 'johndoe@example.com')

    def test_update_student(self):
        student_data = {
            'id': 1,
            'name': 'John Doe',
            'email': 'johndoe@example.com'
        }

        self.client.post('student/student', data=json.dumps(student_data),
                         content_type='application/json')

        updated_student_data = {
            'id': 1,
            'name': 'Jane Doe',
            'email': 'janedoe@example.com'
        }

        response = self.client.put('student/student/1', data=json.dumps(updated_student_data),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)

        student = Student.query.filter_by(id=1).first()
        self.assertEqual(student.name, 'Jane Doe')
        self.assertEqual(student.email, 'janedoe@example.com')

    def test_delete_student(self):
        student_data = {
            'id': 1,
            'name': 'John Doe',
            'email': 'johndoe@example.com'
        }

        self.client.post('student/student', data=json.dumps(student_data),
                         content_type='application/json')

        response = self.client.delete('student/student/1')
        self.assertEqual(response.status_code, 204)

        student = Student.query.filter_by(id=1).first()
        self.assertIsNone(student)

    def test_get_student_by_id(self):
        student_data = {
            'id': 1,
            'name': 'John Doe',
            'email': 'johndoe@example.com'
        }

        self.client.post('student/student', data=json.dumps(student_data),
                         content_type='application/json')

        response = self.client.get('student/student/1')
        self.assertEqual(response.status_code, 200)

        response_data = json.loads(response.data)
        self.assertEqual(response_data['name'], 'John Doe')
        self.assertEqual(response_data['email'], 'johndoe@example.com')
